import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Clock, TrendingUp, Zap, Loader, Sparkles } from 'lucide-react';
import { behaviorAPI, recommendationsAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';

// Mood options with emoji and colors
const MOOD_OPTIONS = [
  { id: 'happy', emoji: '😊', label: 'Happy', color: 'bg-yellow-500', description: 'Uplifting & feel-good movies' },
  { id: 'sad', emoji: '😢', label: 'Sad', color: 'bg-blue-500', description: 'Emotional & touching stories' },
  { id: 'excited', emoji: '🤩', label: 'Excited', color: 'bg-orange-500', description: 'Action-packed & thrilling' },
  { id: 'relaxed', emoji: '😌', label: 'Relaxed', color: 'bg-green-500', description: 'Calm & easy-watching' },
  { id: 'romantic', emoji: '🥰', label: 'Romantic', color: 'bg-pink-500', description: 'Love stories & romance' },
  { id: 'scared', emoji: '😱', label: 'Scared', color: 'bg-purple-500', description: 'Horror & suspense' },
  { id: 'thoughtful', emoji: '🤔', label: 'Thoughtful', color: 'bg-indigo-500', description: 'Mind-bending & intellectual' },
  { id: 'adventurous', emoji: '🚀', label: 'Adventurous', color: 'bg-teal-500', description: 'Epic adventures & fantasy' },
];

// Mood to genre mapping
const MOOD_GENRES = {
  happy: ['Comedy', 'Family', 'Animation'],
  sad: ['Drama', 'Romance'],
  excited: ['Action', 'Thriller', 'Adventure'],
  relaxed: ['Comedy', 'Drama', 'Family'],
  romantic: ['Romance', 'Drama', 'Comedy'],
  scared: ['Horror', 'Thriller', 'Mystery'],
  thoughtful: ['Science Fiction', 'Mystery', 'Drama'],
  adventurous: ['Adventure', 'Fantasy', 'Action'],
};

export const IntelligentRecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [behaviorProfile, setBehaviorProfile] = useState(null);
  const [selectedMood, setSelectedMood] = useState(null);
  const [detectedMood, setDetectedMood] = useState('neutral');
  const [loading, setLoading] = useState(true);
  const [moodLoading, setMoodLoading] = useState(false);

  useEffect(() => {
    fetchIntelligentRecommendations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchIntelligentRecommendations = async () => {
    try {
      setLoading(true);
      const [recsResponse, profileResponse] = await Promise.all([
        recommendationsAPI.getIntelligent(20).catch(() => recommendationsAPI.getTrending(20)),
        behaviorAPI.getProfile().catch(() => ({ 
          data: { preferred_time: 'any time', completion_rate: 0, binge_watching: false, current_mood: 'neutral' }
        })),
      ]);
      
      setRecommendations(recsResponse.data.recommendations || []);
      setDetectedMood(recsResponse.data.mood || 'neutral');
      setBehaviorProfile(profileResponse.data);
    } catch (error) {
      toast.error('Failed to load recommendations');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleMoodSelect = async (mood) => {
    setSelectedMood(mood.id);
    setMoodLoading(true);
    
    try {
      // Record the mood selection
      await behaviorAPI.recordSignal({
        signal_type: 'mood_selection',
        value: 1,
        metadata: { mood: mood.id }
      }).catch(() => {});

      // Get all recommendations and filter by mood-appropriate genres
      const response = await recommendationsAPI.getTrending(50);
      const allRecs = response.data.recommendations || [];
      
      // Filter based on mood genres
      const moodGenres = MOOD_GENRES[mood.id] || [];
      const filtered = allRecs.filter(rec => {
        const movieGenres = rec.movie.genres || [];
        return movieGenres.some(g => moodGenres.includes(g));
      });

      // If not enough filtered results, include some from all
      const finalRecs = filtered.length >= 10 ? filtered.slice(0, 20) : [...filtered, ...allRecs.filter(r => !filtered.includes(r))].slice(0, 20);
      
      setRecommendations(finalRecs);
      toast.success(`Showing ${mood.label.toLowerCase()} picks! ${mood.emoji}`);
    } catch (error) {
      toast.error('Failed to update recommendations');
    } finally {
      setMoodLoading(false);
    }
  };

  const clearMoodFilter = () => {
    setSelectedMood(null);
    fetchIntelligentRecommendations();
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4 flex items-center gap-3">
            <Brain className="w-10 h-10 text-primary" />
            AI Picks
          </h1>
          <p className="text-xl text-text-secondary">
            Personalized recommendations based on your mood and behavior
          </p>
        </motion.div>

        {/* Mood Picker Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-effect rounded-2xl p-6 mb-8"
        >
          <div className="flex items-center gap-3 mb-4">
            <Sparkles className="w-6 h-6 text-primary" />
            <h2 className="font-heading text-2xl font-bold text-white">How are you feeling?</h2>
            {selectedMood && (
              <button
                onClick={clearMoodFilter}
                className="ml-auto text-sm text-text-secondary hover:text-white transition-colors"
              >
                Clear filter
              </button>
            )}
          </div>
          <p className="text-text-secondary mb-6">Select your mood and we'll find the perfect movies for you</p>
          
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
            {MOOD_OPTIONS.map((mood) => (
              <motion.button
                key={mood.id}
                onClick={() => handleMoodSelect(mood)}
                disabled={moodLoading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`relative p-4 rounded-xl transition-all ${selectedMood === mood.id ? `${mood.color} ring-2 ring-white` : 'bg-white/5 hover:bg-white/10'} ${moodLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <div className="text-center">
                  <span className="text-3xl block mb-2">{mood.emoji}</span>
                  <span className="text-white text-sm font-medium">{mood.label}</span>
                </div>
                {selectedMood === mood.id && (
                  <motion.div
                    layoutId="mood-indicator"
                    className="absolute inset-0 border-2 border-white rounded-xl"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </motion.button>
            ))}
          </div>
          
          {selectedMood && (
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 text-center text-text-secondary"
            >
              {MOOD_OPTIONS.find(m => m.id === selectedMood)?.description}
            </motion.p>
          )}
        </motion.div>

        {/* Behavior Insights */}
        {behaviorProfile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
          >
            <div className="glass-effect rounded-xl p-4">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{selectedMood ? MOOD_OPTIONS.find(m => m.id === selectedMood)?.emoji : '😊'}</span>
                <div>
                  <p className="text-xs text-text-secondary">Current Mood</p>
                  <p className="text-white font-bold capitalize">{selectedMood || detectedMood}</p>
                </div>
              </div>
            </div>
            <div className="glass-effect rounded-xl p-4">
              <Clock className="w-6 h-6 text-primary mb-1" />
              <p className="text-xs text-text-secondary">Preferred Time</p>
              <p className="text-white font-bold capitalize">{behaviorProfile.preferred_time || 'Any time'}</p>
            </div>
            <div className="glass-effect rounded-xl p-4">
              <TrendingUp className="w-6 h-6 text-primary mb-1" />
              <p className="text-xs text-text-secondary">Completion Rate</p>
              <p className="text-white font-bold">{(behaviorProfile.completion_rate * 100).toFixed(0)}%</p>
            </div>
            <div className="glass-effect rounded-xl p-4">
              <Zap className="w-6 h-6 text-primary mb-1" />
              <p className="text-xs text-text-secondary">Watch Style</p>
              <p className="text-white font-bold">{behaviorProfile.binge_watching ? 'Binge Watcher' : 'Casual'}</p>
            </div>
          </motion.div>
        )}

        {/* Loading State for Mood Change */}
        {moodLoading && (
          <div className="flex items-center justify-center py-12">
            <Loader className="w-8 h-8 text-primary animate-spin" />
            <span className="ml-3 text-white">Finding movies for your mood...</span>
          </div>
        )}

        {/* Recommendations */}
        {!moodLoading && recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="font-heading text-2xl font-bold text-white mb-6">
              {selectedMood ? `${MOOD_OPTIONS.find(m => m.id === selectedMood)?.emoji} ${MOOD_OPTIONS.find(m => m.id === selectedMood)?.label} Picks` : 'Recommended For You'}
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
              {recommendations.map((rec, index) => (
                <motion.div
                  key={rec.movie.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.03 }}
                  className="relative"
                >
                  <MovieCard movie={rec.movie} />
                  <div className="mt-2 text-xs text-text-secondary line-clamp-2">{rec.reason}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {!moodLoading && recommendations.length === 0 && (
          <div className="glass-effect rounded-2xl p-12 text-center">
            <p className="text-text-secondary">Watch more movies to get intelligent recommendations</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default IntelligentRecommendationsPage;
