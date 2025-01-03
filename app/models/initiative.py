from datetime import datetime, timezone
from app import db

class Initiative(db.Model):
    __tablename__ = 'initiatives'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime(timezone=True), nullable=False)
    
    @property
    def event_date_utc(self):
        """Ensure event_date is always timezone-aware in UTC"""
        if not self.event_date.tzinfo:
            return self.event_date.replace(tzinfo=timezone.utc)
        return self.event_date
    duration_hours = db.Column(db.Float, nullable=False)
    max_participants = db.Column(db.Integer)
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='upcoming')
    
    # Additional details
    requirements = db.Column(db.Text)
    contact_info = db.Column(db.String(200))
    image_url = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'event_date': self.event_date.isoformat(),
            'duration_hours': self.duration_hours,
            'max_participants': self.max_participants,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'requirements': self.requirements,
            'contact_info': self.contact_info,
            'image_url': self.image_url,
            'participant_count': len(self.participants)
        }

class InitiativeParticipant(db.Model):
    __tablename__ = 'initiative_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    initiative_id = db.Column(db.Integer, db.ForeignKey('initiatives.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='joined')
    
    # Relationship
    initiative = db.relationship('Initiative', backref=db.backref('participants', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'initiative_id': self.initiative_id,
            'user_id': self.user_id,
            'joined_at': self.joined_at.isoformat(),
            'status': self.status
        }