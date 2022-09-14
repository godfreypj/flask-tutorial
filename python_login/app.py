"""
Module info
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

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
        SECRET_KEY = 'dev'
    )
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'BndaaKHRM@U6'
    app.config['MYSQL_DB'] = 'python_login'

    # If we haven't already set the configuration file, do so
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    # Otherwise, load up the configuration we passed in
    else:
        app.config.from_mapping(test_config)

    my_sql = MySQL(app)

    # Create an initial route - '/index' page will return this simple string
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg = ''

        # Validate user input
        if 'username' in request.form and 'password' in request.form:
            # Grab the username/password
            user_name = request.form['username']
            password = request.form['password']

            # Go check for a match in our database
            cursor = my_sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('\
                SELECT * FROM accounts WHERE username=%s and password=%s', (user_name, password)\
            )
            # Validate, there can only be one
            if cursor:
                # Assign the account
                account = cursor.fetchone()

                if account:
                    # Build session data for later access
                    session['logged_in'] = True
                    session['username'] = account['username']
                    session['email'] = account['email']

                    return "Logged in, awwww yeah!"

                msg += "Incorrect username/password combo"
            else:
                msg = "Could not connect to database"

        return render_template('index.html', msg=msg)

    return app
