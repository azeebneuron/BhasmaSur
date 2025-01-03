from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models.initiative import Initiative, InitiativeParticipant
from app.utils.activity import create_activity

initiative_bp = Blueprint('initiative', __name__)

@initiative_bp.route('', methods=['POST'])
@jwt_required()
def create_initiative():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'location', 'event_date', 'duration_hours']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Convert the event date string to a timezone-aware datetime object
        event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
        
        # Get current time as timezone-aware datetime
        current_time = datetime.now(timezone.utc)
        
        if event_date < current_time:
            return jsonify({'error': 'Event date cannot be in the past'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    initiative = Initiative(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        event_date=event_date,
        duration_hours=float(data['duration_hours']),
        max_participants=data.get('max_participants'),
        requirements=data.get('requirements'),
        contact_info=data.get('contact_info'),
        image_url=data.get('image_url'),
        created_by=current_user_id
    )
    
    db.session.add(initiative)
    db.session.commit()
    
    # Create activity feed entry
    create_activity(
        current_user_id,
        'initiative_created',
        f"Created new initiative: {initiative.title}",
        initiative.id
    )
    
    return jsonify({
        'message': 'Initiative created successfully',
        'initiative': initiative.to_dict()
    }), 201

@initiative_bp.route('', methods=['GET'])
def get_initiatives():
    # Get query parameters
    status = request.args.get('status', 'upcoming')
    location = request.args.get('location')
    
    # Base query
    query = Initiative.query
    
    # Filter by status
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Filter by location if provided
    if location:
        query = query.filter(Initiative.location.ilike(f'%{location}%'))
    
    # Get current time as timezone-aware datetime
    current_time = datetime.now(timezone.utc)
    
    # Update status based on event date
    initiatives = query.all()
    for initiative in initiatives:
        # Make sure initiative.event_date is timezone-aware
        if not initiative.event_date.tzinfo:
            initiative_date = initiative.event_date.replace(tzinfo=timezone.utc)
        else:
            initiative_date = initiative.event_date
            
        if initiative_date < current_time and initiative.status == 'upcoming':
            initiative.status = 'completed'
    
    db.session.commit()
    
    # Order by date
    initiatives = sorted(initiatives, key=lambda x: x.event_date)
    
    return jsonify({
        'initiatives': [init.to_dict() for init in initiatives]
    }), 200

@initiative_bp.route('/<int:initiative_id>', methods=['GET'])
def get_initiative(initiative_id):
    initiative = Initiative.query.get_or_404(initiative_id)
    return jsonify({'initiative': initiative.to_dict()}), 200

@initiative_bp.route('/<int:initiative_id>/join', methods=['POST'])
@jwt_required()
def join_initiative(initiative_id):
    current_user_id = int(get_jwt_identity())
    
    initiative = Initiative.query.get_or_404(initiative_id)
    
    # Check if initiative is upcoming
    # current_time = datetime.now(timezone.utc)
    # if initiative.event_date < current_time:
    #     return jsonify({'error': 'Cannot join past initiatives'}), 400
    
    if initiative.status != 'upcoming':
        return jsonify({'error': 'Can only join upcoming initiatives'}), 400
    
    # Check if already joined
    existing_participant = InitiativeParticipant.query.filter_by(
        initiative_id=initiative_id,
        user_id=current_user_id,
        status='joined'
    ).first()
    
    if existing_participant:
        return jsonify({'error': 'Already joined this initiative'}), 400
    
    # Check max participants limit
    if initiative.max_participants and len(initiative.participants) >= initiative.max_participants:
        return jsonify({'error': 'Initiative has reached maximum participants'}), 400
    
    participant = InitiativeParticipant(
        initiative_id=initiative_id,
        user_id=current_user_id
    )
    
    db.session.add(participant)
    db.session.commit()
    
    # Create activity feed entry
    create_activity(
        current_user_id,
        'initiative_joined',
        f"Joined initiative: {initiative.title}",
        initiative.id
    )
    
    return jsonify({
        'message': 'Successfully joined initiative',
        'participant': participant.to_dict()
    }), 200

@initiative_bp.route('/<int:initiative_id>/participants', methods=['GET'])
def get_participants(initiative_id):
    initiative = Initiative.query.get_or_404(initiative_id)
    
    participants = InitiativeParticipant.query.filter_by(
        initiative_id=initiative_id,
        status='joined'
    ).all()
    
    return jsonify({
        'participants': [participant.to_dict() for participant in participants]
    }), 200

@initiative_bp.route('/<int:initiative_id>', methods=['PUT'])
@jwt_required()
def update_initiative(initiative_id):
    current_user_id = get_jwt_identity()
    
    initiative = Initiative.query.get_or_404(initiative_id)
    
    # Check if user is the creator
    if initiative.created_by != current_user_id:
        return jsonify({'error': 'Unauthorized to update this initiative'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'title' in data:
        initiative.title = data['title']
    if 'description' in data:
        initiative.description = data['description']
    if 'requirements' in data:
        initiative.requirements = data['requirements']
    if 'contact_info' in data:
        initiative.contact_info = data['contact_info']
    if 'status' in data:
        initiative.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Initiative updated successfully',
        'initiative': initiative.to_dict()
    }), 200