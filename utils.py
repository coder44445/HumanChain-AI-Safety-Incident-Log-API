import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        # Create engine without database
        engine = create_engine(f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/")
        
        # Create database if it doesn't exist
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
            conn.commit()
            logger.info(f"Database {os.getenv('DB_NAME')} created or already exists")

    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise

def populate_database():
    """Populate the database with sample incidents"""
    from app import create_app
    from models import db, Incident
    
    sample_incidents = [
        {
            'title': 'AI Model Bias in Hiring System',
            'description': 'An AI-powered hiring system was found to be biased against female candidates, showing a 20% lower selection rate compared to male candidates with similar qualifications.',
            'severity': 'High'
        },
        {
            'title': 'Chatbot Misinformation Incident',
            'description': 'A customer service chatbot provided incorrect medical advice to users, potentially putting their health at risk.',
            'severity': 'Medium'
        },
        {
            'title': 'Data Privacy Breach in AI Training',
            'description': 'Sensitive user data was inadvertently included in the training dataset without proper anonymization.',
            'severity': 'High'
        }
    ]
    
    app = create_app()
    with app.app_context():
        try:
            # Add sample incidents
            for incident_data in sample_incidents:
                incident = Incident(**incident_data)
                db.session.add(incident)
            
            db.session.commit()
            logger.info("Database populated with sample incidents.")
        except Exception as e:
            logger.error(f"Error populating database: {str(e)}")
            raise

if __name__ == '__main__':
    load_dotenv()
    create_database_if_not_exists()
    populate_database() 