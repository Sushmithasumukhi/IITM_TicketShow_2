from flask_restful import Resource
from flask import request, jsonify
from flask_security import SQLAlchemyUserDatastore, current_user, auth_required, roles_required
from application.models import db, User, Role, Show, Theater, Rating
from application.validation import NotFoundError, UnAuthorizedError, BusinessValidationError
from application.utlis import save_image
from PIL import Image

import os

datastore = SQLAlchemyUserDatastore(db, User, Role)

class ShowAPI(Resource):
# ------------------GET API--------------------------
    @auth_required('token')
    @roles_required('admin')

    def get(self, id=None):
        if id:
            m = Show.query.filter(Show.id == id, Show.admin_id == current_user.id).first() 
            print(m)
            
            if m:
                ratings_of_show = Rating.query.filter(Rating.show_id==id).all()

                if not ratings_of_show:
                    round_avg_rating = 0.00
                if len(ratings_of_show)>0:
                    totrating =  sum(r.rating for r in ratings_of_show)
                    avg_rating = totrating/len(ratings_of_show)
                    round_avg_rating = round(avg_rating,2)
               
                
                if m.m_image:
                    file = os.path.split(m.m_image)
                    path = os.path.join("static","shows",file[1])
                    image_url = f"{request.host_url}{path}"
                return {
                    'id':m.id,
                    'admin_id':m.admin_id,
                    'show_name':m.show_name,
                    'description':m.description,
                    'price':m.price,
                    'tags':m.tags,
                    'm_image':image_url,
                    'show_time':m.show_time,
                    'show_added_on':m.show_added_on.isoformat(),
                    'theater_id':m.theater_id,
                    'avg_rating':round_avg_rating
                    }
            raise NotFoundError(404,'NF1001','Show Not Found')
        
        #GET ALL SHOWS
        show_admin = Show.query.filter(Show.admin_id==current_user.id)
        shows = show_admin.order_by(Show.show_added_on.desc()).all()
        return [{
                'id':m.id,
                'show_name':m.show_name,
                'm_image':f"{request.host_url}static/shows/{os.path.split(m.m_image)[-1]}" if m.m_image else None,
                'admin_id':current_user.id
        } for m in shows],200
    

# ------------------DELETE API--------------------------
    @roles_required('admin')
    @auth_required('token')

    def delete(self, del_id):
        show = Show.query.filter(Show.id==del_id, Show.admin_id == current_user.id).first()

        if show.admin_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','You are not authorized to do this ACTION')

        if not show:
            raise NotFoundError(404,'NF1001','Show doesnt exist')

        db.session.delete(show)
        db.session.commit()
        print('--------------------------Show Deleted Successfully-----------------------')
        return {
                'status_code' : '200', 
                'status' : 'success',
                'message' : 'Deleted Show Successfully!!'
            },200
    
    #isoformmat used to make datetime json serializable
    # 2023-06-22T13:45:30.123456 ISO Format 


# ------------------POST API--------------------------
    @roles_required('admin')
    @auth_required('token')

    def post(self,t_id):
        show_name = request.form.get('show_name')
        description = request.form.get('description')
        tags = request.form.get('tags')
        price = request.form.get('price')
        show_time = request.form.get('show_time')
        theater_id = request.form.get('theater_id') 

        m_image = request.files.get('m_image')

        if not show_name:
            raise BusinessValidationError(406,"BE1004","Show name cant be empty") 
        if m_image and not allowed_file(m_image.filename):
            return BusinessValidationError(422,'BE1006','Invalid image format, use only jpeg, jpg, png, gif, jfif')

        if not m_image:
            m_image = 'movie_default.jpg'
        image_path = None
        if m_image:
            image_path =  save_image(m_image)

        # print(m_image)

        theater_exist = Theater.query.get(t_id)

        if not theater_exist:
            raise NotFoundError(404,'NF1001','Theater doesnt exist ')
        
        time_slot_of_show = Show.query.filter(Show.theater_id==t_id, Show.show_time == show_time ).first()

        if (time_slot_of_show and time_slot_of_show.id != id):
            raise BusinessValidationError(405,'BE1005', f'Time slot is already assigned to \'{time_slot_of_show.show_name}\' in theater {time_slot_of_show.theater.theater_name} at time - {show_time}, Please choose another time slot!!')



        show = Show(show_name=show_name, description=description, tags=tags,price=price, show_time=show_time, m_image=image_path, theater_id=theater_id,admin_id=current_user.id)
        db.session.add(show)
        print('-----------------------Show Uploaded-----------------------------')
        db.session.commit()

        return {
                'status_code' : '200', 
                'status' : 'success',
                'message' : 'show uploaded !!',
            },200


# ------------------PUT API--------------------------
    @roles_required('admin')
    @auth_required('token')

    def put(self,id,t_id):
        show_exist = Show.query.filter(Show.id == id, Show.admin_id == current_user.id).first()
        
        if not show_exist:
            raise NotFoundError(404,'NF1001','Show doesnt exist')
        c_u = show_exist.admin_id
        if c_u != current_user.id:
            raise UnAuthorizedError(401, 'NA1001', 'Not Authorized to do the ACTION')
        show_name = request.form.get('show_name')
        description = request.form.get('description')

        show_time = request.form.get('show_time')

        theater_exist = Theater.query.get(t_id)

        if not theater_exist:
            raise NotFoundError(404,'NF1001','Theater doesnt exist ')
        
        time_slot_of_show = Show.query.filter(Show.theater_id==t_id, Show.show_time == show_time ).first()

        if (time_slot_of_show and time_slot_of_show.id != id):
            raise BusinessValidationError(405,'BE1005', f'Time slot is already assigned to \'{time_slot_of_show.show_name}\' in theater {time_slot_of_show.theater.theater_name} at time - {show_time}, Please choose another time slot!!')
        
        price = request.form.get('price')
        m_image = request.files.get('m_image')

        
        #Updating the show details
        show_exist.show_name = show_name 
        show_exist.description = description 
        show_exist.show_time = show_time
        show_exist.price = price 

        if m_image and not allowed_file(m_image.filename):
            return BusinessValidationError(422,'BE1006','Invalid image format, use only jpeg, jpg, png, gif, jfif')
        if m_image:
            # save updated image
            new_path = save_image(m_image)
            show_exist.m_image = new_path

        #commit the changes
        db.session.commit()
        print('--------------------------UPDATED SHOW-------------------------------')

        return {
                'status_code' : '200', 
                'status' : 'success',
                'message' : 'show updated !!',
            },200

ALLOWED_IMAGE_FILE = ['jpg','png','jpeg','jfif','gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_FILE

# def remove_post(image_path):
#     if os.path.exists(image_path):
#         os.remove(image_path)
