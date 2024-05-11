from flask import make_response
from werkzeug.exceptions import HTTPException
import json

class NotFoundError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"code":error_code, "message":error_message}
        self.response = make_response(json.dumps(message), status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"code":error_code, "message":error_message}
        self.response = make_response(json.dumps(message), status_code)

class UnAuthorizedError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"code":error_code, "message":error_message}
        self.response = make_response(json.dumps(message), status_code)
