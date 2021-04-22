import smtplib
from datetime import date
from email.message import EmailMessage
from os import remove

from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from pdf_generator import create_pdf


def send_email(data):
    today = date.today().strftime('%Y-%m-%d')

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = data["email"]
    msg['Subject'] = 'Attendance Report: ' + today
    msg.set_content('Please find the Attendance List for ' + today + ", of your class attached below\n- Verbose")

    create_pdf(data["id"], data["data"])

    with open("Student Daily Attendance Records.pdf", 'rb') as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = data["id"] + " " + today + ".pdf")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    remove("Student Daily Attendance Records.pdf")
