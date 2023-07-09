from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # Flask-Login needs to know what view fanction handles logins to allow 'restricted' access to certain webpages (i.e. only logged-in users can view certain webpages)

from app import routes, models