import numpy as np
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BehaviorAnalyzer:
    """Analyzes user behavior patterns for intelligent recommendations"""
    
    def __init__(self):
        self.mood_genre_mapping = {
            'relaxed': ['Comedy', 'Animation', 'Family', 'Romance'],
            'excited': ['Action', 'Adventure', 'Thriller'],
            'thoughtful': ['Drama', 'Documentary', 'Mystery'],
            'scared': ['Horror', 'Thriller'],
            'inspired': ['Biography', 'Documentary', 'History']
        }
    
    def analyze_watch_patterns(self, watch_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user's watch patterns"""
        if not watch_history:
            return {
                'preferred_time': None,
                'avg_session_duration': 0,
                'completion_rate': 0,
                'binge_watching': False,
                'preferred_genres': []
            }
        
        # Time of day analysis
        watch_times = []
        for history in watch_history:
            if history.get('last_watched_at'):
                try:
                    dt = datetime.fromisoformat(history['last_watched_at'])
                    watch_times.append(dt.hour)
                except:
                    pass
        
        preferred_time = self._get_preferred_time_slot(watch_times) if watch_times else None
        
        # Session duration analysis
        completed = [h for h in watch_history if h.get('completed')]
        completion_rate = len(completed) / len(watch_history) if watch_history else 0
        
        # Binge watching detection (3+ movies in 24 hours)
        recent_watches = self._count_recent_watches(watch_history, hours=24)
        binge_watching = recent_watches >= 3
        
        return {
            'preferred_time': preferred_time,
            'avg_session_duration': self._calculate_avg_duration(watch_history),
            'completion_rate': completion_rate,
            'binge_watching': binge_watching,
            'preferred_genres': self._extract_preferred_genres(watch_history)
        }
    
    def _get_preferred_time_slot(self, hours: List[int]) -> str:
        """Determine user's preferred watching time"""
        if not hours:
            return None
        
        avg_hour = sum(hours) / len(hours)
        
        if 6 <= avg_hour < 12:
            return 'morning'
        elif 12 <= avg_hour < 18:
            return 'afternoon'
        elif 18 <= avg_hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _calculate_avg_duration(self, watch_history: List[Dict[str, Any]]) -> int:
        """Calculate average watch session duration in minutes"""
        durations = []
        for h in watch_history:
            if h.get('progress_seconds') and h.get('total_duration'):
                durations.append(h['progress_seconds'] / 60)
        
        return int(sum(durations) / len(durations)) if durations else 0
    
    def _count_recent_watches(self, watch_history: List[Dict[str, Any]], hours: int = 24) -> int:
        """Count watches in the last N hours"""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=hours)
        
        count = 0
        for h in watch_history:
            if h.get('last_watched_at'):
                try:
                    dt = datetime.fromisoformat(h['last_watched_at'])
                    if dt.replace(tzinfo=timezone.utc) > cutoff:
                        count += 1
                except:
                    pass
        
        return count
    
    def _extract_preferred_genres(self, watch_history: List[Dict[str, Any]]) -> List[str]:
        """Extract user's preferred genres from watch history"""
        genre_count = {}
        
        for h in watch_history:
            # This would need movie data joined - simplified for now
            pass
        
        return []
    
    def detect_mood(self, watch_history: List[Dict[str, Any]], recent_interactions: List[Dict[str, Any]]) -> str:
        """Detect user's current mood based on recent activity"""
        if not watch_history and not recent_interactions:
            return 'neutral'
        
        # Analyze recent watch patterns (last 3 movies)
        recent_watches = sorted(watch_history, key=lambda x: x.get('last_watched_at', ''), reverse=True)[:3]
        
        # Check completion rates - low completion might indicate restlessness
        if recent_watches:
            recent_completion = sum(1 for w in recent_watches if w.get('completed')) / len(recent_watches)
            if recent_completion < 0.3:
                return 'distracted'
        
        # Check watch time - late night watching might indicate different mood
        now = datetime.now(timezone.utc)
        if 22 <= now.hour or now.hour < 6:
            return 'relaxed'
        
        # Check recent ratings - high ratings indicate satisfaction
        recent_ratings = [h.get('rating', 0) for h in recent_watches if h.get('rating')]
        if recent_ratings:
            avg_rating = sum(recent_ratings) / len(recent_ratings)
            if avg_rating >= 4.5:
                return 'excited'
            elif avg_rating <= 2.5:
                return 'disappointed'
        
        return 'neutral'
    
    def get_mood_based_genres(self, mood: str) -> List[str]:
        """Get genre recommendations based on mood"""
        return self.mood_genre_mapping.get(mood, [])
    
    def enhance_recommendations_with_behavior(
        self,
        recommendations: List[Dict[str, Any]],
        behavior_patterns: Dict[str, Any],
        mood: str
    ) -> List[Dict[str, Any]]:
        """Enhance recommendation scores based on behavioral patterns"""
        mood_genres = self.get_mood_based_genres(mood)
        
        for rec in recommendations:
            movie = rec.get('movie', {})
            original_score = rec.get('score', 0)
            
            # Boost based on mood-genre match
            mood_boost = 0
            if mood_genres:
                movie_genres = movie.get('genres', [])
                matching_genres = set(mood_genres) & set(movie_genres)
                mood_boost = len(matching_genres) * 0.1
            
            # Boost based on preferred time
            time_boost = 0
            preferred_time = behavior_patterns.get('preferred_time')
            if preferred_time == 'evening' and any(g in ['Drama', 'Thriller'] for g in movie.get('genres', [])):
                time_boost = 0.05
            elif preferred_time == 'night' and any(g in ['Horror', 'Action'] for g in movie.get('genres', [])):
                time_boost = 0.05
            
            # Boost for binge-watchers (recommend series-like content)
            binge_boost = 0
            if behavior_patterns.get('binge_watching'):
                binge_boost = 0.05
            
            # Calculate final score
            rec['score'] = min(1.0, original_score + mood_boost + time_boost + binge_boost)
            rec['behavior_factors'] = {
                'mood': mood,
                'mood_boost': mood_boost,
                'time_boost': time_boost,
                'binge_boost': binge_boost
            }
        
        # Re-sort by enhanced scores
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations

# Global instance
behavior_analyzer = BehaviorAnalyzer()
