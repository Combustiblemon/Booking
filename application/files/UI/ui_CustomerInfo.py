from PySide6.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy, QGridLayout, QFrame, QPushButton, QLabel


class Ui_CustomerInfo(object):
    def setupUi(self, CustomerInfo):
        if not CustomerInfo.objectName():
            CustomerInfo.setObjectName(u"CustomerInfo")
        CustomerInfo.resize(355, 594)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CustomerInfo.sizePolicy().hasHeightForWidth())
        CustomerInfo.setSizePolicy(sizePolicy)
        CustomerInfo.setFocusPolicy(Qt.StrongFocus)
        CustomerInfo.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout = QGridLayout(CustomerInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.OKButton = QPushButton(CustomerInfo)
        self.OKButton.setObjectName(u"OKButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.OKButton.sizePolicy().hasHeightForWidth())
        self.OKButton.setSizePolicy(sizePolicy1)
        self.OKButton.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.OKButton, 2, 1, 1, 1, Qt.AlignRight)

        self.editButton = QPushButton(CustomerInfo)
        self.editButton.setObjectName(u"editButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(20)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy2)
        self.editButton.setMinimumSize(QSize(100, 0))
        self.editButton.setBaseSize(QSize(0, 0))

        self.gridLayout.addWidget(self.editButton, 2, 0, 1, 1, Qt.AlignLeft)

        self.textLabel = QLabel(CustomerInfo)
        self.textLabel.setObjectName(u"textLabel")
        font = QFont()
        font.setPointSize(12)
        self.textLabel.setFont(font)
        self.textLabel.setAutoFillBackground(False)
        self.textLabel.setStyleSheet(u"QLabel { background-color : white; }")
        self.textLabel.setFrameShape(QFrame.StyledPanel)
        self.textLabel.setFrameShadow(QFrame.Plain)
        self.textLabel.setTextFormat(Qt.RichText)
        self.textLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.textLabel.setWordWrap(True)
        self.textLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.textLabel, 0, 0, 1, 2)


        self.retranslateUi(CustomerInfo)

        QMetaObject.connectSlotsByName(CustomerInfo)
    # setupUi

    def retranslateUi(self, CustomerInfo):
        CustomerInfo.setWindowTitle(QCoreApplication.translate("CustomerInfo", u"\u03a0\u03bb\u03b7\u03c1\u03bf\u03c6\u03bf\u03c1\u03af\u03b5\u03c2 \u03c0\u03b5\u03bb\u03ac\u03c4\u03b7", None))
        self.OKButton.setText(QCoreApplication.translate("CustomerInfo", u"OK", None))
        self.editButton.setText(QCoreApplication.translate("CustomerInfo", u"\u0395\u03c0\u03b5\u03be\u03b5\u03c1\u03b3\u03b1\u03c3\u03af\u03b1", None))
        self.textLabel.setText("")
    # retranslateUi

