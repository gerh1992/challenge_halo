from flask import Flask
import logging
import os

from challenge_halo.routes import configure_routes

LOGGING_LEVEL = os.getenv("FLASK_LOGGING_LEVEL", "INFO")

logging.basicConfig(
    level=LOGGING_LEVEL,
    format='[%(filename)s:%(lineno)s] %(levelname)s %(asctime)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)


def create_app():
    app = Flask(__name__)
    return app


app = create_app()

configure_routes(app)
