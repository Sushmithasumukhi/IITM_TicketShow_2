from flask_restful import Resource
from flask import request
from flask_security import SQLAlchemyUserDatastore, current_user, auth_required
from application.models import db, User, Role, Show, Rating, Theater
from application.validation import NotFoundError
from application.cache import cache
from application.data_access import get_theater_t_id

import os

datastore = SQLAlchemyUserDatastore(db, User, Role)



class DisplayShows(Resource):
    @auth_required('token')
    @cache.cached(timeout=300)

    def get(self,id):
        shows_display = Show.query.filter(Show.id==id).first()
        if not shows_display:
            return {'message':'Show doesnt exist'},404
        
        ratings_of_show = Rating.query.filter(Rating.show_id==id).all()
        if not ratings_of_show:
            round_avg_rating = 0.00
        if len(ratings_of_show)>0:
            totrating =  sum(r.rating for r in ratings_of_show)
            avg_rating = totrating/len(ratings_of_show)
            round_avg_rating = round(avg_rating,2)

        seats_available = shows_display.theater.seat_capacity - shows_display.seat_booked
        print(seats_available)
        ratings_in_order = Rating.query.filter(Rating.show_id==id).order_by(Rating.r_timestamp.desc()).all()

        # print(avg_rate)

        reviews = []
        for r in ratings_in_order:
            user = User.query.get(r.u_id)
            reviews.append({
                'id':r.id,
                'username':user.username,
                'rating':r.rating,
                'review':r.review,
                'date': r.r_timestamp.isoformat()
            })

        return {
            'id':shows_display.id,
            'show_name':shows_display.show_name,
            'm_image':f"{request.host_url}static/shows/{os.path.split(shows_display.m_image)[-1]}" if shows_display.m_image else None,
            'show_time':shows_display.show_time,
            'show_ratings':round_avg_rating,
            'show_added_on':shows_display.show_added_on.isoformat(),
            'price':shows_display.price,
            'description':shows_display.description,
            'tags':shows_display.tags,
            'theater_id':shows_display.theater_id,
            'seats_available': seats_available,
            'user_id':current_user.id,
            'reviews':reviews
        }
    
class TheaterDetails(Resource):
    @auth_required('token')
    @cache.cached(timeout=300)
    def get(self,t_id):
        t_deltails = get_theater_t_id(t_id)
        if not t_deltails:
            raise NotFoundError(401,'NF1001','Theater doest exist')
        return [{
            'id': s.id,
            'show_name': s.show_name,
            'tags': s.tags,
            'm_image':f"{request.host_url}static/shows/{os.path.split(s.m_image)[-1]}" if s.m_image else None,
            'theater': {
                'id': t_deltails.id,
                'theater_name': t_deltails.theater_name,
                'location': t_deltails.location,
                't_place': t_deltails.t_place,
            }
        } for s in t_deltails.shows],200

    
        