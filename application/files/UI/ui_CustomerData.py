from PySide6.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy, QGridLayout, QComboBox, QDateEdit, QSpacerItem, QSpinBox, QAbstractSpinBox, QLabel, QLineEdit, QDialogButtonBox, QDoubleSpinBox, QTextEdit


class Ui_CustomerData(object):
    def setupUi(self, CustomerData):
        if not CustomerData.objectName():
            CustomerData.setObjectName(u"CustomerData")
        CustomerData.resize(615, 272)
        font = QFont()
        font.setPointSize(10)
        CustomerData.setFont(font)
        CustomerData.setFocusPolicy(Qt.StrongFocus)
        CustomerData.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout = QGridLayout(CustomerData)
        self.gridLayout.setObjectName(u"gridLayout")
        self.zhorizontalSpacer_4 = QSpacerItem(45, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer_4, 3, 3, 1, 1)

        self.peopleInput = QSpinBox(CustomerData)
        self.peopleInput.setObjectName(u"peopleInput")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peopleInput.sizePolicy().hasHeightForWidth())
        self.peopleInput.setSizePolicy(sizePolicy)
        self.peopleInput.setFocusPolicy(Qt.ClickFocus)
        self.peopleInput.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.peopleInput.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.peopleInput.setMaximum(99999)

        self.gridLayout.addWidget(self.peopleInput, 1, 4, 1, 1)

        self.zhorizontalSpacer_5 = QSpacerItem(45, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer_5, 1, 5, 1, 1)

        self.bookingTypeLabel = QLabel(CustomerData)
        self.bookingTypeLabel.setObjectName(u"bookingTypeLabel")

        self.gridLayout.addWidget(self.bookingTypeLabel, 2, 6, 1, 1)

        self.nameLabel = QLabel(CustomerData)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 2)

        self.roomIDInput = QSpinBox(CustomerData)
        self.roomIDInput.setObjectName(u"roomIDInput")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.roomIDInput.sizePolicy().hasHeightForWidth())
        self.roomIDInput.setSizePolicy(sizePolicy1)
        self.roomIDInput.setMinimumSize(QSize(110, 0))
        self.roomIDInput.setFocusPolicy(Qt.ClickFocus)
        self.roomIDInput.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.roomIDInput.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.roomIDInput.setMaximum(999999999)

        self.gridLayout.addWidget(self.roomIDInput, 1, 6, 1, 1)

        self.checkOutLabel = QLabel(CustomerData)
        self.checkOutLabel.setObjectName(u"checkOutLabel")

        self.gridLayout.addWidget(self.checkOutLabel, 2, 2, 1, 1)

        self.bookingTypeInput = QComboBox(CustomerData)
        self.bookingTypeInput.setObjectName(u"bookingTypeInput")
        self.bookingTypeInput.setFocusPolicy(Qt.ClickFocus)

        self.gridLayout.addWidget(self.bookingTypeInput, 3, 6, 1, 1)

        self.nameInput = QLineEdit(CustomerData)
        self.nameInput.setObjectName(u"nameInput")
        sizePolicy.setHeightForWidth(self.nameInput.sizePolicy().hasHeightForWidth())
        self.nameInput.setSizePolicy(sizePolicy)
        self.nameInput.setMinimumSize(QSize(200, 0))
        self.nameInput.setSizeIncrement(QSize(100, 0))
        self.nameInput.setBaseSize(QSize(0, 0))
        self.nameInput.setFocusPolicy(Qt.ClickFocus)
        self.nameInput.setInputMethodHints(Qt.ImhNone)

        self.gridLayout.addWidget(self.nameInput, 1, 0, 1, 3)

        self.checkInLabel = QLabel(CustomerData)
        self.checkInLabel.setObjectName(u"checkInLabel")

        self.gridLayout.addWidget(self.checkInLabel, 2, 0, 1, 1)

        self.zhorizontalSpacer_6 = QSpacerItem(0, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer_6, 1, 7, 1, 1)

        self.checkInInput = QDateEdit(CustomerData)
        self.checkInInput.setObjectName(u"checkInInput")
        sizePolicy1.setHeightForWidth(self.checkInInput.sizePolicy().hasHeightForWidth())
        self.checkInInput.setSizePolicy(sizePolicy1)
        self.checkInInput.setFocusPolicy(Qt.ClickFocus)
        self.checkInInput.setCalendarPopup(True)

        self.gridLayout.addWidget(self.checkInInput, 3, 0, 1, 1)

        self.zverticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.zverticalSpacer, 10, 3, 1, 1)

        self.commentLabel = QLabel(CustomerData)
        self.commentLabel.setObjectName(u"commentLabel")

        self.gridLayout.addWidget(self.commentLabel, 6, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(CustomerData)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy1.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy1)
        self.buttonBox.setMinimumSize(QSize(0, 0))
        self.buttonBox.setSizeIncrement(QSize(0, 0))
        self.buttonBox.setFocusPolicy(Qt.StrongFocus)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 10, 6, 1, 1)

        self.zhorizontalSpacer_2 = QSpacerItem(45, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer_2, 1, 3, 1, 1)

        self.checkOutInput = QDateEdit(CustomerData)
        self.checkOutInput.setObjectName(u"checkOutInput")
        self.checkOutInput.setFocusPolicy(Qt.ClickFocus)
        self.checkOutInput.setCalendarPopup(True)

        self.gridLayout.addWidget(self.checkOutInput, 3, 2, 1, 1)

        self.peopleLabel = QLabel(CustomerData)
        self.peopleLabel.setObjectName(u"peopleLabel")

        self.gridLayout.addWidget(self.peopleLabel, 0, 4, 1, 1)

        self.zhorizontalSpacer = QSpacerItem(45, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer, 3, 5, 1, 1)

        self.zhorizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.zhorizontalSpacer_3, 3, 1, 1, 1)

        self.pricePerNightInput = QDoubleSpinBox(CustomerData)
        self.pricePerNightInput.setObjectName(u"pricePerNightInput")
        sizePolicy.setHeightForWidth(self.pricePerNightInput.sizePolicy().hasHeightForWidth())
        self.pricePerNightInput.setSizePolicy(sizePolicy)
        self.pricePerNightInput.setFocusPolicy(Qt.ClickFocus)
        self.pricePerNightInput.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.pricePerNightInput.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pricePerNightInput.setMaximum(99999999999.990005493164063)

        self.gridLayout.addWidget(self.pricePerNightInput, 3, 4, 1, 1)

        self.pricePerNightLabel = QLabel(CustomerData)
        self.pricePerNightLabel.setObjectName(u"pricePerNightLabel")

        self.gridLayout.addWidget(self.pricePerNightLabel, 2, 4, 1, 1)

        self.roomIDLabel = QLabel(CustomerData)
        self.roomIDLabel.setObjectName(u"roomIDLabel")

        self.gridLayout.addWidget(self.roomIDLabel, 0, 6, 1, 1)

        self.commentInput = QTextEdit(CustomerData)
        self.commentInput.setObjectName(u"commentInput")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(10)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.commentInput.sizePolicy().hasHeightForWidth())
        self.commentInput.setSizePolicy(sizePolicy2)
        self.commentInput.setFocusPolicy(Qt.ClickFocus)
        self.commentInput.setAcceptRichText(False)

        self.gridLayout.addWidget(self.commentInput, 8, 0, 1, 7)

