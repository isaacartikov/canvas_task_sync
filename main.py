import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_school(label, url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{url}/api/v1/users/self",headers = headers)
        if response.status_code == 200:
            name=response.json().get('name')
            print(f"{label} connection successful, name is: {name}")
        else:
            print(f"{label} connection failed, status:{response.status_code}")
    except Exception as e:
        print(f"{label} Error: {e}")


check_school(os.getenv("INSTITUTION_ONE_NAME"), os.getenv("INSTITUTION_ONE_URL"), os.getenv("INSTITUTION_ONE_TOKEN"))

check_school(os.getenv("INSTITUTION_TWO_NAME"), os.getenv("INSTITUTION_TWO_URL"), os.getenv("INSTITUTION_TWO_TOKEN"))