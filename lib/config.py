class Config(object):
    UPLOAD_FOLDER = "static/images"
    # Flask Security
    DEBUG = True
    SECRET_KEY = "super-secret"
    SECURITY_PASSWORD_SALT = "bcrypt"
    SECURITY_LOGIN_USER_TEMPLATE = "login.html"

    # MongoDB Config
    MONGODB_DB = "test"
    MONGODB_HOST = (
        "mongodb://localhost:27017"
    )
    MONGODB_USERNAME = "Liao"
    MONGODB_PASSWORD = "871029"
    MONGODB_AUTH_SOURCE = "admin"

    JSON_AS_ASCII = False
    TEMPLATES_AUTO_RELOAD = True
    UPLOAD_FOLDER = UPLOAD_FOLDER

