from mongoengine import connect

DB = None


def setup(app):
    global DB
    DB = connect(
        db=app.config.get("MONGODB_DB"),  # 從 app.config 中讀取資料庫名稱
        host=app.config.get("MONGODB_HOST"),
        username=app.config.get("MONGODB_USERNAME"),
        password=app.config.get("MONGODB_PASSWORD"),
        authentication_source=app.config.get("MONGODB_AUTH_SOURCE", "admin"),
    )
