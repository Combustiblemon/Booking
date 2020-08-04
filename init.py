import os
import sys
import calendar
from PyQt5 import QtWidgets
from UI import MainWindow, LoadingWindow, ErrorWindow
from datetime import date, datetime
from dotenv import load_dotenv
load_dotenv()


# os.environ['DATABASE_PATH'] = r"./files/data/database.db"
correctLoad = 1
# set up the Qapplication
app = QtWidgets.QApplication(sys.argv)

# create a loading window
loadingW = LoadingWindow('Φόρτωση προγράμματος')
loadingW.show()

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
if calendar.isleap(int(datetime.today().strftime('%Y'))):
    months['2'] = 29

# if the application loaded correctly continue, otherwise display a message
if correctLoad:
    mWindow = MainWindow(months)
    loadingW.close()
    mWindow.showMaximized()
    
    # little Easter egg for my girlfriend
    if datetime.today().strftime('%m-%d') == '11-09':
        EG = ErrorWindow("Χρόνια πολλά μωάκι <3 <3 <3 \n (´▽`ʃ❤ƪ)", "o(^▽^)o")
        EG.show()
    app.exec_()
else:
    errorW = ErrorWindow('Αποτυχία σύνδεσης με βάση δεδομένων!')
    loadingW.close()
    errorW.show()
    app.exec_()