from datetime import datetime
from  flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Incident(db.Model):
    """
    Represents an incident in the system.
    
    Attributes:
        id (int): Primary key
        title (str): Title of the incident (max 200 chars)
        description (str): Detailed description of the incident
        severity (str): Severity level (must be one of: low, medium, high)
        reported_at (datetime): When the incident was reported
    """
    __tablename__ = "incidents"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    reported_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        """
        Convert the incident to a dictionary representation.
        
        Returns:
            dict: Dictionary containing incident data
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'reported_at': self.reported_at.isoformat() if self.reported_at else None
        } 