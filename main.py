import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import notifiers
import provider
from datetime import timedelta,datetime

import report_generator
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
    ping_msg=f"<@{os.getenv('DISCORD_USER_ID')}>, you have assignments that are overdue/due within 24 hours." #ping the user if there are any tasks due within 24 hours.
if now.hour==8:
    notifiers.send_email_message(report_generator.generate_report(all_tasks,"Email"))
elif now.hour==17:
    notifiers.send_discord_message(report_generator.generate_report(all_tasks,"Discord"), ping_msg)