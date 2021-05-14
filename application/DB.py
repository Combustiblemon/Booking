import sqlite3
from sqlite3 import Error
from datetime import date, datetime
from warnings import filterwarnings
from Customer import Customer
from configHandler import config
import DBUtils
import LocalDB
import UI
import logging
import os
import pathlib
import traceback

isLocal = False
if config['DATABASE']['local_database'] == '1':
    isLocal = True

def CreateDatabase(path:str = None):
    """Creates the database file if it is missing
    """
    # no need to create a local DB if we're running on remote
    if isLocal:
        LocalDB.CreateDatabase(path)

def DBError(error=''):
    errorW = UI.ErrorWindow(f'Αποτυχία σύνδεσης με βάση δεδομένων!\n{error}')
    errorW.show()

def ConvertStringToDate(dateString: str):
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

def AddCustomer(customer: Customer):
    """Add the customer Data to the DB

    Args:
        :param customer: The customer object
    """
    
    if isLocal:
        return LocalDB.AddCustomer(customer)
    else:
        try:
            return DBUtils.PUT('customers', customer.GetDictFormatedData())
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()
        
def UpdateCustomer(customerID, customer: Customer):
    """Updates an existing customer in the database with new data

    :param customerID: The ID of the customer to be updated
    :param customer: The customer object
    """
    
    if isLocal:
        return LocalDB.UpdateCustomer(customerID, customer)
    else:
        try:
            payload = customer.GetDictFormatedData()
            payload['filters'] = ('customer_id', customerID, 'eq')
            
            return DBUtils.PATCH('customers', payload)
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def DeleteCustomer(CustomerID):
    """Deletes a customer

    :param CustomerID: The ID of the customer to delete
    """
    
    if isLocal:
        return LocalDB.DeleteCustomer(CustomerID)
    else:
        try:
            return DBUtils.DELETE('customers', [('customer_id', CustomerID, 'eq')])
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()
    

def GetCustomer(name: str, year: int = datetime.today().year):
    """Get customer data from name and year of stay

        :param name: The name of the customer to get the data of
        :param year: The date of the check in. defaults to current year
    """
    name = name.lower()
    if isLocal:
        return LocalDB.GetCustomer(name, year)
    else:
        try:
            filters = [
                ('customer_name', name, 'like'),
                ('check_in', year, 'like')
            ]
            data = DBUtils.GET('customers', filters)
            if len(data) == 0:
                return None
            
            customers = []
            for item in data:
                customers.append(Customer(Name=item['customer_name'],
                                          CheckIn=ConvertStringToDate(item['check_in']),
                                          CheckOut=ConvertStringToDate(item['check_out']),
                                          RoomID=item['room_id'],
                                          BookingType=item['booking_type'],
                                          PricePerNight=item['price_per_night'],
                                          People=item['number_of_people'],
                                          CustomerID=item['customer_id'],
                                          Comments=item['comment'],
                                          NumberOfStayNights=item['stay_days_number']))
                
            return customers
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()


def GetCustomerByID(customerID):
    """Get customer data by ID

        :param customerID: The ID of the customer
    """
    
    if isLocal:
        return LocalDB.GetCustomerByID(customerID)
    else:
        try:
            data = DBUtils.GET('customers', [('customer_id', customerID, 'eq')])
            if len(data) == 0:
                return None
            
            return Customer(Name=data[0]['customer_name'],
                            CheckIn=ConvertStringToDate(data[0]['check_in']),
                            CheckOut=ConvertStringToDate(data[0]['check_out']),
                            RoomID=data[0]['room_id'],
                            BookingType=data[0]['booking_type'],
                            PricePerNight=data[0]['price_per_night'],
                            People=data[0]['number_of_people'],
                            CustomerID=data[0]['customer_id'],
                            Comments=data[0]['comment'],
                            NumberOfStayNights=data[0]['stay_days_number'])
        
        except IndexError:
            return None
          
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()
    
def GetCustomerIDByName(name: str):
    """Returns the CustomerID of a given name

    Args:
        :param name: The name of the customer to find the ID
        :return: List of the CustomerIDs found or None
    """
    
    if isLocal:
        return LocalDB.GetCustomerIDByName(name)
    else:
        try:
            filters = [
                ('customer_name', name, 'like'),
            ]
            data = DBUtils.GET('customers', filters)
            if len(data) == 0:
                return None
            
            customerID = []
            for item in data:
                customerID.append(item[0])
            
            return customerID
        except IndexError:
            return None
        
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def GetCustomersByMonth(month=datetime.today().month, year=datetime.today().year, roomType=0) -> list[Customer]:
    """Returns all the customers of the given month and roomType. Defaults to getting all the data per month

    :param month: The month to get the data. Defaults to the current month
    :param year: The year to get the data. Default to current year
    :param roomType: The ID of the type of room
    """
    
    if isLocal:
        return LocalDB.GetCustomersByMonth(month, year, roomType)
    else:
        try:
            if month < 10:
                month = f'0{str(month)}'
            
            filters = [
                (['check_in', 'check_out'], [f'{year}-{month}', f'{year}-{month}'], 'or'),
            ]
            data = DBUtils.GET('customers', filters)
            if len(data) == 0:
                return None
            
            customers = []
            for item in data:
                customers.append(Customer(Name=item['customer_name'],
                                          CheckIn=ConvertStringToDate(item['check_in']),
                                          CheckOut=ConvertStringToDate(item['check_out']),
                                          RoomID=item['room_id'],
                                          BookingType=item['booking_type'],
                                          PricePerNight=item['price_per_night'],
                                          People=item['number_of_people'],
                                          CustomerID=item['customer_id'],
                                          Comments=item['comment'],
                                          NumberOfStayNights=item['stay_days_number']))
                
            return customers
        
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()
    
