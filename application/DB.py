import sqlite3
from sqlite3 import Error
from datetime import date, datetime
from Customer import Customer
from configHandler import config
import UI
import logging
import os

db_path = ":memory:"

def CreateDatabase(path:str = None):
    """Creates the database file if it is missing
    """
    
    if path:
        global db_path 
        db_path = path
        
    conn = CreateConnection()
    cur = conn.cursor()
    
    try:
        sql = """ CREATE TABLE rooms (
        RoomID   INTEGER PRIMARY KEY
                        NOT NULL,
        RoomType INTEGER NOT NULL
        ); """
        
        cur.execute(sql)
        
        sql = """CREATE TABLE customers (
        CustomerID    INTEGER NOT NULL
                            PRIMARY KEY
                            UNIQUE,
        CustomerName  TEXT    NOT NULL,
        People        INTEGER,
        CheckIn       DATE,
        CheckOut      DATE,
        PricePerNight REAL,
        RoomID        INTEGER NOT NULL,
        BookingType   INTEGER NOT NULL,
        Comments      STRING,
        NumberOfStayNights INTEGER,
        TotalPrice         REAL,
        FOREIGN KEY (
            RoomID
        )
        REFERENCES rooms (RoomID) 
        );"""
        
        cur.execute(sql)
        conn.commit()
    except Error as e:
        errorW = UI.ErrorWindow(e)
    

def CreateConnection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        DBError(e)

    return conn

def DBError(error=''):
    errorW = UI.ErrorWindow(f'Αποτυχία σύνδεσης με βάση δεδομένων!\n{error}')
    errorW.show()

def ConvertStringToDate(dateString):
    """Converts a string to a datetime object. YYYY-MM-DD

    :param dateString: The string to get converted
    """
    try:
        temp = dateString.split('-')
        dateObj = date(int(temp[0]), int(temp[1]), int(temp[2]))
        return dateObj
    except Exception as e:
        logging.exception("exception")
        return dateString

def AddCustomer(conn, customer):
    """Add the customer Data to the DB

    Args:
        :param conn: The database connection object
        :param customer: The customer object
    """
    if conn is None:
        DBError()
        return None
    
    sql = ''' INSERT INTO customers(CustomerName,People,CheckIn,CheckOut,PricePerNight,RoomID,BookingType,Comments,NumberOfStayNights,TotalPrice)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer.GetSQLFormatedDataForInsertion())
    conn.commit()

    return cur.lastrowid

def UpdateCustomer(conn, customerID, customer):
    """Updates an existing customer in the database with new data

    :param conn: The database connection object
    :param customerID: The ID of the customer to be updated
    :param customer: The customer object
    """
    
    if conn is None:
        DBError()
        return None
    
    data = customer.GetSQLFormatedDataForInsertion()
    data.append(customerID)
    
    sql = ''' UPDATE customers SET CustomerName = ?,People = ?,CheckIn = ?,CheckOut = ?,PricePerNight = ?,RoomID = ?,BookingType = ?,Comments = ?,NumberOfStayNights = ?,TotalPrice = ? WHERE CustomerID = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    
    return cur.lastrowid

def DeleteCustomer(conn, CustomerID):
    """Deletes a customer

    :param conn: The connection object
    :param CustomerID: The ID of the customer to delete
    """
    
    if conn is None:
        DBError()
        return None

    cur = conn.cursor()
    cur.execute('DELETE FROM customers WHERE CustomerID = ?;', (CustomerID,))
    conn.commit()
    
    return cur.lastrowid
    

