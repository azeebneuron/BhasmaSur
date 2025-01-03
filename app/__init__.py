from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.waste import waste_bp
    from .routes.business import business_bp
    from .routes.social import social_bp
    from .routes.initiative import initiative_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(waste_bp, url_prefix='/api/waste')
    app.register_blueprint(business_bp, url_prefix='/api/businesses')
    app.register_blueprint(social_bp, url_prefix='/api/social')
    app.register_blueprint(initiative_bp, url_prefix='/api/initiatives')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        from .models.user import User
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@ecoconnect.com',
                password='admin123',  # Change this in production!
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    return app