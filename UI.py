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
        self.monthSelection.setCurrentIndex(datetime.today().month - 1)
        self.currentMonth = datetime.today().month - 1
        
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
        
        self.addRoom = self.findChild(QtWidgets.QAction, 'addRoom')
        self.addRoom.triggered.connect(self.addRoomPressed)
        
        self.removeRoom = self.findChild(QtWidgets.QAction, 'removeRoom')
        self.removeRoom.triggered.connect(self.removeRoomPressed)
        
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
        
        # get the rooms based on the room type
        rooms = DB.GetRoomsByType(conn, self.roomTypeSelection.currentIndex())
        
        #
        if self.roomTypeSelection.currentIndex() == 0:
            rowNumber = DB.GetRoomNumber(conn)
        else:
            rowNumber = DB.GetRoomNumber(conn, self.roomTypeSelection.currentIndex())
        conn.close()
        
        currentRow = self.tableWidget.currentRow()
        currentColumn = self.tableWidget.currentColumn()
        
        # set up the table rows
        try:
            # set the number of rows based on the selected roomtype
            self.tableWidget.setRowCount(0)
        
            for item in rooms:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setVerticalHeaderItem(rowPosition, QtWidgets.QTableWidgetItem(str(item)))
            
            self.tableWidget.setCurrentCell(currentRow, currentColumn)
        
            # set the number of columns based on the selected month
            if self.currentMonth != (self.monthSelection.currentIndex() + 1):
                self.tableWidget.setColumnCount(0)
                self.tableWidget.setColumnCount(self.months[f'{self.monthSelection.currentIndex() + 1}'])
                self.currentMonth = self.monthSelection.currentIndex() + 1
            
            
            for item in data:
                try:
                    row = rooms.index(item.RoomID)  # find the row by searching the room list
                    column = item.CheckIn.day - 1  # starting column is the check in day
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
                except ValueError:
                    pass
                    
            del data  # clean up memory by deleting the customer data from memory
        
        except TypeError:
            return
        
    def cellDoubleClicked(self, row, column):
        try:
            conn = DB.CreateConnection()
            CustomerInfo = DB.GetCustomerByID(conn, self.tableWidget.item(row, column).data(1))
            conn.close()
            
            window = CustomerInfoWindow(CustomerInfo)
            edited = window.exec___()
            
            if edited:
                conn = DB.CreateConnection()
                rooms = DB.GetRoomsByType(conn, self.roomTypeSelection.currentIndex())
                conn.close()
                self.UpdateTableData()
        except AttributeError:
            return
    
    def AddBookingClicked(self):
        window = CustomerDataWindow('Δεδομένα Κράτησης')
        data = window.GetData()
        
        if data:
            conn = DB.CreateConnection()
            occupiedDates = DB.GetRoomOccupiedDates(conn, data.RoomID, data.CheckIn.year)
            
            for item in occupiedDates:
                if not (((data.CheckIn - item[0]).days < 0 and (data.CheckOut - item[0]).days <= 0) or ((data.CheckIn - item[1]).days >= 0 and (data.CheckOut - item[1]).days > 0)):
                    conn.close()
                    MessageBox('Σφάλμα', f'<p style="text-align:center;font-size:18px"><b>Ουπς...</p><p style="font-size:18px">Οι ημερομηνίες <b>"{data.CheckIn} - {data.CheckOut}"</b> συμπίπτουν με άλλη κράτηση.</p>', QMessageBox.Ok)
                    return
            
            DB.AddCustomer(conn, data)
            rooms = DB.GetRoomsByType(conn, self.roomTypeSelection.currentIndex())
            conn.close()

            self.UpdateTableData()

    def DeleteBookingPressed(self):
        try:
            item = self.tableWidget.currentItem()
            text = f"Είστε σίγουροι ότι θέλετε να διαγράψετε την κράτηση;\n\n{item.text()}"
            test = MessageBox("Προσοχή", text)
            if test == QMessageBox.Yes:
                conn = DB.CreateConnection()
                DB.DeleteCustomer(conn, item.data(1))
                conn.close()
                self.UpdateTableData()
        except AttributeError as e:
            return
    
    def addRoomPressed(self):
        window = AddRoomWindow()
        temp = window.exec__()
        
        if temp:
            self.UpdateTableData()
    
    def removeRoomPressed(self):
        window = RemoveRoomWindow()
        temp = window.exec__()
        
        if temp:
            self.UpdateTableData()
    
    def closeEvent(self, event):
        close = MessageBox()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
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
                conn = DB.CreateConnection()
                
                # Check if the new date is equal or within the old date, if it isn't go into the loop
                if not ((data.CheckIn >= customerInfo.CheckIn) and (data.CheckOut <= customerInfo.CheckOut)):
                    occupiedDates = DB.GetRoomOccupiedDates(conn, data.RoomID, data.CheckIn.year, [customerInfo.CheckIn, customerInfo.CheckOut])
                    
                    for item in occupiedDates:
                        # Check if the new date is between the occupied dates
                        if not (((data.CheckIn - item[0]).days < 0 and (data.CheckOut - item[0]).days < 0) or ((data.CheckIn - item[1]).days >= 0 and (data.CheckOut - item[1]).days >= 0)):
                            # print(occupiedDates)
                            conn.close()
                            MessageBox('Σφάλμα', f'<p style="text-align:center;font-size:18px"><b>Ουπς...</p><p style="font-size:18px">Οι ημερομηνίες <b>"{data.CheckIn} - {data.CheckOut}"</b> συμπίπτουν με άλλη κράτηση.</p>', QMessageBox.Ok)
                            del occupiedDates
                            return
                    del occupiedDates
                
                self.SetLabelText(data)
                DB.UpdateCustomer(conn, customerInfo.CustomerID, data)
                conn.close()
                self.edited = 1
        except AttributeError as e:
            return
        
    def OKClicked(self):
        self.close()
    
    def GetRoomType(self, roomID):
        conn = DB.CreateConnection()
        a = roomDictionary[f'{DB.GetRoomType(conn, roomID)}']
        conn.close()
        return a
        
    def exec___(self):
        temp = self.exec_()
        return self.edited
        
