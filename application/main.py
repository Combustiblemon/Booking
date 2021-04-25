import sys
import pathlib
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, QDate

if __name__ == "__main__":
    a = ('test1', 'test2')
    b = [a]
    
    c = [list(i) for i in b]
    print(c)
    