def GetCustomer(conn, name, year=datetime.today().year):
    """

        :param conn: The database connection object
        :param name: The name of the customer to get the data of
        :param year: The date of the check in. defaults to current year
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID, CustomerName, People, CheckIn, CheckOut, PricePerNight, RoomID, BookingType, Comments, NumberOfStayNights, TotalPrice FROM customers WHERE CustomerName = "{name}" AND CheckIn LIKE "{year}%"')
    temp = cur.fetchall()
    
    if not temp:
        return None
    
    # convert tuple to list
    data = [list(i) for i in temp]
    
    for item in data:
        item[3] = ConvertStringToDate(item[3])
        
        item[4] = ConvertStringToDate(item[4])
    
    customers = []  
    for item in data:
        customers.append(Customer(item[1], item[3], item[4], item[6], item[7], item[5], item[2], item[0], item[8], item[9], item[10]))
        
    return customers

def GetCustomerByID(conn, customerID):
    """

        :param conn: The database connection object
        :param customerID: The ID of the customer
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID, CustomerName, People, CheckIn, CheckOut, PricePerNight, RoomID, BookingType, Comments, NumberOfStayNights, TotalPrice FROM customers WHERE CustomerID = "{customerID}"')
    temp = cur.fetchall()
    
    if not temp:
        return None
    
    # convert tuple to list
    data = [list(i) for i in temp]

    data[0][3] = ConvertStringToDate(data[0][3])
        
    data[0][4] = ConvertStringToDate(data[0][4])
        
    return Customer(data[0][1], data[0][3], data[0][4], data[0][6], data[0][7], data[0][5], data[0][2], data[0][0], data[0][8], data[0][9], data[0][10])

def GetCustomerIDByName(conn, name, roomID):
    """Returns the CustomerID of a given name

    Args:
        :param conn: The database connection object
        :param name: The name of the customer to find the ID
        :param roomID: The ID of the room
        :return: List of the CustomerIDs found or None
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID FROM customers WHERE CustomerName = "{name}"')
    temp = cur.fetchall()
    
    if not temp:
        return None
    
    customerID = []
    for item in temp:
        customerID.append(item[0])
    
    return customerID

def GetCustomersByMonth(conn, month=datetime.today().month, year=datetime.today().year, roomType=0):
    """Returns all the customers of the given month and roomType. Defaults to getting all the data per month

    :param conn: The database connection object
    :param month: The month to get the data. Defaults to the current month
    :param year: The year to get the data. Default to current year
    :param roomType: The ID of the type of room
    """
    if conn is None:
        DBError()
        return None
    
    if month < 10:
        month = f'0{str(month)}'
    
    sql = f'''SELECT CustomerID, CustomerName, People, CheckIn, CheckOut, PricePerNight, RoomID, BookingType, Comments, NumberOfStayNights, TotalPrice
    FROM customers 
    WHERE CheckIn LIKE "{year}-{month}%" OR CheckOut LIKE "{year}-{month}%" 
    ORDER BY CheckIn'''
    
    if roomType != 0:
        sql = f'''SELECT CustomerID, CustomerName, People, CheckIn, CheckOut, PricePerNight, RoomID, BookingType, Comments, NumberOfStayNights, TotalPrice 
    FROM customers 
    WHERE (CheckIn LIKE "{year}-{month}%" OR CheckOut LIKE "{year}-{month}%") AND RoomID IN {GetRoomsByType(conn, roomType)}
    ORDER BY CheckIn'''
    
    cur = conn.cursor()
    cur.execute(sql)
    temp = cur.fetchall()
    
    if not temp:
        return None
    
    # convert tuple to list
    data = [list(i) for i in temp]
    
    for item in data:
        item[3] = ConvertStringToDate(item[3])
        
        item[4] = ConvertStringToDate(item[4])

    customers = []  
    for item in data:
        customers.append(Customer(item[1], item[3], item[4], item[6], item[7], item[5], item[2], item[0], item[8], item[9], item[10]))
    
    return customers
    
def GetCustomersByRoomID(conn, roomID):
    """Returns all the customers of the given roomID

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room to get the customers
        
        :return: List of the customers or None
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID, CustomerName, People, CheckIn, CheckOut, PricePerNight, RoomID, BookingType, Comments, NumberOfStayNights, TotalPrice FROM customers WHERE RoomID = {roomID} ORDER BY CheckIn')
    temp = cur.fetchall()
    
    if not temp:
        return None
    
    # convert tuple to list
    data = [list(i) for i in temp]
    
    for item in data:
        item[3] = ConvertStringToDate(item[3])
        
        item[4] = ConvertStringToDate(item[4])
    
    customers = []  
    for item in data:
        customers.append(Customer(item[1], item[3], item[4], item[6], item[7], item[5], item[2], item[0], item[8], item[9], item[10]))
        
    return customers

