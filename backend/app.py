from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv
from resources import auth_bp

def create_app():
    app = Flask(__name__)

# load environment variables from .env file
    load_dotenv()

    #config
    app.config.from_object(LocalDevelopmentConfig)

    # connection for falsk with sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    #flask security init
    from extentions import security
    from flask_security import SQLAlchemyUserDatastore

    datastore = SQLAlchemyUserDatastore(db, User, Role)  # Replace None with User and Role models
    security.init_app(app, datastore=datastore)  # Replace None with your user datastore

    app.datastore = datastore

    #blueprints
    app.register_blueprint(auth_bp)

    #for creating the database tables
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)