from PySide6.QtCore import Qt, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLabel 
 
class Ui_LoadingWindow(object): 
    def setupUi(self, LoadingWindow): 
        if not LoadingWindow.objectName(): 
            LoadingWindow.setObjectName("LoadingWindow") 
        LoadingWindow.resize(325, 42) 
        self.gridLayout = QGridLayout(LoadingWindow) 
        self.gridLayout.setObjectName("gridLayout") 
        self.label = QLabel(LoadingWindow) 
        self.label.setObjectName("label") 
        font = QFont() 
        font.setFamily("Arial") 
        font.setPointSize(16) 
        self.label.setFont(font) 
        self.label.setAlignment(Qt.AlignCenter) 
 
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1) 
 
 
        self.retranslateUi(LoadingWindow)

        QMetaObject.connectSlotsByName(LoadingWindow)
    # setupUi
    
    def retranslateUi(self, LoadingWindow):
        LoadingWindow.setWindowTitle(QCoreApplication.translate("LoadingWindow", "\u039a\u03c1\u03b1\u03c4\u03ae\u03c3\u03b5\u03b9\u03c2", None))
        self.label.setText(QCoreApplication.translate("LoadingWindow", "\u03a6\u03cc\u03c1\u03c4\u03c9\u03c3\u03b7 \u03c0\u03c1\u03bf\u03b3\u03c1\u03ac\u03bc\u03bc\u03b1\u03c4\u03bf\u03c2", None))
    # retranslateUi