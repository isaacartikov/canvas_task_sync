# Canvas to Discord/Email Notification Tool
Python-based tool that collects data from two Canvas instances and sends a clear and concise reminder through Discord/email.

I made this because I'm taking classes through both a high-school and a community college, and logging in to each just to check when things are due each time is annoying. 
Also, we aren't allowed to have our phones in school. So I couldn't even check my CC assignments in class if I wanted to, because to log in, you need to use an authenticator only available on a phone.

## Features:
**Multi-Institution Support** ~ Pulls data from multiple school APIs.
**Customizable** ~ Uses a .env file to allow for customization such as timezone, filtering and institution names.
**Time-Dependent Highlighting** ~ Tags tasks as overdue or provides a countdown depending on assignment status. Pings Discord user if user ID is provided and a task is overdue/urgent.

## Setup
1. Create a copy of the repo.
2. Create a.env file and copy options from below. Replace tokens with your special 'CANVAS_API_TOKEN' tokens, webhook with 'DISCORD_WEBHOOK_URL' and/or gmail account password (2FA on google account required). Try deleting spaces between your app password if the email wont send. *IMPORTANT:* Do not share your Canvas API tokens, your Discord User ID, or your mail token with anybody; they are private.
3. Replace omitted keywords, local timezone and hour of the reminder in military time (0-23, e.g., 8 for 8 AM, 17 for 5 PM).
4. Run `pip install -r requirements.txt`.
5. Create a new task for an automated script runner such as Task Scheduler for Windows and/or execute main.

## Usage
To start the code, run python main.py
```properties
INSTITUTION_ONE_NAME="School Name One Here"
INSTITUTION_ONE_TOKEN=token_one_here
INSTITUTION_ONE_URL=https://yourschool.instructure.com
INSTITUTION_TWO_NAME="School Name Two Here"
INSTITUTION_TWO_TOKEN=token_two_here
INSTITUTION_TWO_URL=https://yourschool.instructure.com

OMIT_KEYWORD_TASKS=notes,textbook,reading,optional

LOCAL_TIMEZONE="America/Chicago"

DISCORD_WEBHOOK_URL=webhook_here
DISCORD_USER_ID=id_here

EMAIL_SENDER=youraccount@example.com
EMAIL_RECEIVER=youraccount@example.com
EMAIL_APP_PASSWORD=16_digit_code_here

EMAIL_REMINDER_TIME=8
DISCORD_REMINDER_TIME=17
```