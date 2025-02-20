from flask import request, Blueprint
from flask_security import login_user
from models import user

login_api = Blueprint("login_api", __name__)


# 設定未授權時轉跳畫面
# security._state.unauthorized_handler(unauthorized_callback)


@login_api.route("/login_user", methods=["POST"])
def validate():
    email = request.values.get("email")
    password = request.values.get("password")
    cur_user = user.validate_user(email, password)
    remember = True if request.values.get("rememberMe", "n") == "y" else False


    if cur_user is None:
        return "帳密錯誤"

    login_user(cur_user, remember=remember)
    return "success"


@login_api.route("/create_manager", methods=["GET"])
def create_manager():
    email = request.values.get("email")
    password = request.values.get("password")
    user.create_user(email, password, "manager")
    return "success"