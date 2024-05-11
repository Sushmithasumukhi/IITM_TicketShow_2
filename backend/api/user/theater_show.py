from flask_restful import Resource
from flask import request
from flask_security import  auth_required
from application.models import  Show, Theater
# from application.cache import cache
from application.data_access import get_all_theater, get_shows_t_id
import os

class Theater_Show(Resource):
    @auth_required('token')
    # @cache.cached(timeout=30)
    def get(self):
        theater_present = get_all_theater()
        shows_in_respective_theater = []

        for t in theater_present:
            t_details = {
                'theater_id' : t.id,
                'theater_name': t.theater_name,
                'location': t.location,
                't_place': t.t_place,
                'seat_capacity':t.seat_capacity,
                'shows_present': []
            }  
            shows = get_shows_t_id(t.id)
            #t.shows
            for s in shows:
                s_details = {
                    'id':s.id,
                    'show_name':s.show_name,
                    'tags': s.tags.split(','),
                    'm_image':f"{request.host_url}static/shows/{os.path.split(s.m_image)[-1]}" if s.m_image else None,
                }

                t_details['shows_present'].append(s_details)

            shows_in_respective_theater.append(t_details)

        return shows_in_respective_theater
