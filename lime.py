import requests
import os
import json
from dotenv import load_dotenv
from set_env import lime_set

load_dotenv()



"""
TODO: Clean up lime_response data and decide what to return.  Need to figure out how to control the radius that matches with bird
"""




def request_new_token():
    url = f'https://web-production.lime.bike/api/rider/v1/login?phone=%2B{os.getenv("LIME_PHONE_NUMBER")}'

    params = {
        "phone" : f"%2B{os.getenv('LIME_PHONE_NUMBER')}"
    }
    print(os.getenv('LIME_PHONE_NUMBER'))
    
    response = requests.get(url)
    print(response.status_code)
    # get verification code from phone
    verification_code = input('Enter verification code: ')

    url = 'https://web-production.lime.bike/api/rider/v1/login' 

    header = {
        'Content-Type': 'application/json' 
    }
    data = {
        "login_code": str(verification_code), "phone": f"+{os.getenv('LIME_PHONE_NUMBER')}"
        }   
    
    response = requests.post(url, headers=header, json=data)

    if response.status_code == 200:
        print('successfully requested new lime token')
        lime_response = response.json()
        # write new lime token to env
        lime_set(lime_response['token'])
        return True
    else:
        print(f"There's a {response.status_code} error with your request in refresh_access_function")
        return False
 

def get_lime():
    """
    Makes API call to get location of lime scooters
    """
    url = "https://web-production.lime.bike/api/rider/v1/views/map"
    headers = {
        "authorization": f"Bearer {os.getenv('LIME_TOKEN')}"
    }
    params = {
        "ne_lat": "52.6",
        "ne_lng": "13.5",
        "sw_lat": "52.4",
        "sw_lng": "13.3",
        "user_latitude": "52.5311",
        "user_longitude": "13.3849",
        "zoom": "16"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        print("sucessfully fetched lime scooters")
        lime_response = response.json()
        print(lime_response['data']['attributes']['bikes'])
        """
        TODO: Clean up lime_response data and decide what to return.  Need to figure out how to control the radius that matches with bird
        """
        return lime_response
    elif response.status_code == 401:
        # if unauthoized, call the request new token function to get a new access token
        print('Unauthorized, requesting new token...')
        if request_new_token():
            get_lime()
    else:
        print(f"There's a {response.status_code} {response.reason} error with your request in get_lime function")
        return False
get_lime()