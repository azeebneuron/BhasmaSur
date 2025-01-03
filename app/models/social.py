from datetime import datetime
from app import db

# User following relationship table
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    badge_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'badge_type': self.badge_type,
            'created_at': self.created_at.isoformat()
        }

class ActivityFeed(db.Model):
    __tablename__ = 'activity_feed'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'waste_log', 'achievement', 'review', etc.
    content = db.Column(db.Text)
    related_id = db.Column(db.Integer)  # ID of related object (waste_log, achievement, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'content': self.content,
            'related_id': self.related_id,
            'created_at': self.created_at.isoformat()
        }

# Update User model to include following relationship
from app.models.user import User

User.following = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == User.id),
    secondaryjoin=(followers.c.followed_id == User.id),
    backref=db.backref('followers', lazy='dynamic'),
    lazy='dynamic'
)

# Add methods to User model for following functionality
def follow(self, user):
    if not self.is_following(user):
        self.following.append(user)

def unfollow(self, user):
    if self.is_following(user):
        self.following.remove(user)

def is_following(self, user):
    return self.following.filter(followers.c.followed_id == user.id).count() > 0

def followed_activities(self):
    return ActivityFeed.query.join(
        followers, (followers.c.followed_id == ActivityFeed.user_id)
    ).filter(followers.c.follower_id == self.id)

# Add methods to User class
User.follow = follow
User.unfollow = unfollow
User.is_following = is_following
User.followed_activities = followed_activities