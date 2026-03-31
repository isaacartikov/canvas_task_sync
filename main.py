import os
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv
import provider
from datetime import timedelta,datetime
load_dotenv()

provider.check_school(os.getenv("INSTITUTION_ONE_NAME"), os.getenv("INSTITUTION_ONE_URL"), os.getenv("INSTITUTION_ONE_TOKEN"))
provider.check_school(os.getenv("INSTITUTION_TWO_NAME"), os.getenv("INSTITUTION_TWO_URL"), os.getenv("INSTITUTION_TWO_TOKEN"))

Canvas_provider_one = provider.CanvasProvider(os.getenv("INSTITUTION_ONE_NAME"), os.getenv("INSTITUTION_ONE_URL"), os.getenv("INSTITUTION_ONE_TOKEN"))
Canvas_provider_two = provider.CanvasProvider(os.getenv("INSTITUTION_TWO_NAME"), os.getenv("INSTITUTION_TWO_URL"), os.getenv("INSTITUTION_TWO_TOKEN"))

all_tasks = Canvas_provider_one.get_upcoming_tasks() + Canvas_provider_two.get_upcoming_tasks()
all_tasks.sort(key=lambda x: x['due_at'] if x['due_at'] else '9999') # Sort by due date, placing tasks without a due date at the end



now = datetime.now(ZoneInfo(os.getenv("LOCAL_TIMEZONE")))

utc_time = datetime.strptime(all_tasks[0]['due_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")) #Parse UTC String
local_time = utc_time.astimezone(ZoneInfo(os.getenv("LOCAL_TIMEZONE"))) #Set timezone from .env
ping_msg=""
if local_time-now<timedelta(days=1):
    ping_msg=f"<@{os.getenv('DISCORD_USER_ID')}>, Tasks due within 24 hours!" #ping the user if there are any tasks due within 24 hours.


message_content = provider.generate_report(all_tasks, "Upcoming Canvas Tasks") 
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

payload = {
    "content": ping_msg,
    "embeds": [
            {
                "title": "Assignment Report",
                "description": message_content,
                "color": 10181046 # decimal code for Purple, you can change this to any color you like by using a different decimal code.
            }
        ]
    }
response = requests.post(webhook_url, json=payload)
if response.status_code == 204:
    print("Message sent")
else:
    print(f"Failed to send. Error: {response.status_code}")