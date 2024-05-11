from flask_restful import Resource,reqparse
from application.models import db, User, Role, Theater
from flask_security import SQLAlchemyUserDatastore, auth_required, roles_required, current_user
from application.validation import NotFoundError,BusinessValidationError, UnAuthorizedError

datastore = SQLAlchemyUserDatastore(db, User, Role)



# Parsers to handle data in request body

create_theater = reqparse.RequestParser()
create_theater.add_argument("theater_name", required=True)
create_theater.add_argument("t_place", required=True)
create_theater.add_argument("location", required=True)
create_theater.add_argument("t_rating")
create_theater.add_argument("seat_capacity", required=True, type=int)

update_theater = reqparse.RequestParser()
update_theater.add_argument("theater_name", required=True)
update_theater.add_argument("t_place", required=True)
update_theater.add_argument("location", required=True)
update_theater.add_argument("t_rating")
update_theater.add_argument("seat_capacity", required=True, type=int)




class TheaterAPI(Resource):
# ------------------DELETE API--------------------------
    @roles_required('admin')
    @auth_required('token')

    def delete(self,t_id):
        theater_exist = Theater.query.get(t_id)
        if theater_exist.admin_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not Authorized')
        
        if not theater_exist:
            raise NotFoundError(404,'NF1002','Theater doesnt exist')
        db.session.delete(theater_exist)
        db.session.commit()
        print('--------------Theater deleted-----------------')
        return {'status_code':'200',
                'message':'Successfully deleted.'}
            

#-------------------POST API-------------------------
    @roles_required('admin')
    @auth_required('token')
    
    def post(self):
        args = create_theater.parse_args()
        theater_name = args.get("theater_name")
        t_place = args.get("t_place")
        location = args.get("location")
        seat_cap = args.get("seat_capacity")

        theater_exist = Theater.query.filter(Theater.theater_name==theater_name, Theater.t_place == t_place).first()
        if not theater_exist:
            add_theater = Theater(theater_name=theater_name,t_place=t_place,location=location,seat_capacity=seat_cap, admin_id=current_user.id)
            db.session.add(add_theater)
            print('----------------------Theater added ----------------------')
            db.session.commit()
            return {
                'status_code' : '200', 
                'status' : 'success',
                'message' : 'New Theater Added',
            },200   
        raise BusinessValidationError(405,'BE1002','Theater already exist')

# ---------------------- PUT API -------------------
    @roles_required('admin')
    @auth_required('token')

    def put(self,t_id):        
        args = update_theater.parse_args()
        theater_name = args.get("theater_name")
        t_place = args.get("t_place")
        location = args.get("location")
        seat_capacity = args.get("seat_capacity")

        theater_exist = Theater.query.filter(Theater.id == t_id).first()

        if theater_exist:
            if theater_exist.admin_id != current_user.id:
                raise UnAuthorizedError(401,'NA1001','Not Authorized')
            theater_exist.theater_name = theater_name
            theater_exist.t_place = t_place
            theater_exist.location = location
            theater_exist.seat_capacity = seat_capacity

            db.session.commit()
            print('----------------------Theater Updated ----------------------')

            return {
                'status_code' : '200', 
                'status' : 'success',
                'message' : 'Updated Theater Successfully',
            },200   
        raise NotFoundError(404,'NF1002','Theater doesnt exist')



# ---------------------- GET API --------------------------
    @roles_required('admin')
    @auth_required('token')

    def get(self, t_id=None):
        # Get particular theater 
        if t_id:
            theater = Theater.query.get(t_id)
            sh = []
            if theater:
                for s in theater.shows:
                    s_data = {
                        'id' : s.id,
                        'show_name' : s.show_name,
                        'show_time' : s.show_time
                        }
                    sh.append(s_data)
                return {
                    'id':theater.id,
                    'theater_name':theater.theater_name,
                    't_place':theater.t_place,
                    'location':theater.location,
                    'seat_capacity':theater.seat_capacity,
                    'shows': sh
                },200
                
            raise NotFoundError(404,'NF1001','Theater Not Found')
        else:
            # get all theater
            
            theaters = Theater.query.filter(Theater.admin_id==current_user.id).all()
            
            
            return  [{
                    'id':t.id,
                    'theater_name':t.theater_name,
                    't_place':t.t_place,
                    'location':t.location,
                    'seat_capacity':t.seat_capacity,
                    # 'show_name': show_name
                }  for t in theaters],200