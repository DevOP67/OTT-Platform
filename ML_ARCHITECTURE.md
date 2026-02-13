# ML/AI Architecture - Movie Recommendation System

---

## 1. Overview

The ML system employs a **hybrid recommendation approach** combining collaborative filtering and content-based methods with behavioral intelligence.

---

## 2. Model Architecture

### 2.1 Collaborative Filtering (CF)

**Algorithm**: Singular Value Decomposition (SVD)

**Input Data**:
- User-item interaction matrix (users × movies)
- Implicit signals: watch_count, completion_rate
- Explicit signals: ratings (1-5 stars)

**Matrix Structure**:
```
           Movie1  Movie2  Movie3  ...
User1      5.0     0       4.5
User2      0       3.0     0
User3      4.0     0       5.0
```

**Training**:
```python
from sklearn.decomposition import TruncatedSVD

# Factorize into user and movie latent factors
U, Σ, V_T = SVD(interaction_matrix, n_components=50)

# Predict score for user i and movie j
score = U[i] @ Σ @ V_T[:, j]
```

**Advantages**:
- Captures latent user preferences
- Works well with sparse data
- Scales to millions of users

**Limitations**:
- Cold-start problem for new users/movies
- Requires sufficient interaction data

---

### 2.2 Content-Based Filtering

**Model**: Sentence-BERT (`all-MiniLM-L6-v2`)

**Input Features**:
- Title + Overview (text)
- Genres (comma-separated)
- Director, Cast (future)

**Embedding Generation**:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Create movie text
movie_text = f"{title}. {overview}. Genres: {genres}"

# Generate 384-dim embedding
embedding = model.encode(movie_text)
```

**User Profile Vector**:
- Average embeddings of movies user liked/watched
- Weighted by rating and recency

**Similarity Scoring**:
```python
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity([user_vector], [movie_embedding])[0][0]
```

**Advantages**:
- No cold-start for new users (based on preferences)
- Interpretable (semantic similarity)
- Works with limited interaction data

---

### 2.3 Hybrid Recommendation Engine

**Scoring Formula**:
```python
def hybrid_score(user_id, movie_id):
    cf_score = collaborative_filtering_score(user_id, movie_id)
    cb_score = content_based_score(user_id, movie_id)
    popularity = movie.popularity / 100  # Normalize
    recency = time_decay_factor(movie.release_date)
    
    final_score = (
        0.4 * cf_score +
        0.3 * cb_score +
        0.2 * popularity +
        0.1 * recency
    )
    
    return final_score
```

**Weights Explanation**:
- **40% CF**: Primary signal for personalized recommendations
- **30% Content**: Semantic relevance and genre matching
- **20% Popularity**: Ensures quality baseline
- **10% Recency**: Promotes new content

---

## 3. Cold-Start Strategy

### 3.1 New User
**Problem**: No watch history → CF fails

**Solution**:
1. Show trending/popular movies
2. Ask for genre preferences during onboarding
3. Use content-based recommendations immediately
4. Switch to hybrid after 5+ interactions

### 3.2 New Movie
**Problem**: No user interactions → CF fails

**Solution**:
1. Use content-based similarity to existing movies
2. Boost visibility via "New Releases" section
3. Accumulate interactions for CF inclusion

---

## 4. Behavioral Intelligence (Phase 2)

### 4.1 Watch Pattern Analysis
**Signals**:
- Watch time distribution (morning vs. night)
- Completion rates by genre
- Binge-watching behavior
- Skip patterns

**Use Case**: Recommend light comedies in the evening, intense thrillers on weekends

### 4.2 Mood Detection
**Approach**: Sentiment analysis on user interactions
- Explicit: User-selected mood tags
- Implicit: Watch speed, pause frequency, rewatch patterns

**Implementation** (Future):
```python
from transformers import pipeline

sentiment_model = pipeline('sentiment-analysis')

# Analyze recent watch history
recent_genres = get_recent_watched_genres(user_id)
mood = infer_mood_from_genres(recent_genres)

# Filter recommendations
if mood == 'stressed':
    recommend(genres=['Comedy', 'Animation'])
```

---

## 5. Group Recommendations (Phase 3)

### 5.1 Preference Aggregation
**Challenge**: Multiple users with different tastes

**Approach**: Consensus-based scoring
```python
def group_recommendation(user_ids):
    user_vectors = [get_user_embedding(uid) for uid in user_ids]
    
    # Centroid of user preferences
    group_vector = np.mean(user_vectors, axis=0)
    
    # Find movies close to centroid
    scores = cosine_similarity([group_vector], all_movie_embeddings)
    
    # Ensure no one hates it (filter movies rated <2 by anyone)
    filtered = filter_group_dislikes(scores, user_ids)
    
    return top_k(filtered, k=20)
```

---

## 6. Explainability (Phase 2)

### 6.1 Recommendation Reasons
For each recommendation, provide:
- "Recommended because you watched {Movie X}"
- "Fans of {Genre} also loved this"
- "Trending in your region"

### 6.2 Feature Attribution
Use SHAP values to explain model decisions:
```python
import shap

explainer = shap.Explainer(model)
shap_values = explainer(user_features)

# Show top contributing features
print(f"Top reason: {feature_names[shap_values.argmax()]}")
```

---

## 7. Model Training Pipeline

### 7.1 Data Collection
```
TMDB API → MongoDB (movies)
User Interactions → MongoDB (watch_history, ratings)
```

### 7.2 Feature Engineering
```python
# Generate interaction matrix
interaction_matrix = create_user_item_matrix(
    watch_history,
    weight_by='completion_rate'
)

# Generate movie embeddings
for movie in movies:
    movie.embedding = embed_movie(movie)
```

### 7.3 Training Schedule
- **CF Model**: Daily batch training (off-peak hours)
- **Embeddings**: One-time generation + incremental for new movies
- **Hybrid Weights**: Weekly A/B testing to optimize

### 7.4 Evaluation Metrics
- **Precision@K**: Proportion of recommended movies watched
- **Recall@K**: Coverage of user's actual watches
- **NDCG**: Ranking quality
- **Diversity**: Genre spread in recommendations
- **Novelty**: Percentage of non-obvious recommendations

---

## 8. Model Storage & Versioning

```
/app/ml_models/
├── cf_model_v1.pkl              # Collaborative filtering
├── movie_embeddings_v1.npy      # Content-based vectors
├── user_profiles_v1.npy         # User preference vectors
└── model_metadata.json          # Version, metrics, timestamp
```

---

## 9. Inference Optimization

### 9.1 Pre-computation
- **User embeddings**: Updated after each interaction
- **Recommendations**: Pre-cached for active users (Redis)
- **Similarity matrices**: Pre-computed for popular movies

### 9.2 Latency Targets
- Cold recommendations: < 200ms
- Personalized recommendations: < 500ms
- Real-time updates: < 100ms

---

## 10. Future Enhancements

### 10.1 Deep Learning Models
- **Neural Collaborative Filtering**: Replace SVD with neural nets
- **Sequence Models**: LSTM/Transformer for watch history
- **Multi-modal**: Image embeddings from posters

### 10.2 Advanced Features
- **Contextual Bandits**: Online learning from user feedback
- **Causal Inference**: Measure recommendation impact
- **Federated Learning**: Privacy-preserving training

---

**Version**: 1.0  
**Last Updated**: Jan 2026
