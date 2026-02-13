import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Clock, TrendingUp, Zap, Loader } from 'lucide-react';
import { behaviorAPI, recommendationsAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';

export const IntelligentRecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [behaviorProfile, setBehaviorProfile] = useState(null);
  const [mood, setMood] = useState('neutral');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntelligentRecommendations();
  }, []);

  const fetchIntelligentRecommendations = async () => {
    try {
      setLoading(true);
      const [recsResponse, profileResponse] = await Promise.all([
        recommendationsAPI.getIntelligent(20),
        behaviorAPI.getProfile(),
      ]);
      
      setRecommendations(recsResponse.data.recommendations);
      setMood(recsResponse.data.mood);
      setBehaviorProfile(profileResponse.data);
    } catch (error) {
      toast.error('Failed to load intelligent recommendations');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const moodEmojis = {
    relaxed: '😌',
    excited: '🤩',
    thoughtful: '🤔',
    neutral: '😊',
    distracted: '😵',
    disappointed: '😔',
  };

  const moodColors = {
    relaxed: 'text-green-400',
    excited: 'text-yellow-400',
    thoughtful: 'text-blue-400',
    neutral: 'text-gray-400',
    distracted: 'text-orange-400',
    disappointed: 'text-red-400',
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
          className="mb-12"
        >
          <h1 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4 flex items-center gap-3">
            <Brain className="w-10 h-10 text-primary" />
            Intelligent Recommendations
          </h1>
          <p className="text-xl text-text-secondary">
            AI-powered suggestions based on your behavior and mood
          </p>
        </motion.div>

        {/* Behavior Insights */}
        {behaviorProfile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12"
          >
            <div className="glass-effect rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-4xl">{moodEmojis[mood] || '😊'}</span>
                <div>
                  <p className="text-sm text-text-secondary">Current Mood</p>
                  <p className={`text-xl font-bold capitalize ${moodColors[mood] || 'text-white'}`}>
                    {mood}
                  </p>
                </div>
              </div>
            </div>

            <div className="glass-effect rounded-2xl p-6">
              <Clock className="w-8 h-8 text-primary mb-2" />
              <p className="text-sm text-text-secondary">Preferred Time</p>
              <p className="text-xl font-bold text-white capitalize">
                {behaviorProfile.preferred_time || 'Any time'}
              </p>
            </div>

            <div className="glass-effect rounded-2xl p-6">
              <TrendingUp className="w-8 h-8 text-primary mb-2" />
              <p className="text-sm text-text-secondary">Completion Rate</p>
              <p className="text-xl font-bold text-white">
                {(behaviorProfile.completion_rate * 100).toFixed(0)}%
              </p>
            </div>

            <div className="glass-effect rounded-2xl p-6">
              <Zap className="w-8 h-8 text-primary mb-2" />
              <p className="text-sm text-text-secondary">Watch Style</p>
              <p className="text-xl font-bold text-white">
                {behaviorProfile.binge_watching ? 'Binge Watcher' : 'Casual Viewer'}
              </p>
            </div>
          </motion.div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="font-heading text-2xl font-bold text-white mb-6">
              Recommended Based on Your Behavior
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6" data-testid="intelligent-recs-grid">
              {recommendations.map((rec, index) => (
                <motion.div
                  key={rec.movie.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="relative"
                >
                  <MovieCard movie={rec.movie} />
                  <div className="mt-2 text-xs text-text-secondary">
                    {rec.reason}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        ) : (
          <div className="glass-effect rounded-2xl p-12 text-center">
            <p className="text-text-secondary">
              Watch more movies to get intelligent recommendations
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default IntelligentRecommendationsPage;
