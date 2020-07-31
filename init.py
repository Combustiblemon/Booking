import os
import sys
import calendar
from PyQt5 import QtWidgets
from UI import MainWindow
from datetime import datetime
from DB import FindCustomerIDByName, AddCustomer, CreateConnection


os.environ['DATABASE_PATH'] = r"./files/data/IliaAppartments.db"
conn = CreateConnection(os.environ['DATABASE_PATH'])
cur = conn.cursor()
""" cur.execute('SELECT * FROM customers WHERE CustomerName = "notName" ORDER BY 1')
rows = cur.fetchall()
for row in rows:
    print(row) """

customerID = FindCustomerIDByName(conn, 'TestName')
print(customerID)

customer = ['TestName', 4, '2020-7-31', '2020-8-5', 60, 3]
""" for i in range(0, 5):
    customer[4] += 10
    AddCustomer(conn, customer) """
conn.close()

# set up the Qapplication
app = QtWidgets.QApplication(sys.argv)

# setup the month to date dictionary
months = {'1': 31,
          '2': 28,
          '3': 31,
          '4': 30,
          '5': 31,
          '6': 30,
          '7': 31,
          '8': 31,
          '9': 30,
          '10': 31,
          '11': 30,
          '12': 31}

# if the year is a leap year add a day to february
if calendar.isleap(int(datetime.today().strftime('%y'))):
    months['2'] = 29

# get the current date in YYYY-MM-DD
month = int(datetime.today().strftime('%m'))

# print(month)

""" mWindow = MainWindow(months)
mWindow.show()
app.exec_() """