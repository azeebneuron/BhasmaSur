from app import db
from app.models.social import ActivityFeed

def create_activity(user_id, activity_type, content, related_id=None):
    """
    Helper function to create activity feed entries
    """
    activity = ActivityFeed(
        user_id=user_id,
        activity_type=activity_type,
        content=content,
        related_id=related_id
    )
    db.session.add(activity)
    db.session.commit()
    return activity