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

discord_hour=int(os.getenv("DISCORD_REMINDER_TIME" ) or "18".strip() or "18") 
email_hour=int(os.getenv("EMAIL_REMINDER_TIME") or "8".strip() or "8") 

print(f"DEBUG: System Hour: {now.hour} | Target Email Hour: {email_hour} | Target Discord Hour: {discord_hour}")

if local_time-now<timedelta(days=1) and os.getenv("DISCORD_USER_ID"): 
    ping_msg=f"<@{os.getenv('DISCORD_USER_ID')}>, you have assignments that are overdue/due within 24 hours." 

    
if now.hour==email_hour: #Send email at the specified time, but can be set in .env
    if (not os.getenv("EMAIL_SENDER") or not os.getenv("EMAIL_APP_PASSWORD") or not os.getenv("EMAIL_RECEIVER")):
        print(f"SENDER: {os.getenv('EMAIL_SENDER')}, PASS: {os.getenv('EMAIL_APP_PASSWORD')}, RCV: {os.getenv('EMAIL_RECEIVER')}")
    else:
        notifiers.send_email_message(report_generator.generate_report(all_tasks,False))
        print ('Email message sent.')

if now.hour==discord_hour: #Ping at the specified time, but can be set in .env
    if (not os.getenv("DISCORD_WEBHOOK_URL")):
        print("DISCORD_WEBHOOK_URL not set, skipping Discord notification.")
    else:
        notifiers.send_discord_message(report_generator.generate_report(all_tasks,True), ping_msg)
        print("Discord message sent.")