#if QT_CONFIG(shortcut)
        self.bookingTypeLabel.setBuddy(self.bookingTypeInput)
        self.nameLabel.setBuddy(self.nameInput)
        self.checkOutLabel.setBuddy(self.checkOutInput)
        self.checkInLabel.setBuddy(self.checkInInput)
        self.commentLabel.setBuddy(self.commentInput)
        self.peopleLabel.setBuddy(self.peopleInput)
        self.pricePerNightLabel.setBuddy(self.pricePerNightInput)
        self.roomIDLabel.setBuddy(self.roomIDInput)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(CustomerData)
        self.buttonBox.accepted.connect(CustomerData.accept)
        self.buttonBox.rejected.connect(CustomerData.reject)

        QMetaObject.connectSlotsByName(CustomerData)
    # setupUi

    def retranslateUi(self, CustomerData):
        CustomerData.setWindowTitle(QCoreApplication.translate("CustomerData", u"CustomerData", None))
        self.bookingTypeLabel.setText(QCoreApplication.translate("CustomerData", u"\u03a4\u03cd\u03c0\u03bf\u03c2 \u039a\u03c1\u03ac\u03c4\u03b7\u03c3\u03b7\u03c2:", None))
        self.nameLabel.setText(QCoreApplication.translate("CustomerData", u"\u038c\u03bd\u03bf\u03bc\u03b1 \u03ba\u03c1\u03ac\u03c4\u03b7\u03c3\u03b7\u03c2:", None))
        self.checkOutLabel.setText(QCoreApplication.translate("CustomerData", u"Check Out:", None))
        self.checkInLabel.setText(QCoreApplication.translate("CustomerData", u"Check In:", None))
        self.commentLabel.setText(QCoreApplication.translate("CustomerData", u"\u03a3\u03c7\u03cc\u03bb\u03b9\u03b1:", None))
        self.peopleLabel.setText(QCoreApplication.translate("CustomerData", u"\u0391\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u03b1\u03c4\u03cc\u03bc\u03c9\u03bd:", None))
        self.pricePerNightLabel.setText(QCoreApplication.translate("CustomerData", u"\u03a4\u03b9\u03bc\u03ae \u03b1\u03bd\u03ac \u03b2\u03c1\u03ac\u03b4\u03c5:", None))
        self.roomIDLabel.setText(QCoreApplication.translate("CustomerData", u"\u0391\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u03b4\u03c9\u03bc\u03b1\u03c4\u03af\u03bf\u03c5:", None))
    # retranslateUi

