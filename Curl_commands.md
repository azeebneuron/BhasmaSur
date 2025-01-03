
1. **Sign Up New User**:
```bash
curl -X POST http://localhost:5000/api/auth/signup \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}'
```

2. **Login**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "password123"
}'
```

3. **Get Profile** (use the access_token from login response):
```bash
curl -X GET http://localhost:5000/api/auth/profile \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

4. **Login as Admin** (default admin credentials):
```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
    "email": "admin@ecoconnect.com",
    "password": "admin123"
}'
```

5. **Refresh Token** (use the refresh_token from login response):
```bash
curl -X POST http://localhost:5000/api/auth/refresh \
-H "Authorization: Bearer YOUR_REFRESH_TOKEN_HERE"
```

You can save the access token in a variable for easier testing:
```bash
# Save token after login
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "password123"
}' | jq -r .access_token)

# Use saved token
curl -X GET http://localhost:5000/api/auth/profile \
-H "Authorization: Bearer $TOKEN"
```

---

Here are the curl commands to test the waste tracking endpoints:

1. **Add Waste Log** (requires auth token):
```bash
curl -X POST http://localhost:5000/api/waste/log \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "category": "plastic",
    "amount": 0.5,
    "unit": "kg"
}'
```

2. **Get All Logs** (with optional filters):
```bash
# All logs from last 30 days
curl -X GET http://localhost:5000/api/waste/logs \
-H "Authorization: Bearer YOUR_TOKEN"

# Filter by category and days
curl -X GET "http://localhost:5000/api/waste/logs?category=plastic&days=7" \
-H "Authorization: Bearer YOUR_TOKEN"
```

3. **Get Statistics**:
```bash
# Get stats for last 30 days
curl -X GET http://localhost:5000/api/waste/stats \
-H "Authorization: Bearer YOUR_TOKEN"

# Get stats for specific period
curl -X GET "http://localhost:5000/api/waste/stats?days=7" \
-H "Authorization: Bearer YOUR_TOKEN"
```

4. **Delete a Log**:
```bash
curl -X DELETE http://localhost:5000/api/waste/log/1 \
-H "Authorization: Bearer YOUR_TOKEN"
```

The waste tracking system includes:
- Predefined categories and units for consistency
- CRUD operations for waste logs
- Filtering by category and date range
- Statistics calculation (totals by category and daily totals)
- User-specific data access

---

Let's implement the eco-friendly business directory next. We'll create:
1. Business model
2. Rating/review system
3. Search and filter functionality

Here are the curl commands to test the business directory endpoints:

1. **Get All Businesses**:
```bash
# Get all businesses
curl -X GET http://localhost:5000/api/businesses

# With filters
curl -X GET "http://localhost:5000/api/businesses?category=zero_waste_store&min_rating=4&verified=true"
```

2. **Add New Business** (requires auth):
```bash
curl -X POST http://localhost:5000/api/businesses \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "name": "Green Earth Store",
    "description": "Zero waste grocery store",
    "category": "zero_waste_store",
    "address": "123 Eco Street"
}'
```

3. **Add Review** (requires auth):
```bash
curl -X POST http://localhost:5000/api/businesses/1/review \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "rating": 5,
    "comment": "Great eco-friendly products!"
}'
```

4. **Get Reviews for a Business**:
```bash
curl -X GET http://localhost:5000/api/businesses/1/reviews
```

5. **Verify Business** (admin only):
```bash
curl -X POST http://localhost:5000/api/businesses/1/verify \
-H "Authorization: Bearer ADMIN_TOKEN"
```

The business directory includes:
- CRUD operations for businesses
- Review and rating system
- Business verification by admin
- Search and filter functionality
- Predefined business categories

---

Now let's create the social feature routes:

Here are the curl commands to test the social features:

1. **Follow a User**:
```bash
curl -X POST http://localhost:5000/api/social/follow/2 \
-H "Authorization: Bearer YOUR_TOKEN"
```

2. **Unfollow a User**:
```bash
curl -X POST http://localhost:5000/api/social/unfollow/2 \
-H "Authorization: Bearer YOUR_TOKEN"
```

3. **Get Activity Feed**:
```bash
curl -X GET http://localhost:5000/api/social/feed \
-H "Authorization: Bearer YOUR_TOKEN"
```

4. **Get User Achievements**:
```bash
curl -X GET http://localhost:5000/api/social/achievements \
-H "Authorization: Bearer YOUR_TOKEN"
```

5. **Get Leaderboard**:
```bash
# Weekly leaderboard
curl -X GET http://localhost:5000/api/social/leaderboard?timeframe=week

# Monthly leaderboard
curl -X GET http://localhost:5000/api/social/leaderboard?timeframe=month

# All-time leaderboard
curl -X GET http://localhost:5000/api/social/leaderboard?timeframe=all-time
```

The social features include:
1. **Following System**
   - Follow/unfollow users
   - Track followers and following

2. **Activity Feed**
   - Shows activities from followed users
   - Different activity types (waste logs, achievements, follows)
   - Chronological order

3. **Achievements**
   - Track user achievements
   - Different badge types
   - Achievement history

4. **Leaderboard**
   - Weekly/monthly/all-time rankings
   - Based on waste reduction activities
   - Top 10 users displayed

5. **Integration with Existing Features**
   - Activities created for waste logs
   - Activities for business reviews
   - Following notifications

---

Here are the curl commands to test the initiative features:

1. **Create an Initiative**:
```bash
curl -X POST http://localhost:5000/api/initiatives \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Marina Beach Cleanup",
    "description": "Join us for a community beach cleanup drive",
    "location": "Marina Beach, Chennai",
    "event_date": "2025-01-15T09:00:00Z",
    "duration_hours": 3,
    "max_participants": 50,
    "requirements": "Please bring gloves and water bottle",
    "contact_info": "Contact: John at 1234567890"
}'
```

2. **Get All Initiatives**:
```bash
# Get all upcoming initiatives
curl -X GET http://localhost:5000/api/initiatives

# Filter by location
curl -X GET "http://localhost:5000/api/initiatives?location=Marina&status=upcoming"
```

3. **Join an Initiative**:
```bash
curl -X POST http://localhost:5000/api/initiatives/1/join \
-H "Authorization: Bearer YOUR_TOKEN"
```

4. **Leave an Initiative**:
```bash
curl -X POST http://localhost:5000/api/initiatives/1/leave \
-H "Authorization: Bearer YOUR_TOKEN"
```

5. **Get Initiative Details**:
```bash
curl -X GET http://localhost:5000/api/initiatives/1
```

6. **Get Initiative Participants**:
```bash
curl -X GET http://localhost:5000/api/initiatives/1/participants
```

7. **Update Initiative** (creator only):
```bash
curl -X PUT http://localhost:5000/api/initiatives/1 \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Updated: Marina Beach Cleanup",
    "description": "Updated description",
    "status": "completed"
}'
```

The initiative system includes:
1. **Creation and Management**
   - Create community initiatives
   - Set date, time, location
   - Specify max participants
   - Add requirements and contact info
   - Update initiative details

2. **Participation**
   - Join/leave initiatives
   - Track participant count
   - Prevent joining full initiatives
   - View participant list

3. **Discovery**
   - List all initiatives
   - Filter by status and location
   - View detailed information

4. **Integration with Social Features**
   - Activity feed entries for creating/joining initiatives
   - Social sharing capabilities

