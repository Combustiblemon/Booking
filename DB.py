import sqlite3
from sqlite3 import Error
from datetime import date, datetime
from Customer import Customer
import logging
import os

def CreateConnection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(os.environ['DATABASE_PATH'])
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

def UpdateCustomer(conn, customerID, customer):
    """Updates an existing customer in the database with new data

    :param conn: The database connection object
    :param customerID: The ID of the customer to be updated
    :param customer: The customer object
    """
    
    if conn is None:
        print('Database connection failed.')
        return None
    
    data = customer.GetSQLFormatedDataForInsertion()
    data.append(customerID)
    
    sql = ''' UPDATE customers SET CustomerName = ?,People = ?,CheckIn = ?,CheckOut = ?,PricePerNight = ?,RoomID = ? WHERE CustomerID = ?'''
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
        print('Database connection failed.')
        return None

    cur = conn.cursor()
    cur.execute('DELETE FROM customers WHERE CustomerID = ?;', (CustomerID,))
    conn.commit()
    
    return cur.lastrowid
    

def GetCustomer(conn, name, year=int(datetime.today().strftime('%Y'))):
    """

        :param conn: The database connection object
        :param name: The name of the customer to get the data of
        :param year: The date of the check in. defaults to current year
    """
    if conn is None:
        print('Database connection failed.')
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID,CustomerName,People,CheckIn,CheckOut,PricePerNight,RoomID FROM customers WHERE CustomerName = "{name}" AND CheckIn LIKE "{year}%"')
    temp = cur.fetchall()
    
    # convert tuple to list
    data = [list(i) for i in temp]
    
    for item in data:
        item[3] = ConvertStringToDate(item[3])
        
        item[4] = ConvertStringToDate(item[4])
    
    customers = []  
    for item in data:
        customers.append(Customer(item[1], item[3], item[4], item[6], item[0], item[5], item[2]))
        
    return customers

def GetCustomerIDByName(conn, name, roomID):
    """Returns the CustomerID of a given name

    Args:
        :param conn: The database connection object
        :param name: The name of the customer to find the ID
        :param roomID: The ID of the room
        :return: List of the CustomerIDs found or None
    """
    if conn is None:
        print('Database connection failed.')
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerID FROM customers WHERE CustomerName = "{name}"')
    temp = cur.fetchall()
    
    customerID = []
    for item in temp:
        customerID.append(item[0])
    
    if not customerID:
        return None
    
    return customerID

def GetCustomersByMonth(conn, month=int(datetime.today().strftime('%m')), year=int(datetime.today().strftime('%Y'))):
    """Returns all the customers of the given month

    :param conn: The database connection object
    :param month: The month to get the data. Defaults to the current month
    :param year: The year to get the data. Default to current year
    """
    if conn is None:
        print('Database connection failed.')
        return None
    
    if month < 10:
        month = f'0{str(month)}'
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerName, People, CheckIn, CheckOut, PricePerNight FROM customers WHERE CheckIn LIKE "{year}-{month}%" OR CheckOut LIKE "{year}-{month}%" ORDER BY CheckIn')
    customers = cur.fetchall()
    
    return customers
    
def GetCustomersByRoomID(conn, roomID):
    """Returns all the customers of the given roomID

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room to get the customers
        
        :return: List of the customers or None
    """
    if conn is None:
        print('Database connection failed.')
        return None
    
    cur = conn.cursor()
    cur.execute(f'SELECT CustomerName, People, CheckIn, CheckOut, PricePerNight FROM customers WHERE RoomID = {roomID} ORDER BY CheckIn')
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
    if conn is None:
        print('Database connection failed.')
        return None
    
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
        item[0] = ConvertStringToDate(item[0])
        
        item[1] = ConvertStringToDate(item[1])

    return dates
    