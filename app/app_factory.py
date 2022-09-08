from flask import Flask
from app.database import db
import configparser


def create_app(config_path, settings_override=None):
    """
    Create a new app.
    :param config_path:
    :type config_path:
    :param settings_override:
    :type settings_override:
    :return:
    :rtype:
    """
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read(config_path)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE"]["CONNECTION_STRING"]
    app.config["IPSTACK_KEY"] = config["IPSTACK"]["IPSTACK_KEY"]
    app.config["ENVIRONMENT"] = config["ENV"]["STAGE"]

    app.debug = config["ENV"]["STAGE"] == "dev"
    app.secret_key = config["ENV"]["SECRET_KEY"]

    if settings_override:
        app.config.update(settings_override)
    db.init_app(app)

    from app.core import core

    app.register_blueprint(core)

    return app
