import os
import sys
import calendar
from PyQt5 import QtWidgets
from UI import MainWindow
from datetime import datetime
from DB import FindCustomerIDByName, AddCustomer, CreateConnection


os.environ['DATABASE_PATH'] = r"./files/data/database.db"
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