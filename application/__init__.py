import os
import sys
import calendar
import pathlib
import configHandler
from shutil import copyfile
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from UI import FilePath, MainWindow, LoadingWindow, ErrorWindow, MessageBox
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import DB
load_dotenv()
config = configHandler.config

correctLoad = 1
# set up the Qapplication
app = QtWidgets.QApplication(sys.argv)

# create a loading window
loadingW = LoadingWindow('Φόρτωση προγράμματος')
loadingW.show()

# check if the database exists, if not create it
if config['DATABASE']['local_database'] == '1':
    path = config['DATABASE']['database_path']
    DB.db_path = path
    if not os.path.isfile(path):
        DB.CreateDatabase(path)

# check if the last backup is older than five day, if true back up all the data files
if (datetime.strptime(config['DATABASE']['last_backup'], '%Y-%m-%d') + timedelta(5)) < datetime.today():
    try:
        scriptPath = pathlib.Path(__file__).parent.absolute()
        path = pathlib.Path(f'{scriptPath}/backup/data')
        path.mkdir(parents=True, exist_ok=True)
        
        correctLoad = None
        src = f'{scriptPath}/files/data'
        dest = f'{scriptPath}/backup/data'
        src_files = os.listdir(src)
        
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name):
                copyfile(full_file_name, f"{dest}/{file_name}")

        configHandler.writeConfig('DATABASE', 'last_backup', datetime.today().strftime('%Y-%m-%d'))
        correctLoad = 1
    except Exception as e:
        print(e.args)
        MessageBox(title='Error', text='<p style="text-align:left;font-size:18px">Αποτυχία εγγραφής αρχείου', buttons=QMessageBox.Ok)

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
if calendar.isleap(datetime.today().year):
    months['2'] = 29

# if the application loaded correctly continue, otherwise display a message
if correctLoad:
    mWindow = MainWindow(months)
    loadingW.close()
    mWindow.showMaximized()
    app.exec_()
else:
    MessageBox(title='Error', text='<p style="text-align:left;font-size:18px">Αποτυχία φόρτωσης προγράμματος', buttons=QMessageBox.Ok)
    loadingW.close()