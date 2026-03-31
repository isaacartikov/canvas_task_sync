
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def generate_report(all_tasks, output):
    if output=="Discord":
        large_header="#"
        smaller_header="##"
        smallest_header="###"
    omit_keywords=[] 
    keywords=os.getenv("OMIT_KEYWORD_TASKS")
    if keywords: # Check if the user has provided any keywords from .env to omit.
        omit_keywords=[word.strip().lower() for word in keywords.split(",")]
    tasks_omitted=0

    message_content=f"\n{large_header} Upcoming Canvas Tasks from {os.getenv('INSTITUTION_ONE_NAME')} and {os.getenv('INSTITUTION_TWO_NAME')}:\n\n"
    print(f"\n {len(all_tasks)} tasks found.\n") 

    stopped_early=False
    for task in all_tasks:
        if any([keyword in task['title'].lower() for keyword in omit_keywords]):
            tasks_omitted+=1
            continue
        if(len(message_content)>1900): # Discord has a 2000 character limit for messages, so we stop adding tasks if we are close to that limit.
            stopped_early=True
            break
        school_name = task['school']
        course_name = task['course']

        utc_time = datetime.strptime(task['due_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")) #Parse UTC String
        local_time = utc_time.astimezone(ZoneInfo(os.getenv("LOCAL_TIMEZONE"))) #Set timezone from .env
        due_string = local_time.strftime('%A, %b %d at %I:%M %p') #Format message
        now = datetime.now(ZoneInfo(os.getenv("LOCAL_TIMEZONE")))
        time_left=local_time-now

        if time_left<timedelta(0):
            overdue=True
            due_string += " (OVERDUE)"
        elif time_left<timedelta(days=1):
            due_string += f" (in {time_left.seconds//3600} hours and {(time_left.seconds//60)%60} minutes)"
            
        message_content += f"{smaller_header} {school_name} ~ {course_name}\n"
        message_content += f"     {task['title']}\n"
        message_content += f"     Due: `{due_string}`\n\n"
    message_content += f"{tasks_omitted} tasks omitted based on pre-set keywords.\n"
    print(f"{tasks_omitted} tasks omitted based on pre-set keywords.\n")
    if (stopped_early):
        message_content += "Message truncated due to Discord character limit. Please check your Canvas accounts for the full list of tasks."
        print("Message truncated")
    message_content += f"{smallest_header} -- End of Message --"
    return message_content