from flask_security import UserMixin, RoleMixin
from flask_security import (
    MongoEngineUserDatastore,
    hash_password,
    verify_password,
)
from . import _db


USER_DATASTORE = None

"""
    setup
"""


def setup():
    # 不同種權限身份
    class Role(_db.DB.Document, RoleMixin):
        name = _db.DB.StringField(max_length=80, unique=True)
        description = _db.DB.StringField(max_length=255)

    # 使用者資訊
    class User(_db.DB.Document, UserMixin):
        email = _db.DB.StringField(max_length=255)
        password = _db.DB.StringField(max_length=255)
        active = _db.DB.BooleanField(default=True)
        confirmed_at = _db.DB.DateTimeField()
        roles = _db.DB.ListField(_db.DB.ReferenceField(Role), default=[])

    # Setup Flask-Security
    global USER_DATASTORE
    USER_DATASTORE = MongoEngineUserDatastore(_db.DB, User, Role)


"""
    others
"""


def create_user():
    student_role = USER_DATASTORE.find_or_create_role("student")
    if USER_DATASTORE.get_user("Liao") is None:
        USER_DATASTORE.create_user(
            email="Liao",
            password=hash_password("871029"),
            roles=[student_role],
        )


def validate_user(email: str, password: str):
    cur_user = USER_DATASTORE.find_user(email=email)

    if verify_password(password, cur_user.password):
        return cur_user
    return None
