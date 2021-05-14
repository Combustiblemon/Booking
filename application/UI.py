from PySide6 import QtWidgets, QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtGui import QColor
from datetime import datetime, date, timedelta
from Customer import Customer
import platform
import DB
from files.UI import ui_MainWindow, ui_AddRoom, ui_CustomerData, ui_CustomerInfo, ui_DeleteRoom, ui_ErrorWindow, ui_LoadingWindow, ui_PasswordWindow
import json
import pathlib
from calendar import monthrange



FilePath = pathlib.Path(__file__).parent.absolute()
dictionary = {} 
with open(f'{FilePath}/files/data/dictionary.json', 'r', encoding="utf8") as file:
    dictionary = json.load(file)
    
roomDictionary = {} 
with open(f'{FilePath}/files/data/roomDictionary.json', 'r', encoding="utf8") as file:
    roomDictionary = json.load(file)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, months):
        super(MainWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
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
        
        self.addRoom = self.findChild(QtGui.QAction, 'addRoom')
        self.addRoom.triggered.connect(self.addRoomPressed)
        
        self.removeRoom = self.findChild(QtGui.QAction, 'removeRoom')
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
        # get the customer data for the current month
        data = DB.GetCustomersByMonth(self.monthSelection.currentIndex() + 1, self.yearSelection.date().year(), self.roomTypeSelection.currentIndex())
        
        # get the rooms based on the room type
        rooms = DB.GetRoomsByType(self.roomTypeSelection.currentIndex())
        
        
        
        currentRow = self.tableWidget.currentRow()
        currentColumn = self.tableWidget.currentColumn()
        
        # set up the table rows
        try:
            # set the number of rows based on the selected roomtype
            self.tableWidget.setRowCount(0)

            #set up the rooms
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
                    
                    # if the check in is on a previous month and check out on a following month, set the cell span to the entire row
                    if item.CheckIn.month < (self.monthSelection.currentIndex() + 1) and item.CheckOut.month > (self.monthSelection.currentIndex() + 1):
                        column = 0
                        _, daysInMonth = monthrange(self.yearSelection.date().year(), self.monthSelection.currentIndex() + 1)
                        span = daysInMonth
                    # if the CheckIn date is on a previous month only paint the days in the current month
                    elif item.CheckIn.month < (self.monthSelection.currentIndex() + 1):  
                        column = 0
                        span = item.CheckOut.day - 1
                    # if the Checkout date is on a following month calculate difference and only paint the days in the current month
                    elif item.CheckOut.month > (self.monthSelection.currentIndex() + 1):
                        _, daysInMonth = monthrange(item.CheckIn.year, item.CheckIn.month)
                        delta = (date(item.CheckIn.year, item.CheckIn.month, daysInMonth) - item.CheckIn).days
                        span = delta + 1
                        
                    
                    self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(f'"{item.Name}" Άτομα: {item.People} Τιμή ανά βράδυ: {item.PricePerNight}')) # create a new item
                    temp = self.tableWidget.item(row, column)  # access the item just created
                    temp.setBackground(QColor(dictionary[f"{item.BookingType}"][1][0], dictionary[f"{item.BookingType}"][1][1], dictionary[f"{item.BookingType}"][1][2], a=150))  # set the background color of the item based on the dictionary
                    temp.setData(1, item.CustomerID)  # set the metadata of the item to the CustomerID
                    self.tableWidget.setSpan(row, column, 1, span)  # merge the cells
                except ValueError:
                    pass
                    
            del data  # clean up memory by deleting the customer data from memory
        
        except TypeError:
            pass
        
    def cellDoubleClicked(self, row, column):
        try:
            CustomerInfo = DB.GetCustomerByID(self.tableWidget.item(row, column).data(1))
            
            window = CustomerInfoWindow(CustomerInfo)
            edited = window.exec___()
            
            if edited:
                rooms = DB.GetRoomsByType(self.roomTypeSelection.currentIndex())
                self.UpdateTableData()
        except AttributeError:
            pass
    
    def AddBookingClicked(self):
        window = CustomerDataWindow('Δεδομένα Κράτησης')
        data = window.GetData()
        
        if data:
            occupiedDates = DB.GetRoomOccupiedDates(data.RoomID, data.CheckIn.year)
            try:
                for item in occupiedDates:
                    # check if the dates entered fall on another booking
                    if not (((data.CheckIn - item[0]).days < 0 and (data.CheckOut - item[0]).days <= 0) or ((data.CheckIn - item[1]).days >= 0 and (data.CheckOut - item[1]).days > 0)):
                        MessageBox('Σφάλμα', f'<p style="text-align:center;font-size:18px"><b>Ουπς...</p><p style="font-size:18px">Οι ημερομηνίες <b>"{data.CheckIn} - {data.CheckOut}"</b> συμπίπτουν με άλλη κράτηση.</p>', QMessageBox.Ok)
                        return
            except TypeError:
                pass
            
            DB.AddCustomer(data)
            rooms = DB.GetRoomsByType(self.roomTypeSelection.currentIndex())

            self.UpdateTableData()

    def DeleteBookingPressed(self):
        try:
            item = self.tableWidget.currentItem()
            text = f"Είστε σίγουροι ότι θέλετε να διαγράψετε την κράτηση;\n\n{item.text()}"
            test = MessageBox("Προσοχή", text)
            if test == QMessageBox.Yes:
                DB.DeleteCustomer(item.data(1))
                self.UpdateTableData()
        except AttributeError as e:
            pass
    
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
        self.ui = ui_CustomerInfo.Ui_CustomerInfo()
        self.ui.setupUi(self)
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
        
    def SetLabelText(self, customerInfo: Customer):
        text = f"""<p><b>Όνομα κράτησης:</b> {customerInfo.Name}</p>
                <p>     <b>Αριθμός ατόμων:</b> {customerInfo.People}</p>
                <p>     <b>Check in:</b>  {customerInfo.CheckIn}</p>
                <p>     <b>Check out:</b> {customerInfo.CheckOut}</p>
                <p>     <b>Διανυκτερεύσεις:</b> {customerInfo.NumberOfStayNights}</p>
                <p>     <b>Τιμή ανά βράδυ:</b> {customerInfo.PricePerNight}€</p>
                <p>     <b>Σύνολο:</b> {customerInfo.PricePerNight * customerInfo.NumberOfStayNights}€</p>
                <p>     <b>Δωμάτιο:</b> {customerInfo.RoomID} ({self.GetRoomType(customerInfo.RoomID)})</p>
                <p>     <b>Κράτηση από:</b> {dictionary[f"{customerInfo.BookingType}"][0]}</p>
                
                <p>     <b>Σχόλια:</b> {customerInfo.Comments}</p>"""
        
        self.textLabel.setText(text)        
        
    def EditInfo(self, customerInfo):
        window = CustomerDataWindow(customerInfo=customerInfo)
        data = window.GetData()
        
        try:
            if data != customerInfo:  # if the data from the edit window are different from before, update the database and set the edited flag to 1
                
                # Check if the new date is equal or within the old date, if it isn't go into the loop
                if not ((data.CheckIn >= customerInfo.CheckIn) and (data.CheckOut <= customerInfo.CheckOut)):
                    occupiedDates = DB.GetRoomOccupiedDates(data.RoomID, data.CheckIn.year, [customerInfo.CheckIn, customerInfo.CheckOut])
                    if occupiedDates:
                        for item in occupiedDates:
                            # Check if the new date is between the occupied dates
                            if not (((data.CheckIn - item[0]).days < 0 and (data.CheckOut - item[0]).days < 0) or ((data.CheckIn - item[1]).days >= 0 and (data.CheckOut - item[1]).days >= 0)):
                                # print(occupiedDates)
                                MessageBox('Σφάλμα', f'<p style="text-align:center;font-size:18px"><b>Ουπς...</p><p style="font-size:18px">Οι ημερομηνίες <b>"{data.CheckIn} - {data.CheckOut}"</b> συμπίπτουν με άλλη κράτηση.</p>', QMessageBox.Ok)
                                del occupiedDates
                                return
                        del occupiedDates
                
                self.SetLabelText(data)
                DB.UpdateCustomer(customerInfo.CustomerID, data)
                self.edited = 1
        except AttributeError as e:
            pass
        
    def OKClicked(self):
        self.close()
    
    def GetRoomType(self, roomID):
        a = roomDictionary[f'{DB.GetRoomType(roomID)}']
        return a
        
    def exec___(self):
        temp = self.exec_()
        return self.edited
        
