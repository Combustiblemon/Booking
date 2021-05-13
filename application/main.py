from datetime import datetime
import sys
import pathlib
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, QDate
from UI import PasswordInputWindow
from PySide6 import QtWidgets
import DBUtils

if __name__ == "__main__":
    d = datetime.today()
    print(d.strftime('%Y-%m-%d'))
    
    