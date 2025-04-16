#!./env/bin/python

import logging
import os
from logging.handlers import RotatingFileHandler

import click
from app import create_app, db
from flask.cli import FlaskGroup

application = create_app()

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage
    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

cli = FlaskGroup(application)


@cli.command("create")
def create():
    """Creates all tables"""
    db.create_all()


if __name__ == "__main__":
    applogger = application.logger

    file_handler = RotatingFileHandler(
        "./error.log", maxBytes=1024 * 1024 * 100, backupCount=20
    )
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - \
                                  %(levelname)s - % (message)s"
    )
    file_handler.setFormatter(formatter)
    application.logger.addHandler(file_handler)
    application.logger.setLevel(logging.DEBUG)

    cli()
