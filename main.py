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

if all_tasks[0]['due_at']: #since all_tasks is sorted, the first index is the earliest due date. 
    first_due_date = datetime.fromisoformat(all_tasks[0]['due_at'].replace("Z", "+00:00")).astimezone(ZoneInfo(os.getenv("LOCAL_TIMEZONE")))
    if first_due_date - now < timedelta(hours=24):
        message_content = provider.generate_report(all_tasks, "Upcoming Canvas Tasks") 
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        
        payload = {
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
    else:
        print("No tasks due within 24 hours, discord message not sent.")