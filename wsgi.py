import app

flask_app = app.PPIInit().__get_flask__()

if __name__ == '__main__':

    import logging
    logging.basicConfig(filename='logs/flask.log',level=logging.DEBUG)

    flask_app.run(debug=flask_app.config.get("DEBUG"),
                  port=flask_app.config.get("PORT"))