from flask import Flask, jsonify, request
from models import db, Incident
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest
from create_database import create_database_if_not_exists

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Add a rotating file handler
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

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
    logger.error(f"Error creating database tables: {str(e)}")
    raise

# Error handlers
@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    logger.error(f"Database error: {str(e)}")
    return jsonify({'error': 'Database error occurred'}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    logger.warning(f"Bad request: {str(e)}")
    return jsonify({'error': 'Invalid request data'}), 400

@app.errorhandler(404)
def handle_not_found(e):
    logger.warning(f"Resource not found: {str(e)}")
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def handle_server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error occurred'}), 500

@app.route('/incidents', methods=['GET'])
def get_incidents():
    """ Get all incidents from the database """
    try:
        incidents = Incident.query.all()
        return jsonify([incident.to_dict() for incident in incidents])
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch incidents: {str(e)}")
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
            logger.warning("No JSON data provided in POST request")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if not all(k in data for k in ['title', 'description', 'severity']):
            logger.warning("Missing required fields in POST request")
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate severity
        data['severity'] = data['severity'].capitalize()

        if not is_valid_severity(data['severity']):
            logger.warning(f"Invalid severity level provided: {data['severity']}")
            return jsonify({'error': 'Invalid severity level. Must be Low, Medium, or High'}), 400
        
        # Create new incident
        incident = Incident(
            title=data['title'],
            description=data['description'],
            severity=data['severity']
        )
        
        db.session.add(incident)
        db.session.commit()
        logger.info(f"Successfully created new incident with ID: {incident.id}")
        
        return jsonify(incident.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Failed to create incident: {str(e)}")
        return jsonify({'error': 'Failed to create incident'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Get a specific incident by its ID"""
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            logger.warning(f"Incident not found with ID: {incident_id}")
            return jsonify({'error': 'Incident not found'}), 404
        return jsonify(incident.to_dict())
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch incident {incident_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch incident'}), 500

@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """ Delete a specific incident by its ID """
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            logger.warning(f"Attempted to delete non-existent incident with ID: {incident_id}")
            return jsonify({'error': 'Incident not found'}), 404
        
        db.session.delete(incident)
        db.session.commit()
        logger.info(f"Successfully deleted incident with ID: {incident_id}")
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Failed to delete incident {incident_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete incident'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True) 