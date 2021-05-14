import json
from operator import truediv
import requests
import configHandler
from PySide6 import QtWidgets, QtCore
from files.UI import ui_PasswordWindow, ui_ErrorWindow

config = configHandler.getConfig()

username = None
password = None

client_id = None
client_secret = None
url = config['CLIENT']['url']
cert_path = config['CLIENT']['cert_path']
access_token = None

def getClientData():
    global username, password
    # keep asking for the login details as long as they are not valid
    while not username or not password:
        username, password = getLoginDetails()

        headers = {
            'username': username,
            'password': password,
            'API_REQUEST': 'True'
        }
        
        try:
            response = requests.post(f'{url}', headers=headers, verify=cert_path)
            data = response.json()
            
            # unpack the dict keys and check for the error messages
            # if there is an error set login details to None and try again
            dKeys = [*data]
            if 'ERROR_USERNAME' in dKeys:
                username = password = None
                continue
            
            if 'ERROR_PASSWORD' in dKeys:
                username = password = None
                continue
            
            # after successful login set the client_id and client_secret globals
            global client_id, client_secret
            client_id = data['client_id']
            client_secret = data['client_secret']
            
            return (data['client_id'], data['client_secret'])
        except requests.exceptions.ConnectionError:
            w = ErrorWindow('Αποτυχία σύνδεσης με την βάση δεδομένων!')
            w.show()
            continue

def getAccessToken() -> str:
    global client_id, client_secret
    # keep asking for the client data as long as there's no data saved
    while not client_id or not client_secret:
        data = getClientData()
        
        
    files = {
        'grant_type': (None, 'password'),
        'username': (None, username),
        'password': (None, password),
        'scope': (None, 'api'),
    }
    
    try:
        response = requests.post(f'{url}oauth/token', files=files, auth=(client_id, client_secret), verify=cert_path)
        data = response.json()
        return data["access_token"]
    except requests.exceptions.ConnectionError:
        w = ErrorWindow('Αποτυχία σύνδεσης με την βάση δεδομένων!')
        w.show()
        return

def GET(route: str, filters: list):
    global access_token
    # keep asking for the client data as long as there's no data saved
    while not access_token:
        access_token = getAccessToken()
   
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        'filters': filters
    }
        
    response = requests.get(f'{url}api/{route}', json=json.dumps(payload), headers=headers, verify=cert_path)
    if response.status_code == 200:
        return response.json()
    print(response.text)
    return False

def PUT(route: str, payload: dict):
    global access_token
    # keep asking for the client data as long as there's no data saved
    if not access_token:
        access_token = getAccessToken()
   
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    print(json.dumps(payload))
    response = requests.put(f'{url}api/{route}', json=json.dumps(payload), headers=headers, verify=cert_path)
    if response.status_code == 200:
        return response.json()
    return False

def PATCH(route: str, payload: dict):
    global access_token
    # keep asking for the client data as long as there's no data saved
    while not access_token:
        access_token = getAccessToken()
   
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
        
    response = requests.patch(f'{url}api/{route}', json=json.dumps(payload), headers=headers, verify=cert_path)
    if response.status_code == 200:
        return response.json()
    return False

def DELETE(route: str, filters: list):
    global access_token
    # keep asking for the client data as long as there's no data saved
    while not access_token:
        access_token = getAccessToken()
   
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    payload = {
        'filters': filters
    }
        
    response = requests.delete(f'{url}api/{route}', json=json.dumps(payload), headers=headers, verify=cert_path)
    if response.status_code == 204:
        return True
    return False

# UI elements here to avoid circular import from UI module
class PasswordInputWindow(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(PasswordInputWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_PasswordWindow.Ui_PasswordWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.usernameInput = self.findChild(QtWidgets.QLineEdit, "usernameInput")
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, "passwordInput")
        
    def GetData(self) -> tuple:
        """returns the user input (username, password)
        """
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return (self.usernameInput.text().strip(), self.passwordInput.text().strip())
        
def getLoginDetails() -> tuple:
    window = PasswordInputWindow()
    data = window.GetData()
        
    if data:
        return data
    
class ErrorWindow(QtWidgets.QDialog):
    def __init__(self, text, title="Error"):
        super(ErrorWindow, self).__init__()
        # Load the main UI file
        self.ui = ui_ErrorWindow.Ui_ErrorWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)