class CustomerDataWindow(QtWidgets.QDialog):
    def __init__(self, title='Δεδομένα πελάτη', customerInfo=None):
        super(CustomerDataWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_CustomerData.Ui_CustomerData()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.setWindowTitle(title)
        
        self.ConnectLogicToObjects()
        
        if customerInfo:
            self.InitializeData(customerInfo)
    
    def ConnectLogicToObjects(self):
        self.bookingTypeInput = self.findChild(QtWidgets.QComboBox, 'bookingTypeInput')
        
        # set up the booking types in the drop down
        data = []
        for item in dictionary.values():
            data.append(item[0])
        self.bookingTypeInput.addItems(data)
        
        self.checkInInput = self.findChild(QtWidgets.QDateEdit, 'checkInInput')
        self.checkInInput.setDate(datetime.today())
        self.checkInInput.dateChanged.connect(self.CheckInChanged)
        
        self.checkOutInput = self.findChild(QtWidgets.QDateEdit, 'checkOutInput')
        self.checkOutInput.setDate(datetime.today() + timedelta(5))
        self.oldDate = QtCore.QDate.currentDate().addDays(-10)
        self.newDate = QtCore.QDate.currentDate().addDays(-10)
        self.checkOutInput.dateChanged.connect(self.CheckOutChanged)

        
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
    
    def CheckInChanged(self, date: QtCore.QDate):
        self.checkOutInput.setDate(date.addDays(5))
    
    def CheckOutChanged(self, date: QtCore.QDate):
        # spaghetti because event fires twice
        # this checks if the stay days are < 1 and readjusts the inputs
        if self.newDate != date and date != self.oldDate:
            if date <= self.checkInInput.date():
                self.oldDate = date
                self.newDate = self.checkInInput.date().addDays(5)
                self.checkOutInput.setDate(self.checkInInput.date().addDays(5))
                MessageBox(title='Προσοχή', text='<p style="text-align:left;font-size:18px"><b>Ο αριθμός διανυκτερεύσεων δεν μπορεί να είναι μικρότερος απο 1', buttons=QMessageBox.Ok) 

    def GetData(self):
        if self.exec_() == QDialog.Accepted:
            delta = self.checkOutInput.date().toPython() - self.checkInInput.date().toPython()
            numberOfNights = delta.days
            return Customer(self.nameinput.text(),
                            self.checkInInput.date().toPython(), 
                            self.checkOutInput.date().toPython(), 
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
        self.ui = ui_AddRoom.Ui_AddRoom()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.roomIDInput = self.findChild(QtWidgets.QSpinBox, 'roomIDInput')
        
        self.roomTypeInput = self.findChild(QtWidgets.QComboBox, 'roomTypeInput')
        self.roomTypeInput.addItems(roomDictionary.values())
           
    def exec__(self):
        if self.exec_() == QDialog.Accepted:
            DB.AddRoom(self.roomIDInput.value(), self.roomTypeInput.currentIndex() + 1)
            return 1
        

class RemoveRoomWindow(QtWidgets.QDialog):
    def __init__(self):
        super(RemoveRoomWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_DeleteRoom.Ui_DeleteRoom()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.listWidget.addItems(self.GetRooms())
        self.listWidget.setCurrentRow(-1)
        
    def GetRooms(self):
        rooms = DB.GetRoomsByType()
        
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
                    DB.DeleteRoom(int(item.text()))
                    
                    return 1
        
class LoadingWindow(QtWidgets.QDialog):
    def __init__(self, text, title='Κρατήσεις'):
        super(LoadingWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_LoadingWindow.Ui_LoadingWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle(title)
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)
        
class ErrorWindow(QtWidgets.QDialog):
    def __init__(self, text, title="Error"):
        super(ErrorWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_ErrorWindow.Ui_ErrorWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle(title)
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)

def MessageBox(title:str = 'Έξοδος', text:str = "Είστε σίγουροι ότι θέλετε να κλείσετε το πρόγραμμα;", buttons=QMessageBox.Yes | QMessageBox.Cancel):
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