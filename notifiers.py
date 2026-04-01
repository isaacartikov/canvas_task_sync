import os
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def send_discord_message(message_content, ping_msg):
    if not message_content:
        print("DEBUG: message_content was EMPTY. Skipping send.")
        return
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
def send_email_message(message_content):
    if not message_content:
        print("DEBUG: message_content was EMPTY. Skipping send.")
        return
    msg = EmailMessage()
    msg.set_content(message_content)
    msg['Subject'] = 'Canvas Assignment Email Report'
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECEIVER")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: #Using Gmail's SMTP server
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_APP_PASSWORD")) #Login with email account and app password (you need to set this up in your Gmail account for security reasons)
            smtp.send_message(msg) 
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
