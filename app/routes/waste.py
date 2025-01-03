from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.waste import WasteLog, WASTE_CATEGORIES, WASTE_UNITS

waste_bp = Blueprint('waste', __name__)

@waste_bp.route('/log', methods=['POST'])
@jwt_required()
def create_log():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['category', 'amount', 'unit']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate category and unit
    if data['category'].lower() not in WASTE_CATEGORIES:
        return jsonify({'error': 'Invalid waste category'}), 400
    if data['unit'].lower() not in WASTE_UNITS:
        return jsonify({'error': 'Invalid unit'}), 400
    
    # Create waste log
    log = WasteLog(
        user_id=current_user_id,
        category=data['category'].lower(),
        amount=float(data['amount']),
        unit=data['unit'].lower()
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'Log created', 'log': log.to_dict()}), 201

@waste_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    current_user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    category = request.args.get('category')
    days = request.args.get('days', default=30, type=int)
    
    # Base query
    query = WasteLog.query.filter_by(user_id=current_user_id)
    
    # Apply filters
    if category:
        query = query.filter_by(category=category.lower())
    if days:
        date_limit = datetime.utcnow() - timedelta(days=days)
        query = query.filter(WasteLog.date >= date_limit)
    
    # Get results ordered by date
    logs = query.order_by(WasteLog.date.desc()).all()
    
    return jsonify({
        'logs': [log.to_dict() for log in logs]
    }), 200

@waste_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    current_user_id = get_jwt_identity()
    days = request.args.get('days', default=30, type=int)
    
    # Calculate date limit
    date_limit = datetime.utcnow() - timedelta(days=days)
    
    # Get total by category
    category_totals = db.session.query(
        WasteLog.category,
        func.sum(WasteLog.amount).label('total')
    ).filter(
        WasteLog.user_id == current_user_id,
        WasteLog.date >= date_limit
    ).group_by(WasteLog.category).all()
    
    # Get daily totals
    daily_totals = db.session.query(
        func.date(WasteLog.date).label('date'),
        func.sum(WasteLog.amount).label('total')
    ).filter(
        WasteLog.user_id == current_user_id,
        WasteLog.date >= date_limit
    ).group_by(func.date(WasteLog.date)).all()
    
    return jsonify({
        'category_totals': {cat: total for cat, total in category_totals},
        'daily_totals': {str(date): total for date, total in daily_totals},
        'days_tracked': days
    }), 200

@waste_bp.route('/log/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    current_user_id = get_jwt_identity()
    
    log = WasteLog.query.filter_by(id=log_id, user_id=current_user_id).first()
    if not log:
        return jsonify({'error': 'Log not found'}), 404
    
    db.session.delete(log)
    db.session.commit()
    
    return jsonify({'message': 'Log deleted'}), 200