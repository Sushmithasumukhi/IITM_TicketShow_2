import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
# from email.mime.application import MIMEApplication
import os
from datetime import datetime
from jinja2 import Template

from application.models import Show, db, Rating
from sqlalchemy import func

SMTP_SERVER_HOST="localhost"
SMTP_SERVER_PORT=1025
SENDER_ADDRESS='contact@ticketshow.com'
SENDER_PASSWORD=''


#------paths to htmls
DAILY_REMINDER_HTML = os.path.join('templates', 'daily_reminder.html')



def send_email(user_mail,subject,message,file=None):
    
    msg=MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = user_mail
    msg['Subject'] = subject
    
    
    msg.attach(MIMEText(message,"html"))
    if not file==None:
        with open(file, 'rb') as f:

            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(f.read())
            encoders.encode_base64(attach)
            attach.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(attach)

    
    s=smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    # s.set_debuglevel(1)
    # with smtplib.SMTP('localhost',port) as s:
        
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return 'Email sent successfully!!!'


# Daily reminder via mail

def daily_mail(username, email):
    with open(DAILY_REMINDER_HTML) as f:
        
        latest_shows = Show.query.order_by(Show.show_added_on.desc()).limit(4)
        
        popular_shows = db.session.query(Show, func.avg(Rating.rating).label('avg_rating')).join(Rating, Rating.show_id == Show.id).group_by(Show.id).order_by(func.avg(Rating.rating).desc()).limit(4)
        
        template = Template(f.read())
        msg = template.render(username=username, latest_shows=latest_shows, popular_shows=popular_shows)

    day = datetime.today().strftime('%d-%m-%Y')
    sub = f'TicketShow: Daily Reminder for ({day})'



    send_email(email, subject=sub, message=msg)