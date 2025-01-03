from datetime import datetime
from app import db

# Predefined categories for validation
BUSINESS_CATEGORIES = [
    'zero_waste_store',
    'sustainable_fashion',
    'organic_food',
    'renewable_energy',
    'eco_friendly_products',
    'repair_service',
    'second_hand_store',
    'vegan_restaurant'
]

class Business(db.Model):
    __tablename__ = 'businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text)
    rating = db.Column(db.Float, default=0)
    verified = db.Column(db.Boolean, default=False)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('BusinessReview', backref='business', lazy=True, cascade='all, delete-orphan')
    
    def update_rating(self):
        """Update average rating based on reviews"""
        if self.reviews:
            self.rating = sum(review.rating for review in self.reviews) / len(self.reviews)
        else:
            self.rating = 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'address': self.address,
            'rating': self.rating,
            'verified': self.verified,
            'added_by': self.added_by,
            'created_at': self.created_at.isoformat(),
            'review_count': len(self.reviews)
        }

class BusinessReview(db.Model):
    __tablename__ = 'business_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_id': self.business_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }