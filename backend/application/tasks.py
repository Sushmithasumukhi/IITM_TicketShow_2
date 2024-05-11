import os 
import csv
import datetime 
from datetime import datetime, timedelta
from application.email import send_email, daily_mail
from flask import current_app
from application.cache import cache

from celery.schedules import crontab
from flask import current_app, render_template

from application.models import db, User, BookingShow, Rating, Show, Theater
from application.workers import celery


# -----------------

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=00, hour=18, day_of_month='*'),
        DailyReminderMail.s(),
        name = 'Daily reminder everyday @ 6PM via email.'
    )

    sender.add_periodic_task(
        # every 1st day of month at 5 AM
        crontab(day_of_month=1, month_of_year='*' , hour=5 , minute=0),
        sendMonthlyMail.s(),
        name = 'Monthly Entertainment Report at 5AM 1st of every month via email.'
    )

# -----------------


@celery.task
def add_task(a, b):
    return a + b


# 1. DAILY reminder TASKS [Daily Reminder Jobs]
# -----------------------

@celery.task
def sendDailyMail(id):
    user = User.query.filter(User.id == id).first()

    daily_mail(user.username, user.email)
    return f'Reminder sent successfully via EMAIL {user.email}'


@celery.task
def DailyReminderMail():
    users = User.query.filter(User.roles.any(name='user')).all()
    

    twenty_four_hours_before = datetime.now() - timedelta(days=1)

    for u in users:
        last_booking = BookingShow.query.filter(BookingShow.user_id == u.id).order_by(BookingShow.booking_time.desc()).first()

        if not last_booking or last_booking.booking_time < twenty_four_hours_before :
            sendDailyMail.delay(u.id)

    return 'Daily Reminder sent successfully via EMAIL'



# 2. MONTHLY mail - tasks [Scheduled Job - Monthly Engagement Report]


@celery.task
def sendMERMail(id, email):

    current_date = datetime.today()
    first_day_prev_month = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_prev_month = current_date.replace(day=1) - timedelta(days=1)

    user = User.query.filter(User.id == id).first()
    if user and 'user' in [role.name for role in user.roles]:
        user_bookings = BookingShow.query.filter(BookingShow.user_id == id, BookingShow.booking_time >= first_day_prev_month, BookingShow.booking_time <= last_day_prev_month).all() 
    else:
        pass
    data = []
    for bookings in user_bookings:
        prev_month = datetime.now().replace(day=1) - timedelta(days=1)  #use prev_month.month in if to get update of previous month.
        # if bookings.booking_time.month == datetime.now().month:

        ratings = Rating.query.filter(Rating.show_id == bookings.show_booked.id).all()
        if len(ratings)>0:
            tot_rting = sum(r.rating for r in ratings)
            avg_rating = tot_rting/len(ratings)
            round_avg_rating = round(avg_rating,2)
        else:
            round_avg_rating = 0.00
        
        show = Show.query.get(bookings.show_id)
        user_rating = Rating.query.filter(Rating.u_id==id, Rating.show_id == show.id).first()
        if user_rating:
            u_rating = user_rating.rating
        user_rating = 0.00

        data.append({
                    'show_seen' : bookings.show_booked.show_name,
                    'theater_booked': bookings.show_booked.theater.theater_name,
                    'rating_provided_by_user' : u_rating,
                    'shows_ratings' : round_avg_rating,
                })
            # print(bookings.show_booked.show_name)
    message = render_template('MER.html', 
                                    username=user.username, 
                                    data = data
                                )
    
    month = datetime.today().strftime('%B-%Y')
    subject = f'TicketShow : Monthly Entertainment Report for {month}'

    send_email(user.email, subject=subject, message=message)

    return f'Monthly review email sent to {user.email}'




@celery.task
def sendMonthlyMail():
    users = User.query.filter(User.roles.any(name='user')).all()
    for user in users:
        sendMERMail.delay(user.id, user.email)

    return 'Monthly mail has been sent.'



#  3. EXPORT tasks [User Triggered Async Job - Export as CSV]
#  ----------------

def genererate_csv(id):
    s_list = []

    header_fields = ['id','shows','theater','genre','ticket_price','ratings','available_tickets','date','time','booked_tickets','tot_earning']
    s_list.append(header_fields)

    theater = Theater.query.get(id)
    if theater:
        shows_in_theater = Show.query.filter(Show.theater_id==theater.id).all()

        for show in shows_in_theater:
            id = show.id
            show_name = show.show_name
            theater_name = theater.theater_name
            genre = show.tags
            tik_price = show.price
            available_tik = theater.seat_capacity - show.seat_booked
            tik_booked = show.seat_booked
            time_of_show = show.show_time
            total_earning = float(tik_booked)*float(tik_price)

            ratings_of_show = Rating.query.filter(Rating.show_id==show.id).all()
            if not ratings_of_show:
                round_avg_rating = 0.00
            if len(ratings_of_show)>0:
                totrating =  sum(r.rating for r in ratings_of_show)
                avg_rating = totrating/len(ratings_of_show)
                round_avg_rating = round(avg_rating,2)


            row = [id,show_name,theater_name,genre,tik_price,round_avg_rating,available_tik,time_of_show,tik_booked,total_earning]
            s_list.append(row)

    return s_list
        
        

@celery.task
def export_csv(id):
    with current_app.app_context():

        theater = Theater.query.filter(Theater.id == id).first()

        if theater:

            csv_file = genererate_csv(theater.id)

            file_name = f'{theater.theater_name}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.csv'

            csv_path = os.path.join('static/CSV', file_name)
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            print('THEATER CSV FILE IS SAVED')

            with open(csv_path,'a+', newline='') as f:
                csvwrite = csv.writer(f)
                csvwrite.writerows(csv_file)
            
            f.close()

            message= render_template('exportNotif.html', csv_path = csv_path, theater_name = theater.theater_name, file_name = file_name)

            subject = f'Export CSV notification'
            send_email(theater.user.email, subject, message, csv_path)
        
        else:
            pass

    return {'status':'success', 'message':'CSV created'}




