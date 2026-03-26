#THIS FILE IS TO MAKE FLASK APPLICATION
from flask import Flask, app
from config import Config
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy() #database object create karo


def create_app():  #flask application create karo
    app = Flask(__name__, instance_relative_config=True)  #flask website start
    app.config.from_object(Config)  #config.py ki settings load karo
    db.init_app(app)  #databse ko Flsk se connect karo


from app.routes.routes import main_bp
app.register_blueprint(main_bp)  #routes activate karo

with app.app_context():     #Flask ko pata hai abhi kon sa app active hai
     #jabh flask ke bahar db access kareinge toh error aati hai working outside of application context kyuki flask ko pata nhihita konsa aap use ho traha hai
    from app.models import models
    db.create_all()  # database tabels automatically create karo