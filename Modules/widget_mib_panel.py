# This Python file uses the following encoding: utf-8
import os
import re
#import pysnmp
from typing import Dict

from pysmi.reader import FileReader
#from pysmi.searcher import StubSearcher,PyFileSearcher, PyPackageSearcher
from pysmi.writer import CallbackWriter
from pysmi.parser import SmiStarParser #, SmiV2Parser, SmiV1CompatParser
from pysmi.codegen import JsonCodeGen #, PySnmpCodeGen
from pysmi.compiler import MibCompiler
import json

from Modules.mib_data import MIB_DATA
from Modules.dialog_snmp_request import SNMPRequestDialog

from Forms.ui_widget_mib_panel import Ui_WidgetMIBPanel

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QDialog
from Modules.common import *
class MIBPanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_WidgetMIBPanel()
        self.ui.setupUi(self)

        self.snmp_ip_address = 'localhost'
        self.snmp_community = 'public'
        
        self.ui.pushButton_Apply.setVisible(False)
        self.ui.pushButton_Cancel.setVisible(False) 

        self.ui.pushButton_SNMP_Request.clicked.connect(self.showSnmpRequestDialog)
        
        self.loaded_mibs: Dict[str, Dict[str, MIB_DATA]] = {}
        self.missing_mibs: Dict[str, list] = {}

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name'])
        self.ui.treeView_MIB.setModel(self.model)
        self.ui.treeView_MIB.selectionModel().selectionChanged.connect(self.onSelectionChangedEvent)
        
        self.initDetailInfo()
        return
    def resetMIBs(self):
        self.initDetailInfo()
        self.loaded_mibs.clear()
        self.missing_mibs.clear()
        return
    def initDetailInfo(self):        
        self.model.clear()
        self.ui.comboBox_Kind.clear()
        self.ui.comboBox_Kind.addItems(["Single", "Table Column"])
        self.ui.comboBox_Type.clear()
        self.ui.comboBox_Type.addItems(["Gauge", "Delta", "String"])
        self.ui.comboBox_Unit.clear()
        self.ui.comboBox_Unit.addItems(["Bytes", "Percent", "Custom"])
        self.ui.comboBox_Scale.clear()
        self.ui.comboBox_Scale.addItems(["Divide", "Multiply"])
        self.clearDetailInfo()
        return
    def clearDetailInfo(self):
        self.ui.pushButton_SNMP_Request.setEnabled(False)
        self.ui.lineEdit_Agent.clear()
        self.ui.lineEdit_Agent.setReadOnly(True)
        self.ui.lineEdit_Group.clear()
        self.ui.lineEdit_Group.setReadOnly(True)
        self.ui.lineEdit_Name.clear()
        self.ui.lineEdit_Name.setReadOnly(True)
        self.ui.comboBox_Kind.setCurrentIndex(0)# setCurrentText("Table")
        self.ui.comboBox_Kind.setEnabled(False)
        self.ui.lineEdit_OID.clear()
        self.ui.lineEdit_OID.setReadOnly(True)
        self.ui.comboBox_Type.setCurrentIndex(0)
        self.ui.comboBox_Type.setEnabled(False)
        self.ui.checkBox_unsigned.setChecked(True)
        self.ui.checkBox_unsigned.setEnabled(False)
        self.ui.checkBox_64bit.setChecked(False)
        self.ui.checkBox_64bit.setEnabled(False)
        self.ui.checkBox_float.setChecked(False)
        self.ui.checkBox_float.setEnabled(False)
        self.ui.comboBox_Unit.setCurrentIndex(0)
        self.ui.comboBox_Unit.setEnabled(False)
        self.ui.lineEdit_Unit.clear()
        self.ui.lineEdit_Unit.setReadOnly(True)
        self.ui.lineEdit_Indicator.clear()
        self.ui.lineEdit_Indicator.setReadOnly(True)
        self.ui.lineEdit_Scale.setText("1")
        self.ui.lineEdit_Scale.setReadOnly(True)
        self.ui.comboBox_Scale.setCurrentIndex(0)
        self.ui.comboBox_Scale.setEnabled(False)
        self.ui.textEdit_Description.clear()
        self.ui.textEdit_Description.setReadOnly(True)
        self.ui.textEdit_Lookup.clear()
        self.ui.textEdit_Lookup.setReadOnly(True)
        return
    def missingMIBsClear(self):
        self.missing_mibs.clear()
        return
    def getMissingMIBs(self):
        return self.missing_mibs
    def getLoadedMIBs(self):
        return self.loaded_mibs
    def loadingMIB(self, file_name):
        if file_name:
            module_name = os.path.basename(file_name).split('.')[0]
            inputMibs = [module_name]
            srcDirectory = os.path.dirname(file_name)
            srcBaseDirectory = get_base_dir("base_mibs")
            try:
                with open(file_name, 'r') as mib_file:
                    if module_name in self.loaded_mibs:
                        self.removeModel(module_name)
                    self.loaded_mibs[module_name] = {}
                    self.loaded_mibs[module_name][module_name] = MIB_DATA()
                    self.loaded_mibs[module_name][module_name].SetMIBData(mib_file.read())
                    self.loaded_mibs[module_name][module_name].SetName(module_name)

                    self.missing_mibs[module_name] = []
            except Exception as e:
                print(f"Error read MIB file: {e}")
                return

            def printOut(mibName, jsonDoc, cbCtx):
                #print(f"{os.linesep}{os.linesep}# MIB module {mibName}")
                try:
                    jsonDoc = json.loads(jsonDoc)  # Parse JSON string to dictionary
                    if mibName not in self.loaded_mibs[module_name]:
                        self.loaded_mibs[module_name][mibName] = MIB_DATA()
                    self.loaded_mibs[module_name][mibName].SetJsonData(jsonDoc)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error for {mibName}: {e}")
                    return
                except Exception as e:
                    print(f"Error processing jsonDoc for {mibName}: {e}")
                    return

            # print("MibCompiler start")
            mibCompiler = MibCompiler(SmiStarParser(), JsonCodeGen(), CallbackWriter(printOut))
            # print("add_sources start")
            mibCompiler.add_sources(FileReader(srcDirectory))
            # print("add_sources for base mib start")
            mibCompiler.add_sources(FileReader(srcBaseDirectory))
            # print("add_searchers start")
            # mibCompiler.add_searchers(StubSearcher(*JsonCodeGen.baseMibs))
            try:
                # print("Starting MIB compilation...")
                results = mibCompiler.compile(*inputMibs, genTexts=True)
                # QMessageBox.information(self, "MIB File Loading Result", f"{results}")
                if results[module_name] == 'compiled':
                    del self.missing_mibs[module_name]
                    self.addModel(module_name)                    
                else:
                    for key, value in results.items():
                        if value == "missing":
                            self.missing_mibs[module_name].append(key)
            except Exception as e:
                print(f"Compilation failed with error: {e}") 
        return   
    def addModel(self, module_name:str):
        self.loaded_mibs[module_name][module_name].MakeGroups()
        mib_data = self.loaded_mibs[module_name][module_name]
        root_item = self.model.invisibleRootItem()
        mib_item = QStandardItem(mib_data.GetName())
        mib_item.setFlags(mib_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        mib_item.setData(mib_data.GetName())

        for i in range(mib_data.GetGroupCounts()):
            group_info = mib_data.GetGroup(i)

            if group_info:
                groupName, objects = group_info
                group_item = QStandardItem(groupName)
                group_item.setFlags(group_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                group_item.setData(groupName)
                mib_item.appendRow(group_item)

                for object_name in objects:
                    object_item = QStandardItem(self.extractName(object_name))
                    object_item.setFlags(object_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    object_item.setData(object_name)
                    group_item.appendRow(object_item)
        root_item.appendRow(mib_item)
        return
    def removeModel(self, mib_item: str):
        model = self.model
        items = model.findItems(mib_item, Qt.MatchExactly)
        if items:
            index = model.indexFromItem(items[0])
            if index.isValid():
                model.removeRow(index.row(), index.parent())
        return
    def extractName(self, name):
        phrase = re.sub(r'(?<!^)(?=[A-Z])', ' ', name).lower()
        words = phrase.split()
        if words and words[-1].startswith("group"):
            return ' '.join(words[:-1])
        return phrase
    def updateDetailInfo(self, item_type: str, module_name:str, item_name:str, group_name):
        self.clearDetailInfo()
        if item_type == "object":
            self.ui.lineEdit_Agent.setText(module_name)
            self.ui.lineEdit_Group.setText(group_name)
            self.ui.lineEdit_Name.setText(self.extractName(item_name))

            if self.loaded_mibs[module_name][module_name].GetJsonData() and self.loaded_mibs[module_name][module_name].GetJsonData().get(item_name):
                object_item = self.loaded_mibs[module_name][module_name].GetJsonData()[item_name]
                #print(object_item)
                if object_item.get("nodetype") and object_item["nodetype"] == "column":
                    self.ui.comboBox_Kind.setCurrentIndex(1)
                if object_item.get("oid"):
                    oid : str= object_item["oid"]
                    if len(oid.split('.')) < 10:
                        oid += ".0"
                    self.ui.lineEdit_OID.setText(oid)
                if object_item.get("syntax") and object_item["syntax"].get("type"):
                    if object_item["syntax"]["type"] == "Counter32":
                        self.ui.comboBox_Type.setCurrentIndex(1) # Delta
                        self.ui.checkBox_unsigned.setChecked(True)
                    elif object_item["syntax"]["type"] == "Integer32" or object_item["syntax"]["type"] == "InterfaceIndex" or object_item["syntax"]["type"] == "INTEGER" or object_item["syntax"]["type"] == "TimeTicks" or object_item["syntax"]["type"] == "Timeout":
                        self.ui.comboBox_Type.setCurrentIndex(0) # Gauge
                        self.ui.checkBox_unsigned.setChecked(False)
                    else:
                        self.ui.comboBox_Type.setCurrentIndex(2) # String
                        self.ui.checkBox_unsigned.setChecked(False)
                if object_item.get("units"):
                    self.ui.comboBox_Unit.setCurrentIndex(2)
                    self.ui.lineEdit_Unit.setText(object_item["units"])
                else:
                    self.ui.comboBox_Unit.setCurrentIndex(2)
                    self.ui.lineEdit_Unit.setText("#")
                if object_item.get("name"):
                    self.ui.lineEdit_Indicator.setText(self.extractName(object_item["name"]))
                if object_item.get("description"):
                    self.ui.textEdit_Description.setText(object_item["description"])
                if object_item.get("syntax") and object_item["syntax"].get("constraints") and object_item["syntax"]["constraints"].get("enumeration"):
                    lookup:str = ""
                    sorted_items = sorted(object_item["syntax"]["constraints"]["enumeration"].items(), key=lambda item: item[1])
                    for key, value in sorted_items:
                        lookup += f"{key}({value})\n"
                    self.ui.textEdit_Lookup.setText(lookup.strip())
                self.ui.pushButton_SNMP_Request.setEnabled(True)
        return
    def onSelectionChangedEvent(self, selected, deselected):
        indexes = self.ui.treeView_MIB.selectedIndexes()
        if indexes:
            item = self.model.itemFromIndex(indexes[0])
            item_type = "module"
            module_name = item.text()
            item_name = item.data()
            group_name = item.data()
            # Get the parent item
            parent_item = item.parent()

            # Get the grandparent item (mib_item)
            if parent_item:
                item_type = "group"
                module_name = parent_item.text()
                grandparent_item = parent_item.parent()
                group_name = parent_item.data()
                if grandparent_item:
                    item_type = "object"
                    module_name = grandparent_item.text()

            self.updateDetailInfo(item_type, module_name, item_name, group_name)
        return
    def showSnmpRequestDialog(self):
        snmp_request_window = SNMPRequestDialog()
        oid = self.ui.lineEdit_OID.text()
        snmp_request_window.setInfos(self.snmp_ip_address, oid, self.snmp_community)
        if snmp_request_window.exec() == QDialog.Accepted :
            self.snmp_ip_address = snmp_request_window.getIPAddress()
            self.snmp_community = snmp_request_window.getCommunity()
            pass
        return
