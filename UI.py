from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QColor
from PyQt5.uic import uiparser
from datetime import datetime, date, timedelta
from Customer import Customer
import platform
import DB
import os
import json


dictionary = {} 
with open('./files/data/dictionary.json', 'r', encoding="utf8") as file:
    dictionary = json.load(file)
    
roomDictionary = {} 
with open('./files/data/roomDictionary.json', 'r', encoding="utf8") as file:
    roomDictionary = json.load(file)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, months):
        super(MainWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/MainWindow.ui', self)
        self.months = months
        self.ConnectLogicToObjects()
        
    # Adding pointers to all the objects of the UI
    def ConnectLogicToObjects(self):
        self.centralWidget().layout().setContentsMargins(10, 10, 10, 10)
        
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.tableWidget.cellDoubleClicked.connect(self.cellDoubleClicked)
        self.SetTableStyle()
        
        self.monthSelection = self.findChild(QtWidgets.QComboBox, 'monthSelection')
        self.monthSelection.setCurrentIndex(int(datetime.today().strftime('%m')) - 1)
        
        self.yearSelection = self.findChild(QtWidgets.QDateEdit, 'yearSelection')
        self.yearSelection.setDate(datetime.today())
        
        self.showButton = self.findChild(QtWidgets.QPushButton, 'showButton')
        self.showButton.clicked.connect(self.UpdateTableData)
        
        self.addBooking = self.findChild(QtWidgets.QPushButton, 'addBooking')
        self.addBooking.clicked.connect(self.AddBookingClicked)
        
        self.deleteBooking = self.findChild(QtWidgets.QPushButton, 'deleteBooking')
        self.deleteBooking.clicked.connect(self.DeleteBookingPressed)
        
        self.roomTypeSelection = self.findChild(QtWidgets.QComboBox, 'roomTypeSelection')
        self.roomTypeSelection.addItems(roomDictionary.values())
        
    def SetTableStyle(self):
        OSVersion = f"{platform.system()} {platform.release()}"
        if OSVersion == "Windows 10":
            self.tableWidget.setStyleSheet("QHeaderView::section{"
                                           "border-top:0px solid #c8c8c8;"
                                           "border-left:0px solid #c8c8c8;"
                                           "border-right:2px solid #c8c8c8;"
                                           "border-bottom: 2px solid #c8c8c8;"
                                           "background-color:white;"
                                           "padding:4px;"
                                           "}"
                                           "QTableCornerButton::section{"
                                           "border-top:0px solid #c8c8c8;"
                                           "border-left:0px solid #c8c8c8;"
                                           "border-right:2px solid #c8c8c8;"
                                           "border-bottom: 2px solid #c8c8c8;"
                                           "background-color:white;"
                                           "}")
            
    # gets called whenever the combobox is changed
    def MonthChange(self):
        self.UpdateDates(self.months[f'{self.monthSelection.currentIndex() + 1}'])
        
    def UpdateDates(self, dateNumber):
        self.tableWidget.setColumnCount(dateNumber)
    
    def Test(self):
        model = self.tableWidget.model()

        print(model)
        
    def Test2(self):
        pass
        
    def cellDoubleClicked(self, e):
        print(e)