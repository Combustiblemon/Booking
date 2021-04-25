from PySide6.QtCore import Qt, QMetaObject, QCoreApplication, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QGridLayout, QSpinBox, QAbstractSpinBox, QComboBox, QSizePolicy, QSpacerItem, QDialogButtonBox


class Ui_AddRoom(object):
    def setupUi(self, AddRoom):
        if not AddRoom.objectName():
            AddRoom.setObjectName(u"AddRoom")
        AddRoom.resize(296, 98)
        font = QFont()
        font.setPointSize(10)
        AddRoom.setFont(font)
        AddRoom.setFocusPolicy(Qt.StrongFocus)
        self.gridLayout = QGridLayout(AddRoom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.roomIDLabel = QLabel(AddRoom)
        self.roomIDLabel.setObjectName(u"roomIDLabel")

        self.gridLayout.addWidget(self.roomIDLabel, 0, 0, 1, 1)

        self.roomTypeLabel = QLabel(AddRoom)
        self.roomTypeLabel.setObjectName(u"roomTypeLabel")

        self.gridLayout.addWidget(self.roomTypeLabel, 0, 1, 1, 1)

        self.roomIDInput = QSpinBox(AddRoom)
        self.roomIDInput.setObjectName(u"roomIDInput")
        self.roomIDInput.setMinimumSize(QSize(110, 0))
        self.roomIDInput.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.roomIDInput.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.roomIDInput.setMaximum(99999)

        self.gridLayout.addWidget(self.roomIDInput, 1, 0, 1, 1)

        self.roomTypeInput = QComboBox(AddRoom)
        self.roomTypeInput.setObjectName(u"roomTypeInput")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roomTypeInput.sizePolicy().hasHeightForWidth())
        self.roomTypeInput.setSizePolicy(sizePolicy)
        self.roomTypeInput.setMinimumSize(QSize(155, 0))
        self.roomTypeInput.setFocusPolicy(Qt.NoFocus)

        self.gridLayout.addWidget(self.roomTypeInput, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(AddRoom)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

#if QT_CONFIG(shortcut)
        self.roomIDLabel.setBuddy(self.roomIDInput)
        self.roomTypeLabel.setBuddy(self.roomTypeInput)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(AddRoom)
        self.buttonBox.accepted.connect(AddRoom.accept)
        self.buttonBox.rejected.connect(AddRoom.reject)

        QMetaObject.connectSlotsByName(AddRoom)
    # setupUi

    def retranslateUi(self, AddRoom):
        AddRoom.setWindowTitle(QCoreApplication.translate("AddRoom", u"\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7 \u0394\u03c9\u03bc\u03b1\u03c4\u03af\u03bf\u03c5", None))
        self.roomIDLabel.setText(QCoreApplication.translate("AddRoom", u"\u0391\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u03b4\u03c9\u03bc\u03b1\u03c4\u03af\u03bf\u03c5:", None))
        self.roomTypeLabel.setText(QCoreApplication.translate("AddRoom", u"\u03a4\u03cd\u03c0\u03bf\u03c2 \u03b4\u03c9\u03bc\u03b1\u03c4\u03af\u03bf\u03c5:", None))
    # retranslateUi

