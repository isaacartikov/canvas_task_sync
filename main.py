import os
import requests
from dotenv import load_dotenv
import provider
from datetime import datetime

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

Canvas_provider_one = provider.CanvasProvider(os.getenv("INSTITUTION_ONE_NAME"), os.getenv("INSTITUTION_ONE_URL"), os.getenv("INSTITUTION_ONE_TOKEN"))
Canvas_provider_two = provider.CanvasProvider(os.getenv("INSTITUTION_TWO_NAME"), os.getenv("INSTITUTION_TWO_URL"), os.getenv("INSTITUTION_TWO_TOKEN"))

all_tasks = Canvas_provider_one.get_upcoming_tasks() + Canvas_provider_two.get_upcoming_tasks()
all_tasks.sort(key=lambda x: x['due_at'] if x['due_at'] else '9999')
print(f"\n {len(all_tasks)} tasks found.\n")
for task in all_tasks:
    school_name = task['school']
    course_name = task['course']
    time = datetime.strptime(task['due_at'], "%Y-%m-%dT%H:%M:%SZ")
    print(f"{school_name} ~ {course_name}")
    print(f"   {task['title']}")
    print(f"   Due: {time.strftime('%A, %b %d at %I:%M %p')}\n")
