# AI-Powered Movie Recommendation & Streaming Platform
## System Architecture Documentation

---

## 1. Overview

This platform delivers intelligent movie recommendations using AI/ML with support for personalized streaming, mood-based filtering, and group watch capabilities. Built with microservices architecture for scalability and production readiness.

### Key Features
- **AI-Powered Recommendations**: Hybrid collaborative + content-based filtering
- **Behavioral Intelligence**: Watch patterns, mood detection, preference learning
- **Mock Streaming**: HLS-ready video playback with progress tracking
- **Group Sessions**: Multi-user synchronized watch experience
- **Real-time Updates**: WebSocket-based notifications

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   React SPA (TypeScript + Tailwind)                       │  │
│  │   - Movie Browser  - Player  - Recommendations            │  │
│  │   - User Profile   - Groups  - Real-time Notifications    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTPS/WSS
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   FastAPI Backend (Main Service)                          │  │
│  │   - Authentication (JWT)    - User Management             │  │
│  │   - Movie Catalog API       - Watch History               │  │
│  │   - Group Session API       - WebSocket Server            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────┬──────────────────┬───────────────────────────┐
│  ML Service      │ Streaming Svc    │   Data Layer              │
│  ┌────────────┐  │ ┌─────────────┐  │  ┌──────────────────────┐ │
│  │ FastAPI    │  │ │ HLS Mock    │  │  │ MongoDB              │ │
│  │ - Rec API  │  │ │ - Video API │  │  │ - Users              │ │
│  │ - Models   │  │ │ - Progress  │  │  │ - Movies             │ │
│  │ - Embedder │  │ │ - ABR       │  │  │ - Watch History      │ │
│  └────────────┘  │ └─────────────┘  │  │ - Interactions       │ │
│                  │                  │  └──────────────────────┘ │
│  ┌────────────┐  │                  │  ┌──────────────────────┐ │
│  │ PyTorch    │  │                  │  │ Redis Cache          │ │
│  │ - CF Model │  │                  │  │ - Sessions           │ │
│  │ - Embedder │  │                  │  │ - Recommendations    │ │
│  └────────────┘  │                  │  └──────────────────────┘ │
└──────────────────┴──────────────────┴───────────────────────────┘
```

### 2.2 Service Boundaries

#### **Main Backend Service** (Port 8001)
- **Responsibility**: Core business logic, orchestration
- **Tech**: FastAPI, Motor (async MongoDB)
- **APIs**: REST + WebSocket
- **Key Modules**:
  - `auth`: JWT-based authentication
  - `users`: User profile management
  - `movies`: Catalog CRUD
  - `watch_history`: Tracking & progress
  - `groups`: Multi-user sessions
  - `recommendations`: Orchestration layer

#### **ML Recommendation Service** (Embedded / Separate)
- **Responsibility**: AI/ML inference and training
- **Tech**: PyTorch, Sentence-Transformers, Scikit-learn
- **Models**:
  - Collaborative Filtering (Matrix Factorization)
  - Content-Based (Sentence embeddings + cosine similarity)
  - Hybrid Scorer
  - Cold-start handler

#### **Streaming Service** (Mock)
- **Responsibility**: Video delivery simulation
- **Tech**: FastAPI serving static video metadata
- **Features**: Progress tracking, ABR simulation

---

## 3. Data Architecture

### 3.1 MongoDB Collections

#### **users**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "password_hash": "bcrypt_hash",
  "name": "John Doe",
  "preferences": {
    "favorite_genres": ["Action", "Sci-Fi"],
    "mood": "excited",
    "preferred_languages": ["en"]
  },
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

#### **movies**
```json
{
  "id": "movie_uuid",
  "tmdb_id": 12345,
  "title": "Inception",
  "overview": "Dream heist thriller...",
  "genres": ["Action", "Sci-Fi"],
  "release_date": "2010-07-16",
  "rating": 8.8,
  "poster_url": "https://...",
  "backdrop_url": "https://...",
  "runtime": 148,
  "language": "en",
  "embedding": [0.1, 0.2, ...],  // 384-dim vector
  "video_url": "mock_video_1.mp4",
  "popularity": 95.3,
  "created_at": "ISO8601"
}
```

#### **watch_history**
```json
{
  "id": "uuid",
  "user_id": "user_uuid",
  "movie_id": "movie_uuid",
  "progress_seconds": 3600,
  "total_duration": 5400,
  "completed": false,
  "rating": 4.5,
  "watch_count": 1,
  "last_watched_at": "ISO8601",
  "created_at": "ISO8601"
}
```

#### **interactions**
```json
{
  "id": "uuid",
  "user_id": "user_uuid",
  "movie_id": "movie_uuid",
  "action": "like|skip|bookmark|rate",
  "value": 4.5,
  "timestamp": "ISO8601"
}
```

#### **group_sessions**
```json
{
  "id": "session_uuid",
  "host_user_id": "user_uuid",
  "member_ids": ["user1", "user2"],
  "movie_id": "movie_uuid",
  "current_position": 1234,
  "status": "active|paused|ended",
  "created_at": "ISO8601"
}
```

### 3.2 Redis Cache Strategy
- **User sessions**: `session:{user_id}` → JWT metadata
- **Recommendations cache**: `rec:{user_id}` → List of movie IDs (TTL: 1 hour)
- **Movie metadata cache**: `movie:{movie_id}` → Full movie object (TTL: 24 hours)
- **Group state**: `group:{session_id}` → Real-time playback state

---

## 4. ML/AI Pipeline

### 4.1 Recommendation Flow

```
User Request → API Gateway
       ↓
  Get User Profile + History
       ↓
  ┌─────────────────────────────┐
  │  Recommendation Engine      │
  │                             │
  │  1. Collaborative Filtering │
  │     - User-item matrix      │
  │     - SVD/ALS               │
  │                             │
  │  2. Content-Based           │
  │     - Movie embeddings      │
  │     - Cosine similarity     │
  │                             │
  │  3. Hybrid Scorer           │
  │     - Weighted combination  │
  │     - Business rules        │
  │                             │
  │  4. Post-processing         │
  │     - Diversity filter      │
  │     - Freshness boost       │
  └─────────────────────────────┘
       ↓
  Return ranked movie list
