from flask_security import UserMixin, RoleMixin
from flask_security import (
    MongoEngineUserDatastore,
    hash_password,
    verify_password,
)
from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, ReferenceField
from uuid import uuid4
from . import _db


USER_DATASTORE = None

"""
    setup
"""



# 不同種權限身份
class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

# 使用者資訊
class User(Document, UserMixin):
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    fs_uniquifier = StringField(default=lambda: str(uuid4()), unique=True)  # 新增的字段
def setup():
    # Setup Flask-Security
    global USER_DATASTORE
    USER_DATASTORE = MongoEngineUserDatastore(_db.DB, User, Role)


"""
    others
"""

def check_user_datastore_connection():
    print(f"User model database: {USER_DATASTORE.user_model._get_db().name}")
    print(f"User model collection: {USER_DATASTORE.user_model._get_collection().name}")
    print(f"Role model database: {USER_DATASTORE.role_model._get_db().name}")
    print(f"Role model collection: {USER_DATASTORE.role_model._get_collection().name}")

def create_user(email: str, password: str, role_name: str = "student"):
    check_user_datastore_connection()
    try:
        # 確保角色存在
        role = USER_DATASTORE.find_or_create_role(role_name)
        # 確保用戶不存在後才創建
        if USER_DATASTORE.find_user(email = email) is None:
            USER_DATASTORE.create_user(
                email=email,
                password=hash_password(password),
                roles=[role],
            )
            print(f"User '{email}' created successfully with role '{role_name}'.")
        else:
            print(f"User '{email}' already exists.")
    except Exception as e:
        print(f"Failed to create user '{email}': {e}")

def create_role(name: str, description: str):
    try:
        if USER_DATASTORE.find_role(name) is None:
            USER_DATASTORE.create_role(name=name, description=description)
            print(f"Role '{name}' created successfully.")
        else:
            print(f"Role '{name}' already exists.")
    except Exception as e:
        print(f"Failed to create role '{name}': {e}")



def validate_user(email: str, password: str):
    try:
        cur_user = USER_DATASTORE.find_user(email=email)
        if cur_user and verify_password(password, cur_user.password):
            return cur_user
        print("Invalid email or password.")
    except Exception as e:
        print(f"Error validating user '{email}': {e}")
    return None