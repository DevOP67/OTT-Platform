import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, TrendingUp, Loader, RefreshCw } from 'lucide-react';
import { recommendationsAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';

export const RecommendationsPage = () => {
  const [personalizedRecs, setPersonalizedRecs] = useState([]);
  const [trendingRecs, setTrendingRecs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const [personalized, trending] = await Promise.all([
        recommendationsAPI.getPersonalized(12),
        recommendationsAPI.getTrending(12),
      ]);
      setPersonalizedRecs(personalized.data.recommendations);
      setTrendingRecs(trending.data.recommendations);
    } catch (error) {
      toast.error('Failed to load recommendations');
      console.error(error);
    } finally {
      setLoading(false);
    }
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
          className="mb-12 flex items-center justify-between"
        >
          <div>
            <h1 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4 flex items-center gap-3">
              <Sparkles className="w-10 h-10 text-primary" />
              For You
            </h1>
            <p className="text-xl text-text-secondary">
              AI-powered recommendations tailored to your taste
            </p>
          </div>
          <button
            data-testid="refresh-recommendations"
            onClick={fetchRecommendations}
            className="bg-white/10 hover:bg-white/20 text-white p-3 rounded-full transition-colors"
            title="Refresh recommendations"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </motion.div>

        {/* Personalized Recommendations */}
        <section className="mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-1 h-8 bg-primary rounded-full" />
              <h2 className="font-heading text-2xl font-bold text-white">Recommended for You</h2>
            </div>

            {personalizedRecs.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6" data-testid="personalized-grid">
                {personalizedRecs.map((rec, index) => (
                  <motion.div
                    key={rec.movie.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="relative"
                  >
                    <MovieCard movie={rec.movie} />
                    {rec.score > 0.8 && (
                      <div className="absolute -top-2 -right-2 bg-primary text-black text-xs font-bold px-2 py-1 rounded-full shadow-glow z-10">
                        {Math.round(rec.score * 100)}% Match
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="glass-effect rounded-2xl p-12 text-center">
                <p className="text-text-secondary">
                  Watch a few movies to get personalized recommendations
                </p>
              </div>
            )}
          </motion.div>
        </section>

        {/* Trending */}
        <section>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-6 h-6 text-secondary" />
              <h2 className="font-heading text-2xl font-bold text-white">Trending Now</h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6" data-testid="trending-grid">
              {trendingRecs.map((rec, index) => (
                <motion.div
                  key={rec.movie.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <MovieCard movie={rec.movie} />
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>
      </div>
    </div>
  );
};

export default RecommendationsPage;
