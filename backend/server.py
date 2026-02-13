from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from typing import Optional, List
from datetime import datetime, timezone

from models import (
    User, UserCreate, UserLogin, UserResponse, TokenResponse,
    Movie, MovieResponse, MovieListResponse,
    WatchHistory, WatchProgressUpdate, WatchRating, WatchHistoryResponse,
    InteractionCreate, Interaction,
    RecommendationRequest, RecommendationResponse,
    BehaviorSignal, UserBehaviorProfile,
    GroupSession, GroupSessionCreate, GroupSessionResponse, GroupSessionInvite, PlaybackState, ChatMessage
)
from auth import (
    get_password_hash, verify_password, create_access_token, get_current_user
)
from tmdb_service import fetch_popular_movies, fetch_movie_genres, search_movies, transform_tmdb_movie
from ml_service import recommendation_engine
from behavior_service import behavior_analyzer
from websocket_manager import manager

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="AI Movie Recommendation Platform")

# Create API router
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Auth Endpoints ====================

@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        preferences=user_data.preferences
    )
    
    # Hash password and store
    user_dict = user.model_dump()
    user_dict['password_hash'] = get_password_hash(user_data.password)
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    user_dict['updated_at'] = user_dict['updated_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Create token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(**user.model_dump())
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    user_doc = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(credentials.password, user_doc['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    access_token = create_access_token(data={"sub": user_doc['id']})
    
    user = User(**user_doc)
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(**user.model_dump())
    )

async def get_current_user_wrapper(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Wrapper to inject db dependency"""
    return await get_current_user(credentials, db)

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user_wrapper)):
    """Get current user"""
    return UserResponse(**current_user.model_dump())

@api_router.put("/auth/preferences")
async def update_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Update user preferences"""
    await db.users.update_one(
        {"id": current_user.id},
        {"$set": {"preferences": preferences, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    return {"message": "Preferences updated successfully"}

# ==================== Movie Endpoints ====================

@api_router.get("/movies", response_model=MovieListResponse)
async def get_movies(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    search: Optional[str] = None
):
    """Get movies with pagination and filtering"""
    query = {}
    if genre:
        query["genres"] = genre
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"overview": {"$regex": search, "$options": "i"}}
        ]
    
    total = await db.movies.count_documents(query)
    skip = (page - 1) * limit
    
    movies_cursor = db.movies.find(query, {"_id": 0}).skip(skip).limit(limit).sort("popularity", -1)
    movies = await movies_cursor.to_list(length=limit)
    
    return MovieListResponse(
        movies=[MovieResponse(**m) for m in movies],
        total=total,
        page=page,
        total_pages=(total + limit - 1) // limit
    )

@api_router.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str):
    """Get movie by ID"""
    movie = await db.movies.find_one({"id": movie_id}, {"_id": 0})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieResponse(**movie)

@api_router.get("/movies/search/query")
async def search_movies_endpoint(q: str, page: int = 1):
    """Search movies"""
    # Search in database first
    movies = await db.movies.find(
        {"$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"overview": {"$regex": q, "$options": "i"}}
        ]},
        {"_id": 0}
    ).limit(20).to_list(20)
    
    return {"movies": [MovieResponse(**m) for m in movies]}

# ==================== Recommendation Endpoints ====================

@api_router.get("/recommendations/personalized")
async def get_personalized_recommendations(
    limit: int = Query(20, le=100),
    current_user: User = Depends(get_current_user_wrapper)
):
    """Get personalized recommendations for user"""
    # Get user watch history
    watch_history = await db.watch_history.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).to_list(1000)
    
    # Get all movies
    all_movies = await db.movies.find({}, {"_id": 0}).to_list(10000)
    
    if not all_movies:
        return {"recommendations": []}
    # Create movie lookup
    movies_dict = {m["id"]: m for m in all_movies}
    
    # Generate user profile vector
    user_vector = recommendation_engine.generate_user_profile_vector(watch_history, movies_dict)
    
    # Get hybrid recommendations
    recommendations = recommendation_engine.hybrid_recommendations(
        user_id=current_user.id,
        user_vector=user_vector,
        candidate_movies=all_movies,
        watch_history=watch_history,
        top_k=limit
    )
    
    # Format response
    result = []
    for rec in recommendations:
        movie = rec["movie"]
        result.append(RecommendationResponse(
            movie=MovieResponse(**movie),
            score=rec["score"],
            reason=rec["reason"]
        ))
    
    return {"recommendations": result}

@api_router.get("/recommendations/trending")
async def get_trending_recommendations(limit: int = Query(20, le=100)):
    """Get trending movies"""
    movies = await db.movies.find(
        {},
        {"_id": 0}
    ).sort("popularity", -1).limit(limit).to_list(limit)
    
    return {
        "recommendations": [
            RecommendationResponse(
                movie=MovieResponse(**m),
                score=m.get("popularity", 0) / 100,
                reason="Trending now"
            )
            for m in movies
        ]
    }

@api_router.get("/recommendations/similar/{movie_id}")
async def get_similar_movies(movie_id: str, limit: int = Query(10, le=50)):
    """Get movies similar to given movie"""
    # Check if movie exists
    target_movie = await db.movies.find_one({"id": movie_id}, {"_id": 0})
    if not target_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get all movies
    all_movies = await db.movies.find({}, {"_id": 0}).to_list(10000)
    
    # Get similar movies
    similar = recommendation_engine.get_similar_movies(movie_id, all_movies, top_k=limit)
    
    # Fetch movie details
    result = []
    for movie_id, score in similar:
        movie = await db.movies.find_one({"id": movie_id}, {"_id": 0})
        if movie:
            result.append(RecommendationResponse(
                movie=MovieResponse(**movie),
                score=score,
                reason="Similar content and themes"
            ))
    
    return {"recommendations": result}

# ==================== Watch History Endpoints ====================

@api_router.post("/watch/start")
async def start_watching(
    movie_id: str,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Start watching a movie"""
    # Check if movie exists
    movie = await db.movies.find_one({"id": movie_id}, {"_id": 0})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if watch history exists
    existing = await db.watch_history.find_one(
        {"user_id": current_user.id, "movie_id": movie_id},
        {"_id": 0}
    )
    
    if existing:
        # Update watch count
        await db.watch_history.update_one(
            {"id": existing["id"]},
            {
                "$inc": {"watch_count": 1},
                "$set": {"last_watched_at": datetime.now(timezone.utc).isoformat()}
            }
        )
        return {"message": "Continuing watch", "watch_id": existing["id"]}
    else:
        # Create new watch history
        watch = WatchHistory(
            user_id=current_user.id,
            movie_id=movie_id,
            total_duration=movie.get("runtime", 120) * 60  # Convert to seconds
        )
        watch_dict = watch.model_dump()
        watch_dict['last_watched_at'] = watch_dict['last_watched_at'].isoformat()
        watch_dict['created_at'] = watch_dict['created_at'].isoformat()
        
        await db.watch_history.insert_one(watch_dict)
        return {"message": "Started watching", "watch_id": watch.id}

@api_router.put("/watch/progress")
async def update_watch_progress(
    progress: WatchProgressUpdate,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Update watch progress"""
    completed = progress.progress_seconds >= progress.total_duration * 0.9  # 90% completion
    
    await db.watch_history.update_one(
        {"user_id": current_user.id, "movie_id": progress.movie_id},
        {
            "$set": {
                "progress_seconds": progress.progress_seconds,
                "total_duration": progress.total_duration,
                "completed": completed,
                "last_watched_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {"message": "Progress updated", "completed": completed}

@api_router.post("/watch/rate")
async def rate_movie(
    rating_data: WatchRating,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Rate a movie"""
    # Update watch history with rating
    result = await db.watch_history.update_one(
        {"user_id": current_user.id, "movie_id": rating_data.movie_id},
        {"$set": {"rating": rating_data.rating}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Watch history not found")
    
    # Create interaction record
    interaction = Interaction(
        user_id=current_user.id,
        movie_id=rating_data.movie_id,
        action="rate",
        value=rating_data.rating
    )
    interaction_dict = interaction.model_dump()
    interaction_dict['timestamp'] = interaction_dict['timestamp'].isoformat()
    
    await db.interactions.insert_one(interaction_dict)
    
    return {"message": "Rating saved"}

@api_router.get("/watch/history")
async def get_watch_history(
    current_user: User = Depends(get_current_user_wrapper),
    limit: int = Query(50, le=200)
):
    """Get user watch history"""
    history = await db.watch_history.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).sort("last_watched_at", -1).limit(limit).to_list(limit)
    
    # Fetch movie details
    result = []
    for h in history:
        movie = await db.movies.find_one({"id": h["movie_id"]}, {"_id": 0})
        if movie:
            result.append({
                **h,
                "movie": MovieResponse(**movie)
            })
    
    return {"history": result}

# ==================== Interactions ====================

@api_router.post("/interactions")
async def create_interaction(
    interaction_data: InteractionCreate,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Create user interaction (like, bookmark, etc.)"""
    interaction = Interaction(
        user_id=current_user.id,
        movie_id=interaction_data.movie_id,
        action=interaction_data.action,
        value=interaction_data.value
    )
    interaction_dict = interaction.model_dump()
    interaction_dict['timestamp'] = interaction_dict['timestamp'].isoformat()
    
    await db.interactions.insert_one(interaction_dict)
    
    return {"message": "Interaction saved"}

# ==================== Admin/Data Management ====================

@api_router.post("/admin/sync-movies")
async def sync_movies_from_tmdb():
    """Sync movies from TMDB (admin endpoint)"""
    try:
        # Fetch genres
        genre_map = await fetch_movie_genres()
        
        # Fetch popular movies (multiple pages)
        all_tmdb_movies = []
        for page in range(1, 6):  # Fetch 5 pages = ~100 movies
            movies = await fetch_popular_movies(page)
            all_tmdb_movies.extend(movies)
        
        # Transform and save to database
        saved_count = 0
        for tmdb_movie in all_tmdb_movies:
            movie_data = transform_tmdb_movie(tmdb_movie, genre_map)
            
            # Check if exists
            existing = await db.movies.find_one({"tmdb_id": movie_data["tmdb_id"]}, {"_id": 0})
            
            if not existing:
                # Create new movie
                movie = Movie(**movie_data)
                
                # Generate embedding
                try:
                    embedding = recommendation_engine.generate_movie_embedding(movie_data)
                    movie.embedding = embedding
                except Exception as e:
                    logger.error(f"Error generating embedding: {e}")
                
                movie_dict = movie.model_dump()
                movie_dict['created_at'] = movie_dict['created_at'].isoformat()
                
                await db.movies.insert_one(movie_dict)
                saved_count += 1
        
        return {"message": f"Synced {saved_count} new movies from TMDB"}
    
    except Exception as e:
        logger.error(f"Error syncing movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/admin/stats")
async def get_platform_stats():
    """Get platform statistics"""
    total_users = await db.users.count_documents({})
    total_movies = await db.movies.count_documents({})
    total_watches = await db.watch_history.count_documents({})
    total_interactions = await db.interactions.count_documents({})
    
    return {
        "total_users": total_users,
        "total_movies": total_movies,
        "total_watches": total_watches,
        "total_interactions": total_interactions
    }

# ==================== Root Endpoint ====================

@api_router.get("/")


# ==================== Phase 2: Behavioral Intelligence ====================

@api_router.get("/behavior/profile")
async def get_behavior_profile(current_user: User = Depends(get_current_user_wrapper)):
    """Get user's behavioral profile"""
    # Get watch history
    watch_history = await db.watch_history.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).to_list(1000)
    
    # Analyze patterns
    patterns = behavior_analyzer.analyze_watch_patterns(watch_history)
    
    # Get recent interactions
    interactions = await db.interactions.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50).to_list(50)
    
    # Detect mood
    mood = behavior_analyzer.detect_mood(watch_history, interactions)
    
    profile = UserBehaviorProfile(
        user_id=current_user.id,
        preferred_time=patterns.get('preferred_time'),
        avg_session_duration=patterns.get('avg_session_duration', 0),
        completion_rate=patterns.get('completion_rate', 0),
        binge_watching=patterns.get('binge_watching', False),
        current_mood=mood,
        preferred_genres=patterns.get('preferred_genres', [])
    )
    
    return profile

@api_router.post("/behavior/signal")
async def record_behavior_signal(
    signal: BehaviorSignal,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Record a behavioral signal"""
    signal.user_id = current_user.id
    signal_dict = signal.model_dump()
    signal_dict['timestamp'] = signal_dict['timestamp'].isoformat()
    
    await db.behavior_signals.insert_one(signal_dict)
    
    return {"message": "Signal recorded"}

@api_router.get("/recommendations/intelligent")
async def get_intelligent_recommendations(
    limit: int = Query(20, le=100),
    current_user: User = Depends(get_current_user_wrapper)
):
    """Get intelligent recommendations enhanced with behavioral analysis"""
    # Get watch history
    watch_history = await db.watch_history.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).to_list(1000)
    
    # Get recent interactions
    interactions = await db.interactions.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50).to_list(50)
    
    # Analyze behavior
    patterns = behavior_analyzer.analyze_watch_patterns(watch_history)
    mood = behavior_analyzer.detect_mood(watch_history, interactions)
    
    # Get all movies
    all_movies = await db.movies.find({}, {"_id": 0}).to_list(10000)
    
    if not all_movies:
        return {"recommendations": []}
    
    # Create movie lookup
    movies_dict = {m["id"]: m for m in all_movies}
    
    # Generate user profile vector
    user_vector = recommendation_engine.generate_user_profile_vector(watch_history, movies_dict)
    
    # Get base recommendations
    base_recs = recommendation_engine.hybrid_recommendations(
        user_id=current_user.id,
        user_vector=user_vector,
        candidate_movies=all_movies,
        watch_history=watch_history,
        top_k=limit * 2  # Get more for behavior filtering
    )
    
    # Enhance with behavioral intelligence
    enhanced_recs = behavior_analyzer.enhance_recommendations_with_behavior(
        base_recs,
        patterns,
        mood
    )
    
    # Format response
    result = []
    for rec in enhanced_recs[:limit]:
        movie = rec["movie"]
        behavior_factors = rec.get('behavior_factors', {})
        reason = f"{rec['reason']} • Mood: {behavior_factors.get('mood', 'neutral')}"
        
        result.append(RecommendationResponse(
            movie=MovieResponse(**movie),
            score=rec["score"],
            reason=reason
        ))
    
    return {"recommendations": result, "mood": mood, "patterns": patterns}

# ==================== Phase 3: Group Watch Sessions ====================

@api_router.post("/groups/create", response_model=GroupSessionResponse)
async def create_group_session(
    session_data: GroupSessionCreate,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Create a new group watch session"""
    # Check if movie exists
    movie = await db.movies.find_one({"id": session_data.movie_id}, {"_id": 0})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Create session
    session = GroupSession(
        name=session_data.name or f"{current_user.name}'s Watch Party",
        host_user_id=current_user.id,
        member_ids=[current_user.id],
        movie_id=session_data.movie_id,
    )
    
    session_dict = session.model_dump()
    session_dict['created_at'] = session_dict['created_at'].isoformat()
    session_dict['updated_at'] = session_dict['updated_at'].isoformat()
    
    await db.group_sessions.insert_one(session_dict)
    
    return GroupSessionResponse(
        **session.model_dump(),
        movie=MovieResponse(**movie),
        member_count=1
    )

@api_router.get("/groups/{session_id}", response_model=GroupSessionResponse)
async def get_group_session(
    session_id: str,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Get group session details"""
    session = await db.group_sessions.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if user is a member
    if current_user.id not in session.get('member_ids', []):
        raise HTTPException(status_code=403, detail="Not a session member")
    
    # Get movie details
    movie = await db.movies.find_one({"id": session.get('movie_id')}, {"_id": 0})
    
    return GroupSessionResponse(
        **session,
        movie=MovieResponse(**movie) if movie else None,
        member_count=len(session.get('member_ids', []))
    )

@api_router.post("/groups/{session_id}/join")
async def join_group_session(
    session_id: str,
    current_user: User = Depends(get_current_user_wrapper)
):
    """Join a group watch session"""
    session = await db.group_sessions.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Add user to members if not already in
    if current_user.id not in session.get('member_ids', []):
        await db.group_sessions.update_one(
            {"id": session_id},
            {
                "$push": {"member_ids": current_user.id},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
            }
        )
    
    return {"message": "Joined session successfully"}

@api_router.get("/groups")
async def get_user_group_sessions(
    current_user: User = Depends(get_current_user_wrapper)
):
    """Get all group sessions for current user"""
    sessions = await db.group_sessions.find(
        {"member_ids": current_user.id, "status": "active"},
        {"_id": 0}
    ).to_list(100)
    
    result = []
    for session in sessions:
        movie = await db.movies.find_one({"id": session.get('movie_id')}, {"_id": 0})
        result.append(GroupSessionResponse(
            **session,
            movie=MovieResponse(**movie) if movie else None,
            member_count=len(session.get('member_ids', []))
        ))
    
    return {"sessions": result}

@api_router.post("/groups/{session_id}/end")
async def end_group_session(
    session_id: str,
    current_user: User = Depends(get_current_user_wrapper)
):
    """End a group watch session (host only)"""
    session = await db.group_sessions.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get('host_user_id') != current_user.id:
        raise HTTPException(status_code=403, detail="Only host can end session")
    
    await db.group_sessions.update_one(
        {"id": session_id},
        {
            "$set": {
                "status": "ended",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {"message": "Session ended"}

# ==================== WebSocket for Real-time Sync ====================

@app.websocket("/ws/group/{session_id}/{user_id}")
async def websocket_group_session(websocket: WebSocket, session_id: str, user_id: str):
    """WebSocket endpoint for real-time group session sync"""
    await manager.connect(websocket, session_id, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get('type')
            
            if message_type == 'playback_update':
                # Sync playback state
                state = data.get('state', {})
                await manager.update_playback_state(session_id, state, websocket)
            
            elif message_type == 'chat_message':
                # Broadcast chat message
                message = data.get('message', '')
                await manager.send_message(session_id, user_id, message, websocket)
            
            elif message_type == 'seek':
                # Sync seek position
                position = data.get('position', 0)
                await manager.update_playback_state(session_id, {
                    'position': position,
                    'is_playing': data.get('is_playing', False)
                }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id, user_id)
        await manager.broadcast(session_id, {
            'type': 'user_left',
            'user_id': user_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

async def root():
    return {
        "message": "AI Movie Recommendation Platform API",
        "version": "1.0.0",
        "status": "active"
    }

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
