from application.models import db, User, Show, Theater, Rating, BookingShow
from application.cache import cache

@cache.cached(timeout=300)
def get_all_theater():
    theater_present = Theater.query.all()
    return theater_present

@cache.memoize(timeout=30)
def get_shows_t_id(theater_id):
    shows = Show.query.filter(Show.theater_id == theater_id).order_by(Show.show_added_on.desc()).all()
    return shows

@cache.memoize(timeout=300)
#theater search
def get_theater_t_id(theater_id):
    t_deltails = Theater.query.filter(Theater.id==theater_id).first()
    return t_deltails


def get_booking_details(user_id):
    b_det = BookingShow.query.filter(BookingShow.user_id == user_id)
    b_details = b_det.order_by(BookingShow.booking_time.desc()).all()

    return b_details

