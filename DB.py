import sqlite3
from sqlite3 import Error

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

def AddCustomer(conn, customer):
    """Add the customer Data to the DB

    Args:
        :param conn: The database connection object
        :param customer: The customer data [CustomerID, Name, People, CheckIn, CheckOut, PricePerNight, RoomID]
    """
    if conn is None:
        print('Database connection failed.')
        return
    
    sql = ''' INSERT INTO customers(Name,People,CheckIn,CheckOut,PricePerNight,RoomID)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()

    return cur.lastrowid

def FindCustomerIDByName(conn, name):
    """[summary]

    Args:
        :param conn: The database connection object
        :param name: The name of the customer to find the ID
        :type name: string
        :return: array of the CustomerIDs found or None
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

def FindRoomCustomers(conn, roomID):
    """[summary]

    Args:
        :param conn: The database connection object
        :param roomID: The ID of the room to get the customers
        :return: Array of the customers or None
    """
    cur = conn.cursor()
    cur.execute(f'SELECT RoomID FROM customers WHERE RoomID = {roomID}')
    customers = cur.fetchall()
    
    
    return customers
    