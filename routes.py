from flask import Blueprint, jsonify, request, render_template
from models import db, Incident
from sqlalchemy import create_engine, exc
import logging

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)



def validate_incident_data(data: dict) -> tuple:
    """
    Validate incident data.
    Returns (error_message, status_code) if validation fails, (None, None) if valid.
    """
    if not data.get('title') or not data.get('description') or not data.get('severity'):
        return "Title, description, and severity cannot be empty", 400
    
    if not isinstance(data['title'], str):
        return "Title must be a string", 400
    
    if not isinstance(data['description'], str):
        return "Description must be a string", 400
    
    if not isinstance(data['severity'], str):
        return "Severity must be a string", 400
    
    # Capitalize severity
    data['severity'] = data['severity'].capitalize()
    
    if data['severity'] not in ['Low', 'Medium', 'High']:
        return "Severity must be 'Low', 'Medium', or 'High'", 400
    
    return None, None

@api.route('/')
def index():
    """Render the API documentation page"""
    return render_template('index.html')

@api.route('/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents from the database"""
    try:
        incidents = Incident.query.all()
        return jsonify([incident.to_dict() for incident in incidents])
    except Exception as e:
        logger.error(f"Error in get_incidents: {str(e)}")
        raise

@api.route('/incidents', methods=['POST'])
def log_new_incident():
    """Create a new incident in the database"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data provided in POST request")
            return jsonify({'error': 'No JSON data provided'}), 400
            
        error_message, status_code = validate_incident_data(data)
        if error_message:
            logger.warning(f"Invalid data provided: {error_message}")
            return jsonify({'error': error_message}), status_code
        
        incident = Incident(
            title=data['title'],
            description=data['description'],
            severity=data['severity']
        )
        
        db.session.add(incident)
        db.session.commit()
        logger.info(f"Successfully created new incident with ID: {incident.id}")
        return jsonify(incident.to_dict()), 201
    
    except Exception as e:
        logger.error(f"Error in log_new_incident: {str(e)}")
        raise

@api.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Get a specific incident by its ID"""
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            logger.warning(f"Incident not found with ID: {incident_id}")
            return jsonify({'error': 'Incident not found'}), 404
        return jsonify(incident.to_dict())
    except Exception as e:
        logger.error(f"Error in get_incident: {str(e)}")
        raise

@api.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """Delete a specific incident by its ID"""
    try:
        incident = Incident.query.get(incident_id)
        if incident is None:
            logger.warning(f"Attempted to delete non-existent incident with ID: {incident_id}")
            return jsonify({'error': 'Incident not found'}), 404
        
        db.session.delete(incident)
        db.session.commit()
        logger.info(f"Successfully deleted incident with ID: {incident_id}")
        return '', 204
    except Exception as e:
        logger.error(f"Error in delete_incident: {str(e)}")
        raise 

# health check
@api.route('/health', methods=['GET'])
def health_check():

    return jsonify(status="OK"), 200

#db health check
@api.route('/health/db', methods=['GET'])
def db_health_check():
    try:
        # Attempt to create a connection using SQLAlchemy
        engine = create_engine(db.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        
        # Execute a simple query to test the connection
        connection.execute('SELECT 1')

        connection.close()

        return jsonify(status="OK", db="MySQL", message="Database is healthy"), 200
    except exc.SQLAlchemyError as e:
        # If there is any error connecting to MySQL, return an error response
        return jsonify(status="ERROR", db="MySQL", message=str(e)), 500

@api.route('/favicon.ico')
def favicon():
    return '', 204  # No content, just to handle the request
