from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QWidget)
from .custom_line_edit import CustomLineEdit
from .custom_button import CustomButton
from .custom_spinbox import CustomSpinBox
from .custom_combobox import CustomComboBox
from Modules.common import *

class Ui_DialogPingCheck(object):
    def setupUi(self, DialogPingCheck):
        if not DialogPingCheck.objectName():
            DialogPingCheck.setObjectName(u"DialogPingCheck")
        DialogPingCheck.resize(430, 305)
        DialogPingCheck.setMinimumSize(QSize(430, 305))
        DialogPingCheck.setMaximumSize(QSize(430, 305))

        DialogPingCheck.setWindowIcon(QIcon(resource_path("res/Icons_tools.png")))

        # Check Name
        font = QFont()
        font.setPointSize(12)
        DialogPingCheck.setFont(font)
        self.label_user_name = QLabel(DialogPingCheck)
        self.label_user_name.setObjectName(u"label_user_name")
        self.label_user_name.setGeometry(QRect(25, 20, 130, 30))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.label_user_name.setFont(font1)
        self.label_user_name.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.lineEdit_user_name = CustomLineEdit(DialogPingCheck, "15px")
        self.lineEdit_user_name.setObjectName(u"lineEdit_user_name")
        self.lineEdit_user_name.setGeometry(QRect(170, 20, 240, 30))       
        # Check Type
        self.label_check_type = QLabel(DialogPingCheck)
        self.label_check_type.setObjectName(u"label_check_type")
        self.label_check_type.setGeometry(QRect(25, 55, 130, 30))
        self.label_check_type.setFont(font1)
        self.label_check_type.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.comboBox_check_type = CustomComboBox(DialogPingCheck, resource_path("res/arrow_down.png"))
        self.comboBox_check_type.setObjectName(u"comboBox_check_type")
        self.comboBox_check_type.setGeometry(QRect(170, 55, 240, 30))
        # Destination Ip        
        self.label_ip_address = QLabel(DialogPingCheck)
        self.label_ip_address.setObjectName(u"label_ip_address")
        self.label_ip_address.setGeometry(QRect(25, 90, 130, 30))
        self.label_ip_address.setFont(font1)
        self.label_ip_address.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.lineEdit_ip_address = CustomLineEdit(DialogPingCheck, "15px")
        self.lineEdit_ip_address.setObjectName(u"lineEdit_ip_address")
        self.lineEdit_ip_address.setGeometry(QRect(170, 90, 240, 30))        
        # Pings per check
        self.label_repeat = QLabel(DialogPingCheck)
        self.label_repeat.setObjectName(u"label_repeat")
        self.label_repeat.setGeometry(QRect(25, 125, 130, 30))
        self.label_repeat.setFont(font1)
        self.label_repeat.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.spinBox_repeat = CustomSpinBox(DialogPingCheck, resource_path("res/arrow_up.png"), resource_path("res/arrow_down.png"))
        self.spinBox_repeat.setObjectName(u"spinBox_repeat")
        self.spinBox_repeat.setGeometry(QRect(170, 125, 110, 30))
        self.spinBox_repeat.setMinimum(1)
        self.spinBox_repeat.setMaximum(999)
        # Timeout
        self.label_timeout = QLabel(DialogPingCheck)
        self.label_timeout.setObjectName(u"label_timeout")
        self.label_timeout.setGeometry(QRect(25, 160, 130, 30))
        self.label_timeout.setFont(font1)
        self.label_timeout.setStyleSheet(u"color: rgb(4, 7, 15);")

        self.spinBox_timeout = CustomSpinBox(DialogPingCheck, resource_path("res/arrow_up.png"), resource_path("res/arrow_down.png"))
        self.spinBox_timeout.setObjectName(u"spinBox_timeout")
        self.spinBox_timeout.setGeometry(QRect(170, 160, 110, 30))
        self.spinBox_timeout.setMinimum(1)
        self.spinBox_timeout.setMaximum(999)
        # Interval
        self.label_interval = QLabel(DialogPingCheck)
        self.label_interval.setObjectName(u"label_interval")
        self.label_interval.setGeometry(QRect(25, 195, 130, 30))
        self.label_interval.setFont(font1)
        self.label_interval.setStyleSheet(u"color: rgb(4, 7, 15);")
        
        self.spinBox_interval = CustomSpinBox(DialogPingCheck, resource_path("res/arrow_up.png"), resource_path("res/arrow_down.png"))
        self.spinBox_interval.setObjectName(u"spinBox_interval")
        self.spinBox_interval.setGeometry(QRect(170, 195, 110, 30))
        self.spinBox_interval.setMinimum(1)
        self.spinBox_interval.setMaximum(999)    
        # Add Button
        self.pushButton_Add = CustomButton(DialogPingCheck, "Add",resource_path("res/Icons_add.png"),"rgb(72, 69, 228)","rgb(72, 69, 228)","rgb(255,255,255)", 0.7, 0.9, 78)
        self.pushButton_Add.setObjectName(u"pushButton_Add")
        self.pushButton_Add.setGeometry(QRect(330, 245, 78, 42))
        # View Button    
        self.pushButton_View = CustomButton(DialogPingCheck, "View",resource_path("res/Icons_view.png"),"rgb(255,255,255)","rgb(72, 69, 228)","rgb(72, 69, 228)", 0.1, 0.3, 85)
        self.pushButton_View.setObjectName(u"pushButton_View")
        self.pushButton_View.setGeometry(QRect(240, 245, 85, 42))    
        
        self.retranslateUi(DialogPingCheck)

        QMetaObject.connectSlotsByName(DialogPingCheck)
    # setupUi

    def retranslateUi(self, DialogPingCheck):
        DialogPingCheck.setWindowTitle(QCoreApplication.translate("DialogPingCheck", u"Ping check setting", None))
        self.label_user_name.setText(QCoreApplication.translate("DialogPingCheck", u"Check name", None))
        self.lineEdit_user_name.setPlaceholderText("")
        self.label_check_type.setText(QCoreApplication.translate("DialogPingCheck", u"Ping Type", None))
        self.lineEdit_ip_address.setText("")
        self.lineEdit_ip_address.setPlaceholderText("")
        self.label_ip_address.setText(QCoreApplication.translate("DialogPingCheck", u"Destination IP", None))
        self.label_repeat.setText(QCoreApplication.translate("DialogPingCheck", u"Pings per check", None))
        self.label_timeout.setText(QCoreApplication.translate("DialogPingCheck", u"Timeout (seconds)", None))
        self.label_interval.setText(QCoreApplication.translate("DialogPingCheck", u"Interval (seconds)", None))
        self.spinBox_interval.setSpecialValueText("")
    # retranslateUi

