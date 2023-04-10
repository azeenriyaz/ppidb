from flask import Flask
import config
import sqlalchemy as sal

class PPIApp():
    flask_app = Flask(__name__)
    flask_app.config.from_object(config.DevConfig)
    engine = sal.create_engine(config.DevConfig.SQLALCHEMY_DATABASE_URI)
    def __init__(self):
        pass
    def __get_app__(self):
        return self.flask_app
    def __get_sql_engine__(self):
        return self.engine