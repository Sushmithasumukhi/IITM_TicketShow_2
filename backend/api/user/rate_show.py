from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_security import current_user, auth_required, roles_required
from application.models import db, User, Role, Show, Theater, Rating
from application.validation import NotFoundError, UnAuthorizedError, BusinessValidationError



rate_show = reqparse.RequestParser()
rate_show.add_argument('rating', type=int, required=True)
rate_show.add_argument('review', type=str, required=True)


class ShowRating(Resource):
    @auth_required('token')
    @roles_required('user')

    def post(self,u_id,t_id,s_id,b_id):  
        show_det = Show.query.get(s_id)
        
        if u_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')
        
        if not show_det:
            raise NotFoundError(404,'NF1001','Show doesnt exist')
        
        exist_rting = Rating.query.filter(Rating.b_id==b_id, Rating.u_id == u_id).first()
        if exist_rting:
            return {'message': 'You have already rated the show'},400

        args = rate_show.parse_args()
        rating = args.get('rating')
        review = args.get('review')

        if rating <=0 and rating > 10:
            return {'message': 'Rate the show between 1 to 10'},405


        rating_entry = Rating(rating=rating,review=review,u_id=u_id,show_id=s_id,b_id=b_id)  #

        db.session.add(rating_entry)
        db.session.commit()
        print('---------------Show review successfully done-------------')

    @auth_required('token')
    def get(self,u_id,s_id):
        
        rating_det = Rating.query.filter(Rating.show_id==s_id, Rating.u_id==u_id).first()
        return {
            'rating_det': rating_det
        },200
    
    @auth_required('token')
    @roles_required('user')
    
    def delete(self,u_id,s_id,r_id):
        rating_done = Rating.query.get(r_id)

        if u_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')
        
        if not rating_done:
            return {'message':'Cannot find the review give, review doesnt exist!'}
        
        db.session.delete(rating_done)
        db.session.commit()
        print('-----------------Review/Rating deleted-------------------')
        return {
            'message':'Review/Rating deleted successfully'
        },200