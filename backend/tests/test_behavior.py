import pytest
from behavior_service import behavior_analyzer
from datetime import datetime, timezone

def test_analyze_watch_patterns_empty():
    patterns = behavior_analyzer.analyze_watch_patterns([])
    assert patterns['preferred_time'] is None
    assert patterns['completion_rate'] == 0
    assert patterns['binge_watching'] is False

def test_detect_mood_neutral():
    mood = behavior_analyzer.detect_mood([], [])
    assert mood == 'neutral'

def test_get_mood_based_genres():
    genres = behavior_analyzer.get_mood_based_genres('relaxed')
    assert 'Comedy' in genres
    assert 'Animation' in genres

def test_enhance_recommendations():
    recommendations = [
        {
            'movie': {'id': '1', 'title': 'Test Movie', 'genres': ['Comedy']},
            'score': 0.5,
            'reason': 'Test'
        }
    ]
    patterns = {'preferred_time': 'evening', 'binge_watching': False}
    
    enhanced = behavior_analyzer.enhance_recommendations_with_behavior(
        recommendations, patterns, 'relaxed'
    )
    
    assert len(enhanced) == 1
    assert enhanced[0]['score'] >= 0.5  # Should be boosted
