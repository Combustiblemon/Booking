import os
import sys
import calendar
import configparser
from shutil import copyfile
from PyQt5 import QtWidgets
from UI import MainWindow, LoadingWindow, ErrorWindow
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from DB import CreateDatabase
load_dotenv()
config = configparser.ConfigParser()

correctLoad = 1
# set up the Qapplication
app = QtWidgets.QApplication(sys.argv)

# create a loading window
loadingW = LoadingWindow('Φόρτωση προγράμματος')
loadingW.show()

# check if the database exists, if not create it
if not os.path.isfile('./files/data/database.db'):
    CreateDatabase()

# check if the last backup is older than five day, if true back up all the data files
config.read('config.ini')
if (datetime.strptime(config['DATABASE']['last_backup'], '%Y-%m-%d') + timedelta(5)) < datetime.today():
    try:
        correctLoad = None
        src = './files/data'
        dest = './backup/data'
        src_files = os.listdir(src)
        
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name):
                copyfile(full_file_name, f"{dest}/{file_name}")
                
        config['DATABASE']['last_backup'] = datetime.today().strftime('%Y-%m-%d')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            correctLoad = 1
    except Exception as e:
        print(e)
        errorW1 = ErrorWindow(f'Αποτυχία εγγραφής αρχείου.\n{e}')
        errorW1.show()

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
    errorW = ErrorWindow('Αποτυχία φόρτωσης προγράμματος')
    loadingW.close()
    app.exec_()