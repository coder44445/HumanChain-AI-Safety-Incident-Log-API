from app import app
from models import db, Incident
from create_database import create_database_if_not_exists

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

def populate_database():
    with app.app_context():
        # Clear existing data
        Incident.query.delete()
        
        # Add sample incidents
        for incident_data in sample_incidents:
            incident = Incident(**incident_data)
            db.session.add(incident)
        
        db.session.commit()
        print("Database populated with sample incidents.")

if __name__ == '__main__':
    create_database_if_not_exists()
    populate_database() 