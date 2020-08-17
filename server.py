import os
from resources.users import user
from resources.all_maps import all_map
import models
from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

DEBUG = True
PORT = 8000


# importing resource

login_manager = LoginManager()  # sets up the ability to set up the session

app = Flask(__name__)

# Need to specify cookie settings when deployed due to chrome issue. This causes problems locally though so only setting conditionally
if 'ON_HEROKU' in os.environ:
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='None',
    )

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD"  # Need this to encode the session
login_manager.init_app(app)  # set up the sessions on the app


# decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
@login_manager.user_loader
def load_user(userid):
    try:
        print("\nloading user: ", userid)
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        print("\nload failed for user: ", userid)
        return None

# we don't want to hog up the SQL connection pool
# so we should connect to the DB before every request
# and close the db connection after every request

# use this decorator to cause a function to run before reqs


@app.before_request
def before_request():
    """Connect to the database before each request"""
    # store the database as a global var in g
    print("app.before_request executed")
    g.db = models.DATABASE
    g.db.connect()

# use this decorator to cause a function to run after reqs


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    print("app.after_request executed")
    g.db.close()
    # send response back to client
    return response


CORS(all_map, origins=['http://localhost:3000',
                       'https://tripstatistics.herokuapp.com'], supports_credentials=True)
app.register_blueprint(all_map, url_prefix='/api/v1/all_maps')

CORS(user, origins=['http://localhost:3000',
                    'https://tripstatistics.herokuapp.com'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

# determine database to use depending on if environment is local or heroku
if 'ON_HEROKU' in os.environ:
    print('\nheroku tables initialized')
    models.initialize()

if __name__ == '__main__':
    print('\nlocal tables initialized')
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
