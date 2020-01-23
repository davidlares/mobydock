import logging

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from redis import StrictRedis
from sqlalchemy.sql.expression import func

# setting a custom logger because we are using Docker
stream_handler = logging.StreamHandler()
# put the logger into the stdout - Docker's default way is running all the in foreground (read by a third party)
stream_handler.setLevel(logging.INFO)

db = SQLAlchemy()
redis_store = FlaskRedis.from_custom_provider(StrictRedis) # only API calls that matches directly to the redis API

page = Blueprint('page', __name__)

# app factory pattern
def create_app():
    """
    Create a Flask application using the app factory pattern.
    :return: Flask app
    """
    # Flask instance
    app = Flask(__name__, instance_relative_config=True) # goes to the Instance Relative Configuration

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True) # check for settings on the config directory

    db.init_app(app)
    redis_store.init_app(app)

    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    return app

@page.route('/')
def index():
    """
    Render the home page where visitors can feed Moby Dock.
    :return: Flask response
    """
    # check if "feed" is an argument on the request
    if request.args.get('feed'):
        # grabbing a random message
        random_message = db.session.query(Feedback).order_by(func.random()).limit(1).scalar().message
        feed_count = redis_store.incr('feed_count')
    else:
        # feeding the counters
        random_message = ''
        feed_count = redis_store.get('feed_count')
        if feed_count is None:
            feed_count = 0

    return render_template('layout.html', message=random_message, feed_count=feed_count)

# endpoint for feeding the Feedbacks
@page.route('/seed')
def seed():
    """
    Reset the database and seed it with a few messages.
    :return: Flask redirect
    """
    db.drop_all()
    db.create_all()

    messages = [
        "Thanks good sir. I'm feeling quite healthy!",
        'Thanks for the meal buddy.',
        "Please stop feeding me. I'm getting huge!"
    ]

    # looping the messages
    for message in messages:
        feedback = Feedback(message=message)
        db.session.add(feedback)
        db.session.commit()

    # redirecting the page
    return redirect(url_for('page.index'))

# feedback DB Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text())
