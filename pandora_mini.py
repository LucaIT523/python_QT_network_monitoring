# This Python file uses the following encoding: utf-8
import sys
import datetime
from Modules.widget_mib_panel import MIBPanelWidget
from Modules.widget_monitoring_panel import MonitoringPanelWidget

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QDialog
from Forms.ui_form_main import Ui_MainWindow

class FreeNetworkTools(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)   
 
        self.ui.actionReset_MIBs.triggered.connect(self.resetMIBs)
        self.ui.actionImport_external_MIBs.triggered.connect(self.importMIBsDialog)
        self.ui.actionShow_loaded_MIBs.triggered.connect(self.showLoadedMIBsDialog) 
        self.ui.actionMIBs_Explorer.triggered.connect(self.showMIBsExplorerPanel) 
        self.ui.actionQuit.triggered.connect(self.close)       

        self.ui.actionMonitoring_Panel.triggered.connect(self.showMonitoringPanelWindow)
        self.ui.actionPing.triggered.connect(self.showPingCheckDialog)
        self.ui.actionSNMP_get.triggered.connect(self.showSNMPCheckDialog)
        self.ui.actionTCP_check.triggered.connect(self.showTCPCheckDialog)
        self.ui.actionPacket_loss.triggered.connect(lambda: self.showPingOtherCheckDialog("Packetloss"))
        self.ui.actionJitter.triggered.connect(lambda: self.showPingOtherCheckDialog("Jitter"))
        self.ui.actionWeb.triggered.connect(self.showWebCheckDialog)
        self.ui.actionEvent_console.triggered.connect(self.showEventConsoleDialog)
        
        self.ui.actionIP_calculator.triggered.connect(self.showIPCalculatorDialog)
        self.ui.actionSLA_calculator.triggered.connect(self.showSLACalculatorDialog)
        self.ui.actionWhois.triggered.connect(self.showWhoisDialog)
        self.ui.actionTraceroute.triggered.connect(self.showTracerouteDialog)
        
        self.ui.actionHelp.triggered.connect(self.showSplashDialog)


        self.mib_panel_widget = MIBPanelWidget()
        self.monitoring_panel_widget = MonitoringPanelWidget()

        self.ui.stackedWidget.addWidget(self.mib_panel_widget)
        self.ui.stackedWidget.addWidget(self.monitoring_panel_widget)
        self.ui.stackedWidget.setCurrentIndex(1)         

        return         

    def closeEvent(self, event):
        if self.monitoring_panel_widget:
            self.monitoring_panel_widget.close()
        # Log application shutdown event
        from Modules.sql_manager import add_event
        date_closed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_event("Pandora MINI shutting down", date_closed)
        event.accept()
        return
    ###################################### MIB
    def resetMIBs(self):
        self.mib_panel_widget.resetMIBs()
        return    
    def importMIBsDialog(self):
        try:
            file_names, _ = QFileDialog.getOpenFileNames(
                           self,
                           "Open MIB Files",
                           "",
                           "MIB Files (*.mib *.my *.txt);;MIB File (*.mib);;MY File (*.my);;All Files (*)"
                       )
            if file_names:       
                self.mib_panel_widget.missingMIBsClear()         
                for file_name in file_names:
                    self.mib_panel_widget.loadingMIB(file_name)
                missing_mibs = self.mib_panel_widget.getMissingMIBs()
                if missing_mibs:
                    results = ""
                    for key, values in missing_mibs.items():
                        results += f"{key} Loading Failed: "
                        results += ", ".join(f"{value} Missing" for value in values)
                        results += "\n"
                    QMessageBox.warning(self, "MIB File Loading Errors", f"{results}")
        except Exception as e:
            print(f"   --- Exception[QFileDialog] Error: {e}")
        return   
    def showLoadedMIBsDialog(self):
        # Show loaded MIBs in a list dialog
        from Modules.dialog_loaded_mibs import LoadedMIBsDialog
        loaded_mibs = self.mib_panel_widget.getLoadedMIBs()
        dialog = LoadedMIBsDialog(self, loaded_mibs)
        dialog.exec()
        return  
    def showMIBsExplorerPanel(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        return
    ###################################### Monitoring
    def showMonitoringPanelWindow(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        return
    def showPingCheckDialog(self):
        from Modules.dialog_ping_check import PingCheckDialog
        ping_check_dialog = PingCheckDialog()
        ping_check_dialog.addCheckSignal.connect(self.addCheckMonitoring)
        if ping_check_dialog.exec() == QDialog.Accepted:
            self.showMonitoringPanelWindow()
        return
    def showSNMPCheckDialog(self):
        from Modules.dialog_snmp_check import SNMPCheckDialog
        snmp_check_dialog = SNMPCheckDialog()
        snmp_check_dialog.addCheckSignal.connect(self.addCheckMonitoring)
        if snmp_check_dialog.exec() == QDialog.Accepted:
            self.showMonitoringPanelWindow()
        return
    def showTCPCheckDialog(self):
        from Modules.dialog_tcp_check import TCPCheckDialog
        tcp_check_dialog = TCPCheckDialog()
        tcp_check_dialog.addCheckSignal.connect(self.addCheckMonitoring)
        if tcp_check_dialog.exec() == QDialog.Accepted:
            self.showMonitoringPanelWindow()
        return
    def showPingOtherCheckDialog(self, type = "Packetloss"):
        from Modules.dialog_ping_others_check import PingOtherCheckDialog
        ping_other_check_dialog = PingOtherCheckDialog(type=type)
        ping_other_check_dialog.addCheckSignal.connect(self.addCheckMonitoring)
        if ping_other_check_dialog.exec() == QDialog.Accepted:
            self.showMonitoringPanelWindow()
        return
    def addCheckMonitoring(self, check_info):
        if self.monitoring_panel_widget.addCheckMonitoring(check_info) == False:
            QMessageBox.warning(self, "Monitoring Selecting Error", f"This monitoring already exists. \n Please re-enter it and add it.")
        return  
    def showWebCheckDialog(self):
        from Modules.dialog_web_check import WebCheckDialog
        web_check_dialog = WebCheckDialog()
        web_check_dialog.addCheckSignal.connect(self.addCheckMonitoring)
        if web_check_dialog.exec() == QDialog.Accepted:
            self.showMonitoringPanelWindow()
        return
    def showEventConsoleDialog(self):
        from Modules.dialog_event_console import EventConsoleDialog
        event_console_dialog = EventConsoleDialog()
        event_console_dialog.show()
        return
    ###################################### Tools
    def showIPCalculatorDialog(self):
        from Modules.dialog_ip_calculator import IPCalculator
        ip_calculator_dialog = IPCalculator()
        ip_calculator_dialog.exec()
    def showSLACalculatorDialog(self):
        from Modules.dialog_sla_calculator import SLACalculator
        sla_calculator_dialog = SLACalculator()
        sla_calculator_dialog.exec()
    def showWhoisDialog(self):
        from Modules.dialog_whois import WhoisDialog
        whois_dialog = WhoisDialog()
        whois_dialog.exec()
    def showTracerouteDialog(self):
        from Modules.dialog_tracerounte import TracerouteDialog
        traceroute_dialog = TracerouteDialog()
        traceroute_dialog.exec()
    ######################################   Help
    def showSplashDialog(self):
        from Modules.dialog_splash import Splash
        splash_dialog =  Splash()
        splash_dialog.exec()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    date_started = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    
    from Modules.dialog_splash import Splash
    splash = Splash()
    splash.show()

    widget = FreeNetworkTools()
    def show_main_dialog():
        from Modules.sql_manager import init_database, add_event, clean_old_events
        init_database()
        add_event("Pandora MINI startup", date_started)
        clean_old_events()
        widget.show()
    
    splash.finished.connect(show_main_dialog)
    sys.exit(app.exec())
