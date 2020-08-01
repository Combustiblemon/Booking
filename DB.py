import sqlite3
from sqlite3 import Error
from datetime import date, datetime
from Customer import Customer
import logging

def CreateConnection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

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
        print('Database connection failed.')
        return None
    
    sql = ''' INSERT INTO customers(CustomerName,People,CheckIn,CheckOut,PricePerNight,RoomID)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer.GetSQLFormatedDataForInsertion())
    conn.commit()

    return cur.lastrowid

    conn.commit()

    return cur.lastrowid

def GetCustomerIDByName(conn, name):
    """Returns the CustomerID of a given name

    Args:
        :param conn: The database connection object
        :param name: The name of the customer to find the ID
        :type name: string
        :return: List of the CustomerIDs found or None
    """
    if conn is None:
        print('Database connection failed.')
        return
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID FROM customers WHERE CustomerName = "{name}"')
    temp = cur.fetchall()
    
    customerID = []
    for item in temp:
        customerID.append(item[0])
    
    if not customerID:
        return None
    
    return customerID

def GetRoomCustomers(conn, roomID):
    """Returns all the customers of the given roomID

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room to get the customers
        
        :return: List of the customers or None
    """
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerName, People, CheckIn, CheckOut, PricePerNight FROM customers WHERE RoomID = {roomID}')
    customers = cur.fetchall()
    
    if not customers:
        return None
    return customers

def GetRoomOccupiedDates(conn, roomID):
    """Returns the dates the room is occupied

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room
        
        :return: List of dates the room is occupied
    """
    cur = conn.cursor()
    cur.execute(f'SELECT CheckIn, CheckOut FROM customers WHERE RoomID = {roomID} ORDER BY CheckIn')
    Temp = cur.fetchall()
    
    if not Temp:
        return None
    
    # convert Tuple Temp to list
    datesTemp = [list(i) for i in Temp]
    
    # Congregate dates into chunks
    dates = [[datesTemp[0][0], datesTemp[0][1]]]
    for item in datesTemp[1:]:
        if dates[len(dates) - 1][1] == item[0]:
            dates[len(dates) - 1][1] = item[1]
        else:
            dates.append(item)
    
    # Convert dates from string to datetime objects
    for item in dates: 
        temp = item[0].split('-')
        item[0] = date(int(temp[0]), int(temp[1]), int(temp[2]))
        
        temp = item[1].split('-')
        item[1] = date(int(temp[0]), int(temp[1]), int(temp[2]))

    return dates
    