def GetRoomOccupiedDates(conn, roomID, year=datetime.today().year, exclude=[]):
    """Returns the dates the room is occupied

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room
        :param month: The month to get the dates for. Defaults to current
        :param year: The year to get the date for. Defaults to current
        :param exclude [Checkin, CheckOut]: The dates to exclude.  
        
        :return: List of dates the room is occupied
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CheckIn, CheckOut FROM customers WHERE RoomID = {roomID} AND (CheckIn LIKE "{year}%" OR CheckOut LIKE "{year}%") ORDER BY CheckIn')
    Temp = cur.fetchall()
    
    if not Temp:
        return None
    
    # convert Tuple Temp to list
    datesTemp = [list(i) for i in Temp]
    
    try:
        datesTemp.remove([exclude[0].strftime('%Y-%m-%d'), exclude[1].strftime('%Y-%m-%d')])
    except Exception as e:
        print(e)
    try:
        # Congregate dates into chunks
        dates = [[datesTemp[0][0], datesTemp[0][1]]]
        for item in datesTemp[1:]:
            if dates[len(dates) - 1][1] == item[0]:
                dates[len(dates) - 1][1] = item[1]
            else:
                dates.append(item)
        
        # Convert dates from string to datetime objects
        for item in dates: 
            item[0] = ConvertStringToDate(item[0])
            
            item[1] = ConvertStringToDate(item[1])

        return dates
    except IndexError:
        return None

def GetRoomType(conn, roomID):
    """Returns the type of room for a given ID

    :param conn: The database connection object
    :param roomID: The ID of the room
    """
    if conn is None:
        DBError()
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT RoomType FROM rooms WHERE RoomID = {roomID}')
    temp = cur.fetchall()
    
    return temp[0][0]

def GetRoomNumber(conn, roomType=0):
    """Returns the number of rooms for a given type. By default returns the number of all rooms

    :param conn: The dtabase connection object
    :param roomType [int]: The ID of the room type
    """
    if conn is None:
        DBError()
        return None
    
    sql = 'SELECT RoomType FROM rooms'
    
    if roomType != 0:
        sql = f'SELECT RoomType FROM rooms WHERE RoomType = {roomType}'
        
    cur = conn.cursor()
    cur.execute(sql)
    temp = cur.fetchall()
    
    return len(temp)

def GetRoomsByType(conn, roomType=None):
    """Returns all the room IDs for the given room type. Defaults to returning all rooms

    :param conn: The database connection object
    :param roomType [int]: The ID of the room type
    """
    if conn is None:
        DBError()
        return None
    
    if roomType:
        sql = f'SELECT RoomID FROM rooms WHERE RoomType = {roomType} ORDER BY RoomID'
    else:
        sql = 'SELECT RoomID FROM rooms'
    
    cur = conn.cursor()
    cur.execute(sql)
    temp = cur.fetchall()
    
    data = []
    for item in temp:
        data.append(item[0])
    
    return tuple(data)

def AddRoom(conn, roomID, roomType):
    """Adds a new room to the database

    :param conn: The database connection object
    :param roomID: The ID of the room
    :param roomType: The type of the room
    """
    if conn is None:
        DBError()
        return None
    
    sql = "INSERT INTO rooms(RoomID,RoomType) Values(?,?)"
    
    cur = conn.cursor()
    cur.execute(sql, (roomID, roomType))
    conn.commit()
    
    return cur.lastrowid

def DeleteRoom(conn, roomID):
    """Deletes a room from the database

    :param conn: The connection object
    :param roomID: The ID of the room to delete
    """
    
    if conn is None:
        DBError()
        return None

    cur = conn.cursor()
    cur.execute('DELETE FROM rooms WHERE RoomID = ?;', (roomID,))
    conn.commit()
    
    return cur.lastrowid