import time
import smtplib
#from picamera import PiCamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def mail_code():
    SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
    SMTP_PORT = 587 #Server Port (don't change!)
    GMAIL_USERNAME = 'openlabids@gmail.com' #change this to match your gmail account
    GMAIL_PASSWORD = 'rmnwqvxmqjojgdzx'  #change this to match your gmail password
    
    class Emailer:
        def sendmail(self, recipient, subject, content, image):

            #Create Headers
            emailData = MIMEMultipart()
            emailData['Subject'] = subject
            emailData['To'] = recipient
            emailData['From'] = GMAIL_USERNAME

            #Attach our text data
            emailData.attach(MIMEText(content))

            #Create our Image Data from the defined image
            imageData = MIMEImage(open(image, 'rb').read(), 'jpg')
            imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
            emailData.attach(imageData)

            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()

            #Login to Gmail
            session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

            #Send Email & Exit
            session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
            session.quit
        
    image = 'image.png'
    sender = Emailer()
    sendTo = 'gokuldharan2001@gmail.com'
    emailSubject = "Intruder Detected!"
    emailContent = "Intruder has been detected at: " + time.ctime()
    sender.sendmail(sendTo, emailSubject, emailContent, image)
    print("Email Sent")
    time.sleep(0.1)