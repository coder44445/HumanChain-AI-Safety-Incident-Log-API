from flask import Flask, jsonify, request
from models import db, Incident
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest
from create_database import create_database_if_not_exists

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create database if it doesn't exist
create_database_if_not_exists()

# MySQL configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
try:
    with app.app_context():
        db.create_all()
except SQLAlchemyError as e:
    print(f"Error creating database tables: {str(e)}")
    raise

# Error handlers
@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    print(f"Database error: {str(e)}")
    return jsonify({'error': 'Database error occurred'}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    print(f"Bad request: {str(e)}")
    return jsonify({'error': 'Invalid request data'}), 400

@app.errorhandler(404)
def handle_not_found(e):
    print(f"Resource not found: {str(e)}")
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def handle_server_error(e):
    print(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error occurred'}), 500

@app.route('/incidents', methods=['GET'])
def get_incidents():
    """ Get all incidents from the database """
    try:
        incidents = Incident.query.all()
        return jsonify([incident.to_dict() for incident in incidents])
    except SQLAlchemyError as e:
        print(f"Failed to fetch incidents: {str(e)}")
        return jsonify({'error': 'Failed to fetch incidents'}), 500

# Validation function for severity
def is_valid_severity(severity):

    """ Returns True is the serverity is valid """

    return severity in ['Low', 'Medium', 'High']

@app.route('/incidents', methods=['POST'])
def log_new_incident():
    """ Create a new incident in the database """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if not all(k in data for k in ['title', 'description', 'severity']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate severity

        data['severity'] = data['severity'].capitalize()

        if not is_valid_severity(data['severity']):
            return jsonify({'error': 'Invalid severity level. Must be Low, Medium, or High'}), 400
        
        # Create new incident
        incident = Incident(
            title=data['title'],
            description=data['description'],
            severity=data['severity']
        )
        
        db.session.add(incident)
        db.session.commit()
        
        return jsonify(incident.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Failed to create incident: {str(e)}")
        return jsonify({'error': 'Failed to create incident'}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Get a specific incident by its ID"""
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            return jsonify({'error': 'Incident not found'}), 404
        return jsonify(incident.to_dict())
    except SQLAlchemyError as e:
        print(f"Failed to fetch incident {incident_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch incident'}), 500

@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):

    """ Delete a specific incident by its ID """
    
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            return jsonify({'error': 'Incident not found'}), 404
        
        db.session.delete(incident)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Failed to delete incident {incident_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete incident'}), 500

if __name__ == '__main__':
    app.run(debug=True) 