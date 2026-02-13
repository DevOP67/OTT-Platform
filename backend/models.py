from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# User Models
class UserPreferences(BaseModel):
    favorite_genres: List[str] = Field(default_factory=list)
    mood: Optional[str] = None
    preferred_languages: List[str] = Field(default=["en"])

class UserBase(BaseModel):
    email: EmailStr
    name: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    preferences: UserPreferences

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Movie Models
class Movie(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tmdb_id: int
    title: str
    overview: str
    genres: List[str]
    release_date: str
    rating: float
    poster_url: str
    backdrop_url: str
    runtime: int
    language: str = "en"
    embedding: Optional[List[float]] = None
    video_url: Optional[str] = None
    popularity: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MovieResponse(BaseModel):
    id: str
    tmdb_id: int
    title: str
    overview: str
    genres: List[str]
    release_date: str
    rating: float
    poster_url: str
    backdrop_url: str
    runtime: int
    language: str
    popularity: float

class MovieListResponse(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    total_pages: int

# Watch History Models
class WatchProgressUpdate(BaseModel):
    movie_id: str
    progress_seconds: int
    total_duration: int

class WatchRating(BaseModel):
    movie_id: str
    rating: float = Field(ge=0.5, le=5.0)

class WatchHistory(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    movie_id: str
    progress_seconds: int = 0
    total_duration: int
    completed: bool = False
    rating: Optional[float] = None
    watch_count: int = 1
    last_watched_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WatchHistoryResponse(BaseModel):
    id: str
    movie_id: str
    progress_seconds: int
    total_duration: int
    completed: bool
    rating: Optional[float]
    watch_count: int
    last_watched_at: datetime
    movie: Optional[MovieResponse] = None

# Interaction Models
class InteractionCreate(BaseModel):
    movie_id: str
    action: str  # "like", "skip", "bookmark", "rate"
    value: Optional[float] = None

class Interaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    movie_id: str
    action: str
    value: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Recommendation Models
class RecommendationRequest(BaseModel):
    limit: int = Field(default=20, le=100)
    genres: Optional[List[str]] = None
    mood: Optional[str] = None

class RecommendationResponse(BaseModel):
    movie: MovieResponse
    score: float
    reason: str

# Behavioral Signal Models (Phase 2)
class BehaviorSignal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    signal_type: str  # "watch_time", "pause_frequency", "skip", "rewatch"
    movie_id: Optional[str] = None
    value: float
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserBehaviorProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    preferred_time: Optional[str] = None  # morning, afternoon, evening, night
    avg_session_duration: int = 0  # minutes
    completion_rate: float = 0.0
    binge_watching: bool = False
    current_mood: str = "neutral"
    preferred_genres: List[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# Group Session Models (Phase 3)
class GroupSessionCreate(BaseModel):
    movie_id: str
    name: Optional[str] = None

class GroupSessionInvite(BaseModel):
    session_id: str
    user_email: str

class GroupSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    host_user_id: str
    member_ids: List[str] = Field(default_factory=list)
    movie_id: str
    current_position: int = 0
    is_playing: bool = False
    status: str = "active"  # active, paused, ended
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GroupSessionResponse(BaseModel):
    id: str
    name: str
    host_user_id: str
    member_ids: List[str]
    movie_id: str
    current_position: int
    is_playing: bool
    status: str
    movie: Optional[MovieResponse] = None
    member_count: int = 0

class PlaybackState(BaseModel):
    position: int  # seconds
    is_playing: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    user_id: str
    user_name: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
