from PySide6.QtCore import Qt, QMetaObject, QCoreApplication
from PySide6.QtWidgets import QListWidget, QGridLayout, QAbstractItemView, QDialogButtonBox


class Ui_DeleteRoom(object):
    def setupUi(self, DeleteRoom):
        if not DeleteRoom.objectName():
            DeleteRoom.setObjectName(u"DeleteRoom")
        DeleteRoom.resize(219, 457)
        self.gridLayout = QGridLayout(DeleteRoom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(DeleteRoom)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAutoScroll(False)
        self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DeleteRoom)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFocusPolicy(Qt.StrongFocus)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(DeleteRoom)
        self.buttonBox.accepted.connect(DeleteRoom.accept)
        self.buttonBox.rejected.connect(DeleteRoom.reject)

        QMetaObject.connectSlotsByName(DeleteRoom)
    # setupUi

    def retranslateUi(self, DeleteRoom):
        DeleteRoom.setWindowTitle(QCoreApplication.translate("DeleteRoom", u"\u0394\u03b9\u03b1\u03b3\u03c1\u03b1\u03c6\u03ae \u03b4\u03c9\u03bc\u03b1\u03c4\u03af\u03bf\u03c5", None))
    # retranslateUi

