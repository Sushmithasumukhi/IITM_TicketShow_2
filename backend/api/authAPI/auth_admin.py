from flask_restful import Resource
from flask import jsonify
from flask_security import auth_required, roles_required, current_user, SQLAlchemyUserDatastore
from application.models import db, User, Role
datastore = SQLAlchemyUserDatastore(db, User, Role)

class Auth_AdminAPI(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        return jsonify({
            'current_user': current_user.id
        })
    


# dummy API for admin auth