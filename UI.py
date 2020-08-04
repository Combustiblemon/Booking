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
        self.UpdateTableData()
        
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
            
    def UpdateTableData(self):
        # Create connection to database
        conn = DB.CreateConnection()
        # get the customer data for the current month
        data = DB.GetCustomersByMonth(conn, self.monthSelection.currentIndex() + 1, self.yearSelection.date().year(), self.roomTypeSelection.currentIndex())
        
        #
        if self.roomTypeSelection.currentIndex() == 0:
            rowNumber = DB.GetRoomNumber(conn)
        else:
            rowNumber = DB.GetRoomNumber(conn, self.roomTypeSelection.currentIndex())
        
        
        # set the number of rows based on the selected roomtype
        self.tableWidget.setRowCount(0)
        
        # get the rooms based on the room type
        rooms = DB.GetRoomsByType(conn, self.roomTypeSelection.currentIndex())
        conn.close()
        
        # set up the table rows
        for item in rooms:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setVerticalHeaderItem(rowPosition, QtWidgets.QTableWidgetItem(str(item)))
        
        # set the number of columns based on the selected month
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setColumnCount(self.months[f'{self.monthSelection.currentIndex() + 1}'])
        
        
        for item in data:
            row = rooms.index(item.RoomID)  # find the row by searching the room list
            column = item.CheckIn.day  # starting column is the check in day
            span = item.NumberOfStayNights  # how many cells to merge based on the stay days
            if item.CheckIn.month < (self.monthSelection.currentIndex() + 1):  # if the CheckIn date is on a previous month calculate difference
                column = 0
                delta = -(item.CheckIn - date(self.yearSelection.date().year(), self.monthSelection.currentIndex() + 1, 1))
                span = item.NumberOfStayNights - delta.days + 1  # set span to difference
            
            self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(f'"{item.Name}" Άτομα: {item.People} Τιμή ανά βράδυ: {item.PricePerNight}'))
            temp = self.tableWidget.item(row, column)  # access the item just created
            temp.setBackground(QColor(dictionary[f"{item.BookingType}"][1][0], dictionary[f"{item.BookingType}"][1][1], dictionary[f"{item.BookingType}"][1][2], alpha=150))  # set the background color of the item based on the dictionary
            temp.setData(1, item.CustomerID)  # set the metadata of the item to the CustomerID
            self.tableWidget.setSpan(row, column, 1, span)  # merge the cells
        
        del data  # clean up memory by deleting the customer data from memory
        
            
class CustomerInfoWindow(QtWidgets.QDialog):
    def __init__(self, customerInfo):
        super(CustomerInfoWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/CustomerInfo.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.edited = None
        
        self.ConnectLogicToObjects(customerInfo)
        
    def ConnectLogicToObjects(self, customerInfo):
        self.textLabel = self.findChild(QtWidgets.QLabel, 'textLabel')
        self.SetLabelText(customerInfo)
        
        self.OKButton = self.findChild(QtWidgets.QPushButton, 'OKButton')
        self.OKButton.clicked.connect(self.OKClicked)
        
        self.editButton = self.findChild(QtWidgets.QPushButton, 'editButton')
        self.editButton.clicked.connect(lambda EditInfo: self.EditInfo(customerInfo))
        
    def SetLabelText(self, customerInfo):
        text = f"""<p><b>Όνομα κράτησης:</b> {customerInfo.Name}</p>
                <p>     <b>Αριθμός ατόμων:</b> {customerInfo.People}</p>
                <p>     <b>Check in:</b>  {customerInfo.CheckIn}</p>
                <p>     <b>Check out:</b> {customerInfo.CheckOut}</p>
                <p>     <b>Διανυκτερεύσεις:</b> {customerInfo.NumberOfStayNights}</p>
                <p>     <b>Τιμή ανά βράδυ:</b> {customerInfo.PricePerNight}€</p>
                <p>     <b>Σύνολο:</b> {customerInfo.TotalPrice}€</p>
                <p>     <b>Δωμάτιο:</b> {customerInfo.RoomID} ({self.GetRoomType(customerInfo.RoomID)})</p>
                <p>     <b>Κράτηση από:</b> {dictionary[f"{customerInfo.BookingType}"][0]}</p>
                
                <p>     <b>Σχόλια:</b> {customerInfo.Comments}</p>"""
        
        self.textLabel.setText(text)        
        
    def EditInfo(self, customerInfo):
        window = CustomerDataWindow(customerInfo=customerInfo)
        data = window.GetData()
        
        try:
            if data != customerInfo:  # if the data from the edit window are different from before, update the database and set the edited flag to 1
                self.SetLabelText(data)
                conn = DB.CreateConnection()
                DB.UpdateCustomer(conn, customerInfo.CustomerID, data)
                conn.close()
                self.edited = 1
        except AttributeError as e:
            return
        
    def OKClicked(self):
        self.close()
    
    def GetRoomType(self, roomID):
        conn = DB.CreateConnection()
        return roomDictionary[f'{DB.GetRoomType(conn, roomID)}']
        conn.close()
        
    def exec___(self):
        temp = self.exec_()
        return self.edited
        
