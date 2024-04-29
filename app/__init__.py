from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create instances of Flask extensions without initializing them
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'  # Change to 'routes.login'
    login_manager.login_message_category = 'info'

    # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import inside the function to avoid circular import
        return User.query.get(int(user_id))


    # Import Blueprints and register them with the app
    from app.routes import bp as routes_bp
    from app.admin import admin_bp

    app.register_blueprint(routes_bp)
    app.register_blueprint(admin_bp)

    # Import models to ensure they are registered with SQLAlchemy
    from app import models

    return app