class CustomerDataWindow(QtWidgets.QDialog):
    def __init__(self, title='Δεδομένα πελάτη', customerInfo=None):
        super(CustomerDataWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/CustomerData.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.setWindowTitle(title)
        
        self.ConnectLogicToObjects()
        
        if customerInfo:
            self.InitializeData(customerInfo)
    
    def ConnectLogicToObjects(self):
        self.bookingTypeInput = self.findChild(QtWidgets.QComboBox, 'bookingTypeInput')
        data = []
        for item in dictionary.values():
            data.append(item[0])
        self.bookingTypeInput.addItems(data)
        
        self.checkInInput = self.findChild(QtWidgets.QDateEdit, 'checkInInput')
        self.checkInInput.setDate(datetime.today())
        
        self.checkOutInput = self.findChild(QtWidgets.QDateEdit, 'checkOutInput')
        self.checkOutInput.setDate(datetime.today() + timedelta(5))
        
        self.commentInput = self.findChild(QtWidgets.QTextEdit, 'commentInput')
        
        self.nameinput = self.findChild(QtWidgets.QLineEdit, 'nameInput')
        
        self.peopleInput = self.findChild(QtWidgets.QSpinBox, 'peopleInput')
        
        self.pricePerNightInput = self.findChild(QtWidgets.QDoubleSpinBox, 'pricePerNightInput')
        
        self.roomIDInput = self.findChild(QtWidgets.QSpinBox, 'roomIDInput')
        
    def InitializeData(self, customerInfo):
        self.bookingTypeInput.setCurrentIndex(customerInfo.BookingType - 1)
        
        self.checkInInput.setDate(customerInfo.CheckIn)
        
        self.checkOutInput.setDate(customerInfo.CheckOut)
        
        self.commentInput.setText(customerInfo.Comments)
        
        self.nameinput.setText(customerInfo.Name)
        
        self.peopleInput.setValue(customerInfo.People)
        
        self.pricePerNightInput.setValue(customerInfo.PricePerNight)
        
        self.roomIDInput.setValue(customerInfo.RoomID)
        
        
        
    def GetTypeList(self):
        temp = roomDictionary.values()
        itemList = []
        for item in temp:
            itemList.append(item[0])
        
        return itemList
    
    def GetData(self):
        if self.exec_() == QDialog.Accepted:
            delta = self.checkOutInput.date().toPyDate() - self.checkInInput.date().toPyDate()
            numberOfNights = delta.days
            return Customer(self.nameinput.text(),
                            self.checkInInput.date().toPyDate(), 
                            self.checkOutInput.date().toPyDate(), 
                            self.roomIDInput.value(), 
                            self.bookingTypeInput.currentIndex() + 1,
                            self.pricePerNightInput.value(),
                            self.peopleInput.value(),
                            Comments=self.commentInput.toPlainText(),
                            NumberOfStayNights=numberOfNights,
                            TotalPrice=(numberOfNights) * self.pricePerNightInput.value())
            

class AddRoomWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddRoomWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/AddRoom.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.roomIDInput = self.findChild(QtWidgets.QSpinBox, 'roomIDInput')
        
        self.roomTypeInput = self.findChild(QtWidgets.QComboBox, 'roomTypeInput')
        self.roomTypeInput.addItems(roomDictionary.values())
           
    def exec__(self):
        if self.exec_() == QDialog.Accepted:
            conn = DB.CreateConnection()
            DB.AddRoom(conn, self.roomIDInput.value(), self.roomTypeInput.currentIndex() + 1)
            conn.close()
            return 1
        

class RemoveRoomWindow(QtWidgets.QDialog):
    def __init__(self):
        super(RemoveRoomWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/DeleteRoom.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.listWidget.addItems(self.GetRooms())
        self.listWidget.setCurrentRow(-1)
        
    def GetRooms(self):
        conn = DB.CreateConnection()
        rooms = DB.GetRoomsByType(conn)
        conn.close()
        
        if rooms:
            rooms = [str(i) for i in rooms]
        
        
        return rooms
    
    def exec__(self):
        if self.exec_() == QDialog.Accepted:
            row = self.listWidget.currentRow()
            item = self.listWidget.item(row)
            if item:
                msg = MessageBox('Προσοχή', f'Είστε σίγουροι ότι θέλετε να διαγράψετε το δωμάτιο "{item.text()}";')
                if msg == QMessageBox.Yes:
                    conn = DB.CreateConnection()
                    DB.DeleteRoom(conn, int(item.text()))
                    conn.close()
                    
                    return 1
        
class LoadingWindow(QtWidgets.QDialog):
    def __init__(self, text, title='Κρατήσεις'):
        super(LoadingWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/LoadingWindow.ui', self)
        
        self.setWindowTitle(title)
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)
        
class ErrorWindow(QtWidgets.QDialog):
    def __init__(self, text, title="Error"):
        super(ErrorWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/ErrorWindow.ui', self)
        
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle(title)
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)

def MessageBox(title='Έξοδος', text="Είστε σίγουροι ότι θέλετε να κλείσετε το πρόγραμμα;", buttons=QMessageBox.Yes | QMessageBox.Cancel):
    """
    :param title: Window title
    :param text: Window Text
    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setStandardButtons(buttons)
    msgBox = msgBox.exec()

    return msgBox