import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Clock, Star, Film, Loader } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { watchAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';

export const ProfilePage = () => {
  const { user } = useAuth();
  const [watchHistory, setWatchHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalWatched: 0,
    totalMinutes: 0,
    averageRating: 0,
  });

  useEffect(() => {
    fetchWatchHistory();
  }, []);

  const fetchWatchHistory = async () => {
    try {
      const response = await watchAPI.getHistory(50);
      const history = response.data.history;
      setWatchHistory(history);

      // Calculate stats
      const completed = history.filter((h) => h.completed);
      const totalMinutes = completed.reduce((sum, h) => sum + (h.total_duration / 60), 0);
      const ratings = history.filter((h) => h.rating).map((h) => h.rating);
      const avgRating = ratings.length > 0 ? ratings.reduce((a, b) => a + b, 0) / ratings.length : 0;

      setStats({
        totalWatched: completed.length,
        totalMinutes: Math.round(totalMinutes),
        averageRating: avgRating,
      });
    } catch (error) {
      toast.error('Failed to load watch history');
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
        {/* Profile Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-effect rounded-2xl p-8 mb-8"
        >
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 bg-gradient-to-br from-primary to-primary-hover rounded-full flex items-center justify-center">
              <User className="w-10 h-10 text-black" />
            </div>
            <div>
              <h1 className="font-heading text-3xl font-bold text-white mb-2">{user?.name}</h1>
              <p className="text-text-secondary">{user?.email}</p>
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
        >
          <div className="glass-effect rounded-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Film className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-3xl font-bold text-white">{stats.totalWatched}</p>
                <p className="text-text-secondary">Movies Watched</p>
              </div>
            </div>
          </div>

          <div className="glass-effect rounded-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-3xl font-bold text-white">{stats.totalMinutes}</p>
                <p className="text-text-secondary">Minutes Watched</p>
              </div>
            </div>
          </div>

          <div className="glass-effect rounded-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Star className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-3xl font-bold text-white">{stats.averageRating.toFixed(1)}</p>
                <p className="text-text-secondary">Average Rating</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Watch History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="font-heading text-3xl font-bold text-white mb-6">Watch History</h2>

          {watchHistory.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6" data-testid="watch-history-grid">
              {watchHistory.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="relative"
                >
                  {item.movie && <MovieCard movie={item.movie} />}
                  {item.completed && (
                    <div className="absolute top-2 left-2 bg-primary text-black text-xs font-bold px-2 py-1 rounded-full">
                      Completed
                    </div>
                  )}
                  {item.rating && (
                    <div className="absolute bottom-2 left-2 right-2 bg-black/80 backdrop-blur-sm p-2 rounded-lg flex items-center justify-center gap-1">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-white font-bold">{item.rating.toFixed(1)}</span>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="glass-effect rounded-2xl p-12 text-center">
              <p className="text-text-secondary">No watch history yet. Start watching movies!</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default ProfilePage;
