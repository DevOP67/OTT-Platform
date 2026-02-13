import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Users, Plus, Play, Loader } from 'lucide-react';
import { groupAPI, moviesAPI } from '../api';
import { toast } from 'sonner';

export const GroupSessionsPage = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState('');
  const [sessionName, setSessionName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchSessions();
    fetchMovies();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await groupAPI.getUserSessions();
      setSessions(response.data.sessions);
    } catch (error) {
      toast.error('Failed to load sessions');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMovies = async () => {
    try {
      const response = await moviesAPI.getMovies({ limit: 20 });
      setMovies(response.data.movies);
    } catch (error) {
      console.error('Failed to load movies:', error);
    }
  };

  const handleCreateSession = async () => {
    if (!selectedMovie) {
      toast.error('Please select a movie');
      return;
    }

    try {
      setCreating(true);
      const response = await groupAPI.createSession({
        movie_id: selectedMovie,
        name: sessionName || undefined,
      });
      
      toast.success('Watch party created!');
      navigate(`/group/${response.data.id}`);
    } catch (error) {
      toast.error('Failed to create session');
      console.error(error);
    } finally {
      setCreating(false);
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
              <Users className="w-10 h-10 text-primary" />
              Group Watch Parties
            </h1>
            <p className="text-xl text-text-secondary">
              Watch movies together in real-time with friends
            </p>
          </div>
          <button
            data-testid="create-session-button"
            onClick={() => setShowCreateModal(true)}
            className="bg-primary hover:bg-primary-hover text-black font-bold py-3 px-6 rounded-full flex items-center gap-2 transition-transform hover:scale-105"
          >
            <Plus className="w-5 h-5" />
            Create Party
          </button>
        </motion.div>

        {/* Active Sessions */}
        {sessions.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="font-heading text-2xl font-bold text-white mb-6">Your Active Parties</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="sessions-grid">
              {sessions.map((session) => (
                <motion.div
                  key={session.id}
                  whileHover={{ y: -4 }}
                  className="glass-effect rounded-2xl overflow-hidden cursor-pointer"
                  onClick={() => navigate(`/group/${session.id}`)}
                >
                  {session.movie && (
                    <img
                      src={session.movie.backdrop_url || session.movie.poster_url}
                      alt={session.movie.title}
                      className="w-full h-48 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="font-heading text-xl font-bold text-white mb-2">
                      {session.name}
                    </h3>
                    <p className="text-text-secondary mb-4">
                      {session.movie?.title}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-text-secondary">
                        <Users className="w-4 h-4" />
                        <span>{session.member_count} members</span>
                      </div>
                      <button
                        className="bg-primary hover:bg-primary-hover text-black font-bold py-2 px-4 rounded-full flex items-center gap-2 transition-transform hover:scale-105"
                      >
                        <Play className="w-4 h-4 fill-current" />
                        Join
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        ) : (
          <div className="glass-effect rounded-2xl p-12 text-center">
            <Users className="w-16 h-16 text-text-muted mx-auto mb-4" />
            <p className="text-text-secondary mb-6">
              No active watch parties. Create one to watch with friends!
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-primary hover:bg-primary-hover text-black font-bold py-3 px-6 rounded-full transition-transform hover:scale-105"
            >
              Create Your First Party
            </button>
          </div>
        )}

        {/* Create Modal */}
        {showCreateModal && (
          <div
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowCreateModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="glass-heavy rounded-2xl p-8 max-w-md w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="font-heading text-3xl font-bold text-white mb-6">
                Create Watch Party
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">
                    Party Name (Optional)
                  </label>
                  <input
                    type="text"
                    value={sessionName}
                    onChange={(e) => setSessionName(e.target.value)}
                    placeholder="Movie Night with Friends"
                    className="w-full bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-3"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">
                    Select Movie
                  </label>
                  <select
                    value={selectedMovie}
                    onChange={(e) => setSelectedMovie(e.target.value)}
                    className="w-full bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-3"
                  >
                    <option value="">Choose a movie...</option>
                    {movies.map((movie) => (
                      <option key={movie.id} value={movie.id}>
                        {movie.title}
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  onClick={handleCreateSession}
                  disabled={creating || !selectedMovie}
                  className="w-full bg-primary hover:bg-primary-hover text-black font-bold py-3 px-6 rounded-full transition-transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {creating ? 'Creating...' : 'Create Party'}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GroupSessionsPage;