def GetCustomersByRoomID(roomID):
    """Returns all the customers of the given roomID

    Args:
        :param roomID: The ID of the room to get the customers
        
        :return: List of the customers or None
    """
    
    if isLocal:
        return LocalDB.GetCustomersByRoomID(roomID)
    else:
        try:
            data = DBUtils.GET('rooms', [('room_id', roomID, 'eq')])
            
            if len(data) == 0:
                return None
            
            customers = []
            for item in data:
                customers.append(Customer(Name=item['customer_name'],
                                          CheckIn=ConvertStringToDate(item['check_in']),
                                          CheckOut=ConvertStringToDate(item['check_out']),
                                          RoomID=item['room_id'],
                                          BookingType=item['booking_type'],
                                          PricePerNight=item['price_per_night'],
                                          People=item['number_of_people'],
                                          CustomerID=item['customer_id'],
                                          Comments=item['comment'],
                                          NumberOfStayNights=item['stay_days_number']))
                
            return customers
        
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def GetRoomOccupiedDates(roomID, year=datetime.today().year, exclude:list = None):
    """Returns the dates the room is occupied

    Args:
        :param roomID: The ID of the room
        :param month: The month to get the dates for. Defaults to current
        :param year: The year to get the date for. Defaults to current
        :param exclude [Checkin, CheckOut]: The dates to exclude.  
        
        :return: List of dates the room is occupied
    """
    
    if isLocal:
        return LocalDB.GetRoomOccupiedDates(roomID, year, exclude)
    else:
        try:
            filters = [
                ('room_id', roomID, 'eq'),
                (['check_in', 'check_out'], [f'{year}', f'{year}'], 'or'),
            ]
            data = DBUtils.GET('customers', filters)
            
            datesTemp = []
            for item in data:
                datesTemp.append([item['check_in'], item['check_out']])
                        
            try:
                datesTemp.remove([exclude[0].strftime('%Y-%m-%d'), exclude[1].strftime('%Y-%m-%d')])
            except Exception as e: 
                pass
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
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def GetRoomType(roomID):
    """Returns the type of room for a given ID

    :param conn: The database connection object
    :param roomID: The ID of the room
    """
    
    if isLocal:
        return LocalDB.GetRoomType(roomID)
    else:
        try:
            data = DBUtils.GET('rooms', [('room_id', roomID, 'eq')])
            return data[0]['room_type']
        
        except IndexError:
            return None
        
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def GetRoomNumber(roomType=0):
    """Returns the number of rooms for a given type. By default returns the number of all rooms

    :param roomType [int]: The ID of the room type
    """
    
    if isLocal:
        return LocalDB.GetRoomNumber(roomType)
    else:
        try:
            if roomType == 0:
                filt = [('room_type', 0, 'ge')]
            else:
                filt = [('room_type', roomType, 'eq')]
            
            return len(DBUtils.GET('rooms', filt))
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def GetRoomsByType(roomType:int = None):
    """Returns all the room IDs for the given room type. Defaults to returning all rooms

    :param roomType [int]: The ID of the room type
    """
    
    if isLocal:
        return LocalDB.GetRoomsByType(roomType)
    else:
        try:
            if roomType == 0:
                filt = [('room_type', 0, 'ge')]
            else:
                filt = [('room_type', roomType, 'eq')]
            
            data = DBUtils.GET('rooms', filt)
            
            return tuple([i['room_id'] for i in data])
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def AddRoom(roomID, roomType):
    """Adds a new room to the database

    :param roomID: The ID of the room
    :param roomType: The type of the room
    """
    
    if isLocal:
        return LocalDB.AddRoom(roomID, roomType)
    else:
        try:
            payload = {
                'room_id': roomID,
                'roomType': roomType
            }
            return DBUtils.PUT('rooms', payload)
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()

def DeleteRoom(roomID):
    """Deletes a room from the database

    :param conn: The connection object
    :param roomID: The ID of the room to delete
    """
    
    if isLocal:
        return LocalDB.DeleteRoom(roomID)
    else:
        try:
            return DBUtils.DELETE('rooms', [('room_id', roomID, 'eq')])
        except Exception as e:
            DBError(str(e))
            print(e)
            traceback.print_exc()