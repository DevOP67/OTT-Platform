import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
import logging
import pickle
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.model_dir = Path("/app/ml_models")
        self.model_dir.mkdir(exist_ok=True)
        # No ML model loading - use pre-computed embeddings from database
        
    def generate_movie_embedding(self, movie: Dict[str, Any]) -> List[float]:
        """Generate simple embedding based on genres and metadata"""
        # Simple hash-based embedding for deployment without ML models
        genres = movie.get("genres", [])
        rating = movie.get("rating", 5.0)
        popularity = movie.get("popularity", 50.0)
        
        # Create a simple 50-dimensional embedding
        embedding = [0.0] * 50
        
        # Genre-based features (first 20 dimensions)
        genre_map = {
            "Action": 0, "Adventure": 1, "Animation": 2, "Comedy": 3,
            "Crime": 4, "Documentary": 5, "Drama": 6, "Family": 7,
            "Fantasy": 8, "History": 9, "Horror": 10, "Music": 11,
            "Mystery": 12, "Romance": 13, "Science Fiction": 14, "Thriller": 15,
            "War": 16, "Western": 17, "Sci-Fi": 14
        }
        
        for genre in genres:
            if genre in genre_map:
                embedding[genre_map[genre]] = 1.0
        
        # Rating features (dimensions 20-30)
        embedding[20] = rating / 10.0
        embedding[21] = 1.0 if rating >= 8.0 else 0.0
        
        # Popularity features (dimensions 30-40)
        embedding[30] = min(popularity / 100.0, 1.0)
        
        return embedding
    
    def generate_user_profile_vector(self, watch_history: List[Dict[str, Any]], movies: Dict[str, Any]) -> np.ndarray:
        """Generate user preference vector from watch history"""
        if not watch_history:
            return None
        
        embeddings = []
        weights = []
        
        for history in watch_history:
            movie_id = history.get("movie_id")
            movie = movies.get(movie_id)
            if movie and movie.get("embedding"):
                embedding = np.array(movie["embedding"])
                embeddings.append(embedding)
                
                # Weight by rating and completion
                rating_weight = history.get("rating", 3.0) / 5.0
                completion_weight = 1.0 if history.get("completed") else 0.5
                weights.append(rating_weight * completion_weight)
        
        if not embeddings:
            return None
        
        # Weighted average of embeddings
        embeddings = np.array(embeddings)
        weights = np.array(weights).reshape(-1, 1)
        user_vector = np.average(embeddings, axis=0, weights=weights.flatten())
        
        return user_vector
    
    def content_based_recommendations(
        self,
        user_vector: np.ndarray,
        candidate_movies: List[Dict[str, Any]],
        top_k: int = 20
    ) -> List[Tuple[str, float]]:
        """Get content-based recommendations using cosine similarity"""
        if user_vector is None:
            return []
        
        scores = []
        for movie in candidate_movies:
            if movie.get("embedding"):
                movie_embedding = np.array(movie["embedding"])
                similarity = cosine_similarity([user_vector], [movie_embedding])[0][0]
                scores.append((movie["id"], float(similarity)))
        
        # Sort by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def collaborative_filtering_recommendations(
        self,
        user_id: str,
        interaction_matrix: np.ndarray,
        user_map: Dict[str, int],
        movie_map: Dict[int, str],
        top_k: int = 20
    ) -> List[Tuple[str, float]]:
        """Collaborative filtering using simple user-based approach"""
        # This is a simplified version - in production, use matrix factorization
        if user_id not in user_map:
            return []
        
        user_idx = user_map[user_id]
        user_ratings = interaction_matrix[user_idx]
        
        # Find similar users
        similarities = cosine_similarity([user_ratings], interaction_matrix)[0]
        similar_users = np.argsort(similarities)[::-1][1:11]  # Top 10 similar users
        
        # Aggregate recommendations from similar users
        recommended_scores = np.zeros(interaction_matrix.shape[1])
        for similar_user_idx in similar_users:
            recommended_scores += interaction_matrix[similar_user_idx] * similarities[similar_user_idx]
        
        # Filter out already watched movies
        watched_mask = user_ratings > 0
        recommended_scores[watched_mask] = -np.inf
        
        # Get top recommendations
        top_indices = np.argsort(recommended_scores)[::-1][:top_k]
        
        recommendations = []
        for idx in top_indices:
            if recommended_scores[idx] > 0:
                movie_id = movie_map.get(idx)
                if movie_id:
                    recommendations.append((movie_id, float(recommended_scores[idx])))
        
        return recommendations
    
    def hybrid_recommendations(
        self,
        user_id: str,
        user_vector: np.ndarray,
        candidate_movies: List[Dict[str, Any]],
        watch_history: List[Dict[str, Any]],
        top_k: int = 20,
        cf_weight: float = 0.4,
        content_weight: float = 0.3,
        popularity_weight: float = 0.2,
        recency_weight: float = 0.1
    ) -> List[Dict[str, Any]]:
        """Hybrid recommendation combining multiple signals"""
        
        # Content-based scores
        content_scores = {}
        if user_vector is not None:
            content_recs = self.content_based_recommendations(user_vector, candidate_movies, top_k=100)
            content_scores = {movie_id: score for movie_id, score in content_recs}
        
        # Calculate hybrid scores
        scored_movies = []
        for movie in candidate_movies:
            movie_id = movie["id"]
            
            # Skip if already watched
            if any(h.get("movie_id") == movie_id for h in watch_history):
                continue
            
            # Content score
            content_score = content_scores.get(movie_id, 0.0)
            
            # Popularity score (normalized)
            popularity_score = min(movie.get("popularity", 0) / 100.0, 1.0)
            
            # Recency score (newer movies get slight boost)
            try:
                release_year = int(movie.get("release_date", "2000")[:4])
                recency_score = max((release_year - 1990) / 35.0, 0.0)  # Normalize to 0-1
            except:
                recency_score = 0.5
            
            # Combined score (no CF for now - needs more data)
            final_score = (
                content_weight * content_score +
                popularity_weight * popularity_score +
                recency_weight * recency_score
            )
            
            scored_movies.append({
                "movie": movie,
                "score": final_score,
                "reason": self._generate_reason(movie, content_score, popularity_score)
            })
        
        # Sort by score and return top k
        scored_movies.sort(key=lambda x: x["score"], reverse=True)
        return scored_movies[:top_k]
    
    def _generate_reason(self, movie: Dict[str, Any], content_score: float, popularity_score: float) -> str:
        """Generate explanation for recommendation"""
        if content_score > 0.7:
            return f"Matches your interest in {', '.join(movie.get('genres', [])[:2])}"
        elif popularity_score > 0.8:
            return "Highly rated and popular"
        else:
            return "Recommended for you"
    
    def get_similar_movies(
        self,
        movie_id: str,
        all_movies: List[Dict[str, Any]],
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Find similar movies based on embeddings"""
        target_movie = next((m for m in all_movies if m["id"] == movie_id), None)
        if not target_movie or not target_movie.get("embedding"):
            return []
        
        target_embedding = np.array(target_movie["embedding"])
        
        scores = []
        for movie in all_movies:
            if movie["id"] != movie_id and movie.get("embedding"):
                movie_embedding = np.array(movie["embedding"])
                similarity = cosine_similarity([target_embedding], [movie_embedding])[0][0]
                scores.append((movie["id"], float(similarity)))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# Global instance
recommendation_engine = RecommendationEngine()
