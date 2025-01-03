from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.business import Business, BusinessReview, BUSINESS_CATEGORIES
from app.models.user import User

business_bp = Blueprint('business', __name__)

@business_bp.route('', methods=['GET'])
def get_businesses():
    # Get query parameters
    category = request.args.get('category')
    rating = request.args.get('min_rating', type=float)
    verified = request.args.get('verified', type=bool)
    
    # Base query
    query = Business.query
    
    # Apply filters
    if category:
        if category not in BUSINESS_CATEGORIES:
            return jsonify({'error': 'Invalid category'}), 400
        query = query.filter_by(category=category)
    
    if rating is not None:
        query = query.filter(Business.rating >= rating)
    
    if verified is not None:
        query = query.filter_by(verified=verified)
    
    # Order by rating and get results
    businesses = query.order_by(Business.rating.desc()).all()
    
    return jsonify({
        'businesses': [business.to_dict() for business in businesses]
    }), 200

@business_bp.route('', methods=['POST'])
@jwt_required()
def create_business():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['name', 'category', 'address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate category
    if data['category'] not in BUSINESS_CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400
    
    # Create business
    business = Business(
        name=data['name'],
        description=data.get('description', ''),
        category=data['category'],
        address=data['address'],
        added_by=current_user_id
    )
    
    db.session.add(business)
    db.session.commit()
    
    return jsonify({'message': 'Business created', 'business': business.to_dict()}), 201

@business_bp.route('/<int:business_id>/review', methods=['POST'])
@jwt_required()
def add_review(business_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate business exists
    business = Business.query.get_or_404(business_id)
    
    # Validate rating
    rating = data.get('rating')
    if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Invalid rating. Must be between 1-5'}), 400
    
    # Check if user already reviewed this business
    existing_review = BusinessReview.query.filter_by(
        business_id=business_id,
        user_id=current_user_id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this business'}), 400
    
    # Create review
    review = BusinessReview(
        business_id=business_id,
        user_id=current_user_id,
        rating=rating,
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    business.update_rating()
    db.session.commit()
    
    return jsonify({'message': 'Review added', 'review': review.to_dict()}), 201

@business_bp.route('/<int:business_id>/verify', methods=['POST'])
@jwt_required()
def verify_business(business_id):
    current_user_id = get_jwt_identity()
    
    # Check if user is admin
    user = User.query.get(current_user_id)
    if not user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get business
    business = Business.query.get_or_404(business_id)
    business.verified = True
    db.session.commit()
    
    return jsonify({
        'message': 'Business verified',
        'business': business.to_dict()
    }), 200

@business_bp.route('/<int:business_id>/reviews', methods=['GET'])
def get_reviews(business_id):
    # Get business
    business = Business.query.get_or_404(business_id)
    
    # Get reviews ordered by date
    reviews = BusinessReview.query.filter_by(business_id=business_id)\
        .order_by(BusinessReview.created_at.desc()).all()
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews]
    }), 200