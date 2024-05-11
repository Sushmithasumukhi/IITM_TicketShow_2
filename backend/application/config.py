class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = "thisissecter"
    SECURITY_PASSWORD_SALT = "thisissaltt"
    SECURITY_PASSWORD_HASH="bcrypt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_ROLE_ADMIN = 'admin'
    
    ALLOWED_IMAGE_FILE = ['jpg','png','jpeg','jfif','gif']
    

    CACHE_TYPE='RedisCache'
    CACHE_REDIS_HOST='localhost'

    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

class DevelopementConfig(Config):
    DEBUG = True