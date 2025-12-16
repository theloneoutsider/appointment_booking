from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Ehsan.Artista.1370@localhost/appointment_booking"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/appointment_booking"
app.config["SECRET_KEY"] = "something secure"


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

from model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from route import blueprint
app.register_blueprint(blueprint)