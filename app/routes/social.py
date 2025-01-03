from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.social import Achievement, ActivityFeed
from sqlalchemy import desc
from datetime import datetime, timedelta

social_bp = Blueprint('social', __name__)

# Following/Followers
@social_bp.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return jsonify({'error': 'Cannot follow yourself'}), 400
    
    current_user = User.query.get_or_404(current_user_id)
    user_to_follow = User.query.get_or_404(user_id)
    
    if current_user.is_following(user_to_follow):
        return jsonify({'error': 'Already following this user'}), 400
    
    current_user.follow(user_to_follow)
    db.session.commit()
    
    # Create activity feed entry
    activity = ActivityFeed(
        user_id=current_user_id,
        activity_type='follow',
        content=f"Started following {user_to_follow.username}",
        related_id=user_id
    )
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'message': f'Now following {user_to_follow.username}'}), 200

@social_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    
    current_user = User.query.get_or_404(current_user_id)
    user_to_unfollow = User.query.get_or_404(user_id)
    
    if not current_user.is_following(user_to_unfollow):
        return jsonify({'error': 'Not following this user'}), 400
    
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    
    return jsonify({'message': f'Unfollowed {user_to_unfollow.username}'}), 200

# Activity Feed
@social_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_activity_feed():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    # Get activities from followed users and self
    activities = ActivityFeed.query.filter(
        (ActivityFeed.user_id.in_([user.id for user in current_user.following])) |
        (ActivityFeed.user_id == current_user_id)
    ).order_by(ActivityFeed.created_at.desc()).limit(50).all()
    
    return jsonify({
        'activities': [activity.to_dict() for activity in activities]
    }), 200

# Achievements
@social_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    current_user_id = get_jwt_identity()
    
    achievements = Achievement.query.filter_by(user_id=current_user_id)\
        .order_by(Achievement.created_at.desc()).all()
    
    return jsonify({
        'achievements': [achievement.to_dict() for achievement in achievements]
    }), 200

# Leaderboard
@social_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    timeframe = request.args.get('timeframe', 'week')  # week, month, all-time
    
    if timeframe == 'week':
        date_limit = datetime.utcnow() - timedelta(days=7)
    elif timeframe == 'month':
        date_limit = datetime.utcnow() - timedelta(days=30)
    else:
        date_limit = datetime.min
    
    # Get users with their waste reduction stats
    from app.models.waste import WasteLog
    
    leaderboard = db.session.query(
        User,
        db.func.count(WasteLog.id).label('total_logs'),
        db.func.sum(WasteLog.amount).label('total_amount')
    ).join(WasteLog).filter(
        WasteLog.date >= date_limit
    ).group_by(User.id).order_by(
        db.desc('total_logs'),
        db.desc('total_amount')
    ).limit(10).all()
    
    return jsonify({
        'timeframe': timeframe,
        'leaders': [{
            'username': user.username,
            'total_logs': total_logs,
            'total_amount': float(total_amount) if total_amount else 0
        } for user, total_logs, total_amount in leaderboard]
    }), 200

# Helper function to create activity feed entries
def create_activity(user_id, activity_type, content, related_id=None):
    activity = ActivityFeed(
        user_id=user_id,
        activity_type=activity_type,
        content=content,
        related_id=related_id
    )
    db.session.add(activity)
    db.session.commit()
    return activity