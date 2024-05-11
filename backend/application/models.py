#KORAGAJJA

from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime


db=SQLAlchemy()


# -----------------------------------------------------------Models------------------------------------------------------------------


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String , unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    ad_shows = db.relationship('Theater', backref='user', cascade='all, delete', lazy='subquery')
    bookings = db.relationship('BookingShow', backref='user_booking', cascade="all, delete",lazy='subquery')
    ratings_given = db.relationship('Rating', backref='user_rating', cascade="all, delete",lazy='subquery')


class Theater(db.Model):
    __tablename__='theater'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    theater_name = db.Column(db.String, nullable=False)
    t_place = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    seat_capacity = db.Column(db.Integer)
    # Theater <1-n> Show
    shows = db.relationship('Show', backref='theater', cascade='all, delete', lazy='subquery')
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Show(db.Model, UserMixin):
    __tablename__='show'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    show_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)  #genre
    price = db.Column(db.String, nullable=False)    
    m_image = db.Column(db.String, nullable=False)
    show_time = db.Column(db.String(50))
    show_added_on = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now)
    seat_booked = db.Column(db.Integer, default=0)

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    # show <1-n> booking
    # show <1-n> ratings
    s_ratings = db.relationship('Rating',backref='show_rating', cascade='all, delete',lazy='subquery')
    s_booking = db.relationship('BookingShow',backref='show_booked',cascade='all, delete',lazy='subquery')



class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    r_timestamp = db.Column(db.DateTime(timezone=True), default=datetime.now)
    review = db.Column(db.Text)

    b_id = db.Column(db.Integer, db.ForeignKey('bookingshow.id'), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    # theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)


class BookingShow(db.Model):
    __tablename__ = 'bookingshow'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    show_id = db.Column(db.Integer, db.ForeignKey('show.id'),nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    num_of_tickets = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime(timezone=True), default=datetime.now)
    
    tot_cost = db.Column(db.Float)
    
    b_ratings = db.relationship('Rating',backref='booking_rating', cascade='all, delete',lazy='subquery')
