from email.message import EmailMessage
import smtplib
import time
import emailer_config as config

EMAIL_ADDRESS = config.EMAIL_ADDRESS
EMAIL_PASSWORD = config.PASSWORD

def send_email():
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'mikesdgreat@gmail.com'
    msg['Subject'] = 'Attendance Report!'
    msg.set_content('Attached below is the PDF of the Student Attendance Report.')

    with open("pdfTable.pdf", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
