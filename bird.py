from flask import Flask
import requests
import uuid
from dotenv import load_dotenv
import os
from set_env import bird_set
from datetime import datetime
from utils import time_check

load_dotenv()

def refresh_access():
    """
    refreshes your bird access token and generates a new random uuid
    """
    # generates new uuid for device-id in headers
    myuuid = uuid.uuid4()
    # headers needed for bird token refresh
    headers = {
        "User-Agent": "Bird/4.53.0 (co.bird.Ride; build:24; iOS 12.4.1) Alamofire/4.53.0",
        "Device-Id": str(myuuid),
        "Platform": "ios",
        "App-Version": "4.53.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('BIRD_REFRESH')}",
        }
    response = requests.post(f"https://api-auth.prod.birdapp.com/api/v1/auth/refresh/token", headers=headers)
    if response.status_code == 200:
        print("sucessfully fetched new access code")
        bird_response = response.json()
        # calls bird set from set_env.py to set the new env variables
        bird_set(bird_response["access"], bird_response["refresh"], myuuid)
        return True
    else:
        print(f"There's a {response.status_code} error with your request in refresh_access_function")
        return False



def get_bird():
    """
    - Checks if 24 hours have passed since last access token was fetched from the .env file
        - If over 24 hours fetches new acces token with refresh acces function
        - If under 24 hours continues on
    - Makes API call to get location of birds
    """
    # check time since last refresh using time_check function in utils
    if not time_check(1, "BIRD_LAST_REFRESH"):
        if not refresh_access():
            print("Error in bird refresh access")
            return False
    # After time check, request location of birds

    # ==============================Will need to get user lat and long from frontend=========================================

    url = "https://api.birdapp.com/bird/nearby?latitude=47.6061&longitude=122.3328&radius=1000"
    myuuid = uuid.uuid4()
    headers = {
        "Authorization": f"Bird {os.getenv('BIRD_ACCESS')}",
        "Device-id": str(myuuid),
        "App-Version": "4.41.0",
        "Location": str({"latitude":47.6061,"longitude":122.3328,"altitude":500,"accuracy":100,"speed":-1,"heading":-1})
    }
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        print("sucessfully fetched bird scooters")
        bird_response = response.json()
        print(bird_response)
    else:
        print(f"There's a {response.status_code} error with your request in get_bird function")
    
    

get_bird()