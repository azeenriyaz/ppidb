from .views import PPIBP
from flask_app import PPIApp

class PPIInit():
    flask_app = PPIApp().__get_app__()
    flask_app.static_url_path = flask_app.config.get("STATIC_FOLDER")
    flask_app.static_folder = flask_app.config.get("STATIC_FOLDER")
    flask_app.template_folder = flask_app.config.get("TEMPLATES_FOLDER")
    flask_app.secret_key = flask_app.config.get("SECRET_KEY")
    flask_app.instance_path = flask_app.config.get("INSTANCE_PATH")
    flask_app.register_blueprint(PPIBP)
    def __get_flask__(self):
        return self.flask_app
        