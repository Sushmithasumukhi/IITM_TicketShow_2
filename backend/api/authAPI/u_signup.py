from flask_restful import Resource, reqparse
from flask_security import SQLAlchemyUserDatastore, auth_required, current_user, roles_required
from flask_security.utils import hash_password
from application.models import User, Role, db
from application.validation import BusinessValidationError

datastore = SQLAlchemyUserDatastore(db, User, Role)


create_user = reqparse.RequestParser()
create_user.add_argument("username", type=str, required=True)
create_user.add_argument("password", type=str, required=True)
create_user.add_argument("email", type=str, required=True)

class SignUpAPI(Resource):
    def post(self):
        args = create_user.parse_args()
        username=args.get("username")
        password=args.get("password")
        email=args.get("email")

        if email is None:
            raise BusinessValidationError(405,"BE1001","email cant be empty")
        if email:
            data=User.query.filter(User.email==email).first()
            if not data:
                usern = User.query.filter(User.username==username).first()
                if not usern:
                    user = datastore.create_user(username=username, email=email, password=hash_password(password))
                    user_role = datastore.find_or_create_role(name='user', description='User')
                    datastore.add_role_to_user(user,user_role)
                    db.session.commit()
                    print('-----------------User signup ----------------------')
                    return ("User created successfully",200)
                return BusinessValidationError(409,'BE1001','Username already exists')
            else:
                raise BusinessValidationError(409,"BE1002","email already exists")
            
    @auth_required('token')
    @roles_required('user')
    def get(self):
        user_details = User.query.get(current_user.id)
        return {'current_user':user_details.id},200
