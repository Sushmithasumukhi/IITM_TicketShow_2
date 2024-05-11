#KORAGAJJA
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_security.utils import hash_password
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, roles_required

from application.config import DevelopementConfig , Config
from application.models import User, Role, db
# importing cache
from application.cache import cache



# Celery imports
from application import workers
from application.tasks import *


#  Importing APIs 
from api.authAPI.auth_admin import Auth_AdminAPI
from api.authAPI.u_signup import SignUpAPI
from api.show import ShowAPI
from api.theater import TheaterAPI
from api.user.display_show import DisplayShows, TheaterDetails
from api.user.theater_show import Theater_Show
from api.user.booking_show import Booking_Ticket, CancelBooking
from api.user.booking_details import User_Booking_Details
from api.user.rate_show import ShowRating
from api.user.search import Theater_Search, Show_Search
from api.user.user_details import UserDetails

datastore = SQLAlchemyUserDatastore(db, User, Role)

# ---------------------

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
app.config.from_object(Config)

#  Database initialization
db.init_app(app)

#  Security
security = Security(app,datastore)

#   API Initialization
api = Api(app)

# ------------------------

app.app_context().push()

# CORS ENABLE
CORS(app, supports_credentials=True)


# resources={r"/*":{"origins":"http://localhost:8080"}}
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authentication-token'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response
# FLASK CACHING
cache.init_app(app)


# API END POINTS

api.add_resource(SignUpAPI, '/user/signup', '/user/login' )
api.add_resource(Auth_AdminAPI, '/auth-admin')

api.add_resource(ShowAPI, '/admin/show/all','/admin/show/<int:id>','/admin/show/delete/<int:del_id>',
                 '/admin/show/update/<int:id>/theater/<int:t_id>','/admin/show/upload/<int:t_id>')

api.add_resource(TheaterAPI, '/admin/theater/create','/admin/get/theater','/admin/theater/delete/<int:t_id>',
                 '/admin/theater/update/<int:t_id>','/admin/theater/<int:t_id>')

api.add_resource(DisplayShows,'/user/shows/<int:id>')
api.add_resource(Theater_Show, '/user/theaters/shows')
api.add_resource(Booking_Ticket, '/user/booking/<int:u_id>/theater/<int:t_id>/show/<int:s_id>','/user/booking/<int:u_id>/theater/<int:t_id>/show/<int:s_id>')
api.add_resource(CancelBooking, '/user/<int:u_id>/theater/<int:t_id>/show/<int:s_id>/booking/<int:b_id>')
api.add_resource(User_Booking_Details, '/user/<int:user_id>/booking/details')
api.add_resource(ShowRating, '/user/<int:u_id>/<int:t_id>/<int:s_id>/<int:b_id>','/user/<int:u_id>/show/<int:s_id>/review/<int:r_id>') 
api.add_resource(Show_Search,'/user/shows/search')
api.add_resource(Theater_Search,'/user/theaters/search')
api.add_resource(TheaterDetails,'/user/theater/<int:t_id>')
api.add_resource(UserDetails, '/user/<int:u_id>')



# CELERY -----
celery = workers.celery

celery.conf.update(
    broker = app.config['CELERY_BROKER_URL'],
    backend = app.config['CELERY_RESULT_BACKEND'],
    timezone = 'Asia/Calcutta',
    enable_utc = False
)

celery.Task = workers.ContextTask
app.app_context().push()



# -- Export route

@auth_required('token')
@roles_required('admin')
@app.route("/admin/theater/export/<int:id>",methods=['GET'])
@cache.cached(timeout=15)
def exports(id):
    with current_app.app_context():
        export_csv.delay(id)
            
        return {'message':'CSV export triggered successfully!!'},200




# Two admins created when database created for first time

def create_admin():
    db.create_all()
    if not datastore.find_user(email='admin1@ticketshow.com'):
        admin1 = datastore.create_user(email='admin1@ticketshow.com', password = hash_password('admin1234'), username="Admin_01")
    if not datastore.find_user(email='admin2@ticketshow.com'):
        admin2 = datastore.create_user(email='admin2@ticketshow.com', password = hash_password('admin1234'), username="Admin_02")
    # if not datastore.find_user(email='admin3@ticketshow.com'):
    #     admin3 = datastore.create_user(email='admin3@ticketshow.com', password = hash_password('admin1234'), username="Admin_03")

        admin_role = datastore.find_or_create_role(name='admin', description='Administration')
        datastore.add_role_to_user(admin1,admin_role)
        datastore.add_role_to_user(admin2,admin_role)
        # datastore.add_role_to_user(admin3,admin_role)


        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)