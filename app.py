from flask import Flask
from config import Config
from models import db
from routes import api
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)
    
    file_handler = RotatingFileHandler(
        os.path.join(Config.LOG_DIR, Config.LOG_FILE),
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    
    try:
        # Initialize database
        db.init_app(app)
        
        # Register blueprints
        app.register_blueprint(api)
        
        # Create database tables
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
        
        return app
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        app = create_app()
        app.run(debug=Config.DEBUG)
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        raise 