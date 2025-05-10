from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QWidget)
from .custom_line_edit import CustomLineEdit
from .custom_combobox import CustomComboBox
from Modules.common import *
from Forms.custom_button import CustomButton

class Ui_DialogIPCalculator(object):
    def setupUi(self, DialogIPCalculator):
        if not DialogIPCalculator.objectName():
            DialogIPCalculator.setObjectName(u"DialogIPCalculator")
        DialogIPCalculator.resize(640, 430)
        DialogIPCalculator.setMinimumSize(QSize(640, 430))
        DialogIPCalculator.setMaximumSize(QSize(640, 430))

        DialogIPCalculator.setWindowIcon(QIcon(resource_path("res/Icons_tools.png")))
        # Ip Address
        font = QFont()
        font.setPointSize(12)
        DialogIPCalculator.setFont(font)
        self.label_ip_address = QLabel(DialogIPCalculator)
        self.label_ip_address.setObjectName(u"label_ip_address")
        self.label_ip_address.setGeometry(QRect(25, 20, 150, 30))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.label_ip_address.setFont(font1)
        self.label_ip_address.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.lineEdit_ip_address = CustomLineEdit(DialogIPCalculator, "15px")
        self.lineEdit_ip_address.setObjectName(u"lineEdit_ip_address")
        self.lineEdit_ip_address.setGeometry(QRect(170, 20, 450, 30))
        # Subnet Mask
        self.label_SubnetMask = QLabel(DialogIPCalculator)
        self.label_SubnetMask.setObjectName(u"label_SubnetMask")
        self.label_SubnetMask.setGeometry(QRect(25, 55, 140, 30))
        self.label_SubnetMask.setFont(font1)
        self.label_SubnetMask.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.lineEdit_SubnetMask = CustomLineEdit(DialogIPCalculator, "15px")
        self.lineEdit_SubnetMask.setObjectName(u"lineEdit_SubnetMask")
        self.lineEdit_SubnetMask.setGeometry(QRect(170, 55, 190, 30))
        # Ip Version
        self.comboBox_IPVersion = CustomComboBox(DialogIPCalculator, resource_path("res/arrow_down.png"))
        self.comboBox_IPVersion.setObjectName(u"comboBox_IPVersion")
        self.comboBox_IPVersion.setGeometry(QRect(380, 55, 100, 30))

        # Calculate Button
        self.pushButton_Calculate = CustomButton(DialogIPCalculator, text="Calculate", background_color="rgb(72, 69, 228)", border_color="rgb(72, 69, 228)", height=30, width=120, radius="5px")
        self.pushButton_Calculate.setObjectName(u"pushButton_Calculate")
        self.pushButton_Calculate.setGeometry(QRect(500, 55, 120, 30))
        # Result
        self.label_Result = QLabel(DialogIPCalculator)
        self.label_Result.setObjectName(u"label_Result")
        self.label_Result.setGeometry(QRect(200, 90, 270, 30))
        self.label_Result.setMinimumSize(QSize(270, 30))
        self.label_Result.setMaximumSize(QSize(270, 30))
        self.label_Result.setFont(font1)
        self.label_Result.setStyleSheet(u"color: rgb(4, 7, 15);")
        self.label_Result.setAlignment(Qt.AlignCenter)

        self.textEdit_Result = QTextEdit(DialogIPCalculator)
        self.textEdit_Result.setObjectName(u"textEdit_Result")
        self.textEdit_Result.setGeometry(QRect(25, 120, 590, 290))
        font4 = QFont()
        font4.setPointSize(9)
        self.textEdit_Result.setFont(font4)
        self.textEdit_Result.setStyleSheet(u"color: rgb(0, 0, 127);")
        self.textEdit_Result.setReadOnly(True)

        self.retranslateUi(DialogIPCalculator)

        QMetaObject.connectSlotsByName(DialogIPCalculator)
    # setupUi

    def retranslateUi(self, DialogIPCalculator):
        DialogIPCalculator.setWindowTitle(QCoreApplication.translate("DialogIPCalculator", u"IP Network Calculator Window", None))
        self.label_ip_address.setText(QCoreApplication.translate("DialogIPCalculator", u"IP Address", None))
        self.lineEdit_ip_address.setText("")
        self.lineEdit_ip_address.setPlaceholderText("")
        self.label_SubnetMask.setText(QCoreApplication.translate("DialogIPCalculator", u"Subnet Mask/Prefix", None))
        self.label_Result.setText(QCoreApplication.translate("DialogIPCalculator", u"IP Network Calculating Results", None))
        self.lineEdit_SubnetMask.setText("")
        self.lineEdit_SubnetMask.setPlaceholderText("")
    # retranslateUi

