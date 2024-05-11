from flask_restful import Resource
from flask import request
from flask_security import auth_required
from application.models import Show, Theater

import os



class Show_Search(Resource):
    @auth_required('token')
    
    def get(self):
        
        query = request.args.get('query')

        shows = Show.query.filter((Show.show_name.ilike(f'%{query}%')) |
                                  (Show.tags.ilike(f'%{query}%'))).all()
        

        if not shows:
            return {'message':'No shows found'}

       
        return [{
            'id':s.id,
            'show_name':s.show_name,
            'tags': s.tags.split(','),
            'm_image':f"{request.host_url}static/shows/{os.path.split(s.m_image)[-1]}" if s.m_image else None,
            'theater':{
                'id':s.id,
                'theater_name':s.theater.theater_name,
                't_place':s.theater.t_place,
                'location':s.theater.location
            }
        } for s in shows],200

    

class Theater_Search(Resource):
    @auth_required('token')
    def get(self):
        
        query = request.args.get('query')

        theaters = Theater.query.filter((Theater.theater_name.ilike(f'%{query}%')) | (Theater.location.ilike(f'%{query}%')) |  (Theater.t_place.ilike(f'%{query}%'))).all()
        if not theaters:
            return {'message':'No theaters found'}
        
        return [{
            'id':t.id,
            'theater_name':t.theater_name,
            't_place':t.t_place,
            'location':t.location
        } for t in theaters],200

