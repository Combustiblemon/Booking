from PySide6.QtCore import Qt,QMetaObject, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy, QGridLayout,QLabel, QDialogButtonBox


class Ui_ErrorWindow(object):
    def setupUi(self, ErrorWindow):
        if not ErrorWindow.objectName():
            ErrorWindow.setObjectName(u"ErrorWindow")
        ErrorWindow.resize(411, 123)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrorWindow.sizePolicy().hasHeightForWidth())
        ErrorWindow.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(ErrorWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(ErrorWindow)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setFocusPolicy(Qt.StrongFocus)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ErrorWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(ErrorWindow)
        self.buttonBox.accepted.connect(ErrorWindow.accept)
        self.buttonBox.rejected.connect(ErrorWindow.reject)

        QMetaObject.connectSlotsByName(ErrorWindow)
    # setupUi

    def retranslateUi(self, ErrorWindow):
        ErrorWindow.setWindowTitle(QCoreApplication.translate("ErrorWindow", u"Error", None))
        self.label.setText(QCoreApplication.translate("ErrorWindow", u"TextLabel", None))
    # retranslateUi

