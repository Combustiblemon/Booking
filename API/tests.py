import os
import pathlib
import requests
from requests import Response
import json
from dotenv import load_dotenv
load_dotenv(f'{pathlib.Path(__file__).parent.absolute()}/.env')


certPath = os.environ['PATH_TO_CERT']

def printResponce(response: Response, verbose=False):
    if verbose:
        print(response.status_code)
        print(response.content)
    else:
        print(response.status_code)
        print(response.json())

def test_room():
    files = {
        'grant_type': (None, 'password'),
        'username': (None, 'main1'),
        'password': (None, 'password'),
        'scope': (None, 'api'),
    }
    
    client_id = "HhBd1k02PCLVdt3g46zLFBzs"
    client_secret = 'BXTlyIPTyuwhlTv3XdYAhuZN8GTFlLkGSzE9uegGlWWzEn9K'
    response = requests.post('https://127.0.0.1:5000/oauth/token', files=files, auth=(client_id, client_secret), verify=certPath)
    
    print(response.status_code, response.json())
    data = response.json()
    
    headers = {
        'Authorization': f'Bearer {data["access_token"]}',
    }
    get_payload = {
        'filters': [
            ('room_type', 69, 'eq')
        ]
    }
    put_payload = {
        'room_type': 54,
        'room_id': 1124
    }
    patch_payload = {
        'room_type': 1160,
        'room_id': 1124,
        'filters': [
            ('room_id', 1124, 'eq')
        ]
    }
    delete_payload = {
        'filters': [
            ('room_id', 1124, 'eq')
        ]
    }
    
    test_url = 'https://127.0.0.1:5000/api/rooms'
    tests = {
        'GET': False,
        'PUT': False,
        'PATCH': False,
        'DELETE': False,
    }
    response = requests.put(test_url, json=json.dumps(put_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    PUT\n\n')
    tests['PUT'] = True if response.status_code == 200 else response.content
    
    response = requests.get(test_url, json=json.dumps(get_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    GET\n\n')
    tests['GET'] = True if response.status_code == 200 else response.content
    
    response = requests.patch(test_url, json=json.dumps(patch_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    PATCH\n\n')
    tests['PATCH'] = True if response.status_code == 200 else response.content
    
    response = requests.delete(test_url, json=json.dumps(delete_payload), headers=headers, verify=certPath)
    printResponce(response, verbose=True)
    print('^^^^^    DELETE\n\n')
    tests['DELETE'] = True if response.status_code == 204 else response.content
    
    print('\n\nRooms test:')
    for k, v in tests.items():
        print(f'    {k}: {v}')

def test_customer():
    files = {
        'grant_type': (None, 'password'),
        'username': (None, 'main1'),
        'password': (None, 'password'),
        'scope': (None, 'api'),
    }
    
    client_id = "HhBd1k02PCLVdt3g46zLFBzs"
    client_secret = 'BXTlyIPTyuwhlTv3XdYAhuZN8GTFlLkGSzE9uegGlWWzEn9K'
    response = requests.post('https://127.0.0.1:5000/oauth/token', files=files, auth=(client_id, client_secret), verify=certPath)
    
    print(response.status_code, response.json())
    data = response.json()
    
    headers = {
        'Authorization': f'Bearer {data["access_token"]}',
    }
    get_payload = {
        'filters': [
            ('room_id', 3, 'eq'),
            ('number_of_people', 4, 'eq'),
            ('booking_type', 2, 'eq')
        ]
    }
    put_payload = {
        'customer_name': "test name", 
        'number_of_people': 4, 
        'check_in': '2021-04-11', 
        'check_out': '2021-04-12', 
        'price_per_night': 420.69,
        'room_id': 3,
        'booking_type': 2,
        'comment': 'test comment',
        'stay_days_number': 4
    }
    patch_payload = {
        'comment': 'i am patched',
        'filters': [
            ('room_id', 3, 'eq'),
            ('number_of_people', 4, 'eq'),
            ('booking_type', 2, 'eq')
        ]
    }
    delete_payload = {
        'filters': [
            ('room_id', 3, 'eq'),
            ('number_of_people', 4, 'eq'),
            ('booking_type', 2, 'eq')
        ]
    }
    
    test_url = 'https://127.0.0.1:5000/api/customers'
    tests = {
        'GET': False,
        'PUT': False,
        'PATCH': False,
        'DELETE': False,
    }
    response = requests.put(test_url, json=json.dumps(put_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    PUT\n\n')
    tests['PUT'] = True if response.status_code == 200 else response.content
    
    response = requests.get(test_url, json=json.dumps(get_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    GET\n\n')
    tests['GET'] = True if response.status_code == 200 else response.content
    
    response = requests.patch(test_url, json=json.dumps(patch_payload), headers=headers, verify=certPath)
    printResponce(response)
    print('^^^^^    PATCH\n\n')
    tests['PATCH'] = True if response.status_code == 200 else response.content
    
    response = requests.delete(test_url, json=json.dumps(delete_payload), headers=headers, verify=certPath)
    printResponce(response, verbose=True)
    print('^^^^^    DELETE\n\n')
    tests['DELETE'] = True if response.status_code == 204 else response.content
    
    print('\n\nCustomers test:')
    for k, v in tests.items():
        print(f'    {k}: {v}')
        
test_room()
test_customer()