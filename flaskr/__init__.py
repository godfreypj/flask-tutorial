"""
Module info
"""
import os

from flask import Flask

def create_app(test_config=None):
    """
    Create app - kicks off app, sets configuration
    """
    # Create the app and configure - passing in this current module for the name & where the
    #  'instance' folder is located
    app = Flask(__name__, instance_relative_config=True)

    # Configure: working in dev so secret key is not so secret, and put the db file in the
    # 'instance' folder we described above
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # If we haven't already set the configuration file, do so
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Otherwise, load up the configuration we passed in
        app.config.from_mapping(test_config)

    # If the 'instance' directory is not created, do so
    try:
        os.makedirs(app.instance_path)
    # Otherwise, throw an OS error
    except OSError:
        pass
