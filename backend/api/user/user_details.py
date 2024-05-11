from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_security import current_user, auth_required
from application.models import db, User, Show, Rating
from application.cache import cache
from application.validation import NotFoundError, UnAuthorizedError
import os

class UserDetails(Resource):

    @auth_required('token')
    # @auth_required('user')

    @cache.cached(timeout=30)

    def get(self,u_id):
        usr_details = User.query.filter(User.id == current_user.id).first()

        if not usr_details:
            raise NotFoundError(404,'NF1001','User doesnt exist')
        
        if u_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')
        

        reviews = []
        ratings = Rating.query.filter(Rating.u_id == usr_details.id).order_by(Rating.r_timestamp.desc()).all()
        for r in ratings:
            show = Show.query.filter(Show.id == r.show_id).all()
            for s in show:
                reviews.append({
                        'id':s.id,
                        'show_name':s.show_name,
                        'm_image':f"{request.host_url}static/shows/{os.path.split(s.m_image)[-1]}" if s.m_image else None, 
                        'review':r.review,
                        'date': r.r_timestamp.isoformat(),
                        'rating':r.rating,
                        'rate_id':r.id
                    })
                
        if len(reviews) == 0:
            return {'message': 'No reviews given...'}

        return {
            'id':usr_details.id,
            'username':usr_details.username,
            'email':usr_details.email,
            'reviews': reviews,
        },200
