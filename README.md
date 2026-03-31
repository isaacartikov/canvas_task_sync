# Canvas to Discord Notification Tool for Dual Enrollment
Python-based tool that collects data from two Canvas instances and sends a clear and concise summary through Discord.

I made this because I am taking college-level classes through a community college, and logging in just to check when things are due each time is annoying. Im also rather forgetful, so this helps remind me to do my assignments.
Also, we aren't allowed to have our phones in school. So I couldn't even check my assignments in class if I wanted to.

## Features:
**Multi-Institution Support** ~ Pulls data from multiple school APIs.
**Customizable** ~ Uses a .env file to allow for customization such as timezone, filtering and institution names.
**Time-Dependent Highlighting** ~ Tags tasks as overdue or provides a countdown depending on assignment status. 

## Setup
1. Create a copy of the repo.
2. Create a.env file and copy options from below. Replace tokens with your special 'CANVAS_API_TOKEN' tokens and webhook with 'DISCORD_WEBHOOK_URL'. Replace omitted keywords and local timezone as desired. *IMPORTANT:* Do not share your Canvas API tokens with anybody; they are private.
3. Run `pip install -r requirements.txt`.
4. Create a new task for an automated script runner such as Task Scheduler for Windows and execute as desired.

```text
INSTITUTION_ONE_NAME="School Name One Here"
INSTITUTION_ONE_TOKEN=token_one_here
INSTITUTION_ONE_URL=https://yourschool.instructure.com

INSTITUTION_TWO_NAME="School Name Two Here"
INSTITUTION_TWO_TOKEN=token_two_here
INSTITUTION_TWO_URL=https://yourschool.instructure.com

OMIT_KEYWORD_TASKS=notes,textbook,reading,optional

LOCAL_TIMEZONE="America/Chicago"

DISCORD_WEBHOOK_URL=webhook_here

```