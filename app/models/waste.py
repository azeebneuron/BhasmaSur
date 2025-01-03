from datetime import datetime
from app import db

class WasteLog(db.Model):
    __tablename__ = 'waste_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'amount': self.amount,
            'unit': self.unit,
            'date': self.date.isoformat()
        }

# Predefined categories and units for validation
WASTE_CATEGORIES = ['plastic', 'paper', 'glass', 'metal', 'organic', 'electronic']
WASTE_UNITS = ['kg', 'g', 'items']