```

### 4.2 Model Components

#### **Collaborative Filtering**
- **Algorithm**: Matrix Factorization (SVD)
- **Input**: User-item interaction matrix (watch history + ratings)
- **Output**: Predicted scores for unwatched movies
- **Training**: Offline batch (daily)

#### **Content-Based Filtering**
- **Model**: Sentence-BERT (`all-MiniLM-L6-v2`)
- **Input**: Movie metadata (title + overview + genres)
- **Output**: 384-dimensional embeddings
- **Similarity**: Cosine similarity between user preference vector and movie embeddings

#### **Hybrid Scoring**
```python
final_score = (0.5 * cf_score) + (0.3 * content_score) + (0.2 * popularity_boost)
```

#### **Cold-Start Strategy**
- New users → Content-based recommendations based on popular movies
- After 5+ interactions → Enable collaborative filtering

---

## 5. API Specification

### 5.1 Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Get JWT token
- `GET /api/auth/me` - Get current user

### 5.2 Movies
- `GET /api/movies` - List movies (paginated, filtered)
- `GET /api/movies/{id}` - Get movie details
- `GET /api/movies/search?q={query}` - Search movies

### 5.3 Recommendations
- `GET /api/recommendations/personalized` - Get user recommendations
- `GET /api/recommendations/similar/{movie_id}` - Similar movies
- `GET /api/recommendations/trending` - Trending content

### 5.4 Watch History
- `POST /api/watch/start` - Start watching movie
- `PUT /api/watch/progress` - Update watch progress
- `GET /api/watch/history` - Get user watch history
- `POST /api/watch/rate` - Rate a movie

### 5.5 Groups (Future)
- `POST /api/groups/create` - Create group session
- `POST /api/groups/{id}/join` - Join session
- `WebSocket /ws/group/{id}` - Real-time sync

---

## 6. Deployment Architecture

### 6.1 Current (Development)
```
Docker Container
├── Backend (FastAPI) → 0.0.0.0:8001
├── Frontend (React) → 0.0.0.0:3000
├── MongoDB → localhost:27017
└── Redis (planned) → localhost:6379
```

### 6.2 Production (Kubernetes - Future)
```
Ingress Controller (NGINX)
     ↓
┌─────────────┬─────────────┬──────────────┐
│ Backend Pods│ ML Pods     │ Frontend CDN │
│ (3 replicas)│ (2 replicas)│ (Static)     │
└─────────────┴─────────────┴──────────────┘
     ↓              ↓
┌─────────────┬─────────────┐
│ MongoDB     │ Redis       │
│ (StatefulSet)│ (Cluster)  │
└─────────────┴─────────────┘
```

---

## 7. Security Considerations

- **Authentication**: JWT with RS256 signing
- **Password Storage**: bcrypt hashing
- **API Rate Limiting**: 100 req/min per user
- **CORS**: Configured for production domain
- **Input Validation**: Pydantic models
- **SQL Injection**: N/A (NoSQL with parameterized queries)

---

## 8. Performance Optimization

- **Database Indexing**: user_id, movie_id, timestamps
- **Caching Strategy**: Redis for hot data (recommendations, movie metadata)
- **Async I/O**: FastAPI + Motor for non-blocking operations
- **Pagination**: Limit query results (20 items per page)
- **CDN**: Static assets served from CDN (production)

---

## 9. Monitoring & Observability (Future)

- **Metrics**: Prometheus (request latency, error rates, model inference time)
- **Logging**: Structured JSON logs → ELK stack
- **Tracing**: OpenTelemetry for distributed tracing
- **Alerts**: Grafana dashboards with alerting rules

---

## 10. Development Roadmap

### Phase 1: Core MVP (Current)
✅ System architecture
🔄 FastAPI backend with auth
🔄 MongoDB schemas
🔄 TMDB data ingestion
🔄 Basic recommendation engine
🔄 React frontend
🔄 Mock streaming

### Phase 2: Advanced ML
⏳ Behavior signal collection
⏳ Mood detection (sentiment analysis)
⏳ Explainable recommendations
⏳ Model evaluation metrics

### Phase 3: Social & Groups
⏳ Group watch sessions
⏳ WebSocket real-time sync
⏳ Group preference aggregation

### Phase 4: Production Hardening
⏳ Docker + Kubernetes
⏳ CI/CD pipeline
⏳ Load testing (Locust)
⏳ Security audit
⏳ Monitoring stack

---

## 11. Technology Stack

| Layer | Technology | Version |
|-------|------------|--------|
| Frontend | React | 19.0 |
| UI Library | Radix UI + Tailwind | Latest |
| Backend | FastAPI | 0.110.1 |
| Database | MongoDB | 4.5 |
| Cache | Redis | 7.x (planned) |
| ML Framework | PyTorch | 2.x |
| NLP | Sentence-Transformers | Latest |
| Auth | JWT (python-jose) | Latest |
| Data Source | TMDB API | v3 |

---

## 12. External Dependencies

- **TMDB API**: Movie metadata, posters, ratings
- **MovieLens Dataset**: User interaction data for training
- **HuggingFace Models**: Sentence embeddings

---

**Document Version**: 1.0  
**Last Updated**: Jan 2026  
**Author**: E1 Agent
