import logging
import os
import app

root = logging.getLogger()
root.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/flask.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
root.addHandler(file_handler)

flask_app = app.PPIInit().__get_flask__()

@flask_app.errorhandler(Exception)
def handle_error(e):
    logging.error(str(e))
    return "An error occurred.", 500

workers = flask_app.config.get('WORKERS')
timeout = flask_app.config.get('GUNICORN_TIMEOUT')
bind = flask_app.config.get('GUNICORN_BIND')

if __name__ == "__main__":
    from gunicorn.app.base import BaseApplication

    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': bind,
        'workers': workers,
        'timeout': timeout,
        'loglevel': 'info',
        'name': 'ppidb'
    }

    GunicornApp(flask_app, options).run()