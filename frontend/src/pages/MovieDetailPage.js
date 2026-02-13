import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Play, Pause, Star, Clock, Calendar, ArrowLeft, Loader, Heart, X } from 'lucide-react';
import ReactPlayer from 'react-player';
import { moviesAPI, watchAPI, recommendationsAPI, interactionsAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

export const MovieDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [movie, setMovie] = useState(null);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState(false);
  const [showPlayer, setShowPlayer] = useState(false);
  const [userRating, setUserRating] = useState(0);
  const playerRef = useRef(null);

  useEffect(() => {
    fetchMovieDetails();
    fetchSimilarMovies();
  }, [id]);

  const fetchMovieDetails = async () => {
    try {
      const response = await moviesAPI.getMovie(id);
      setMovie(response.data);
    } catch (error) {
      toast.error('Failed to load movie details');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSimilarMovies = async () => {
    try {
      const response = await recommendationsAPI.getSimilar(id, 6);
      setSimilarMovies(response.data.recommendations.map(r => r.movie));
    } catch (error) {
      console.error('Failed to fetch similar movies:', error);
    }
  };

  const handlePlayClick = async () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to watch');
      return;
    }

    try {
      await watchAPI.startWatching(id);
      setShowPlayer(true);
      setPlaying(true);
      toast.success('Starting playback...');
    } catch (error) {
      toast.error('Failed to start watching');
      console.error(error);
    }
  };

  const handleClosePlayer = () => {
    setPlaying(false);
    setShowPlayer(false);
  };

  const handleProgress = (state) => {
    // Update watch progress every 10 seconds
    if (state.playedSeconds % 10 < 1 && state.playedSeconds > 0) {
      try {
        watchAPI.updateProgress({
          movie_id: id,
          progress_seconds: Math.floor(state.playedSeconds),
          total_duration: Math.floor(state.loadedSeconds),
        });
      } catch (error) {
        console.error('Failed to update progress:', error);
      }
    }
  };

  const handleRate = async (rating) => {
    if (!isAuthenticated) {
      toast.error('Please sign in to rate');
      return;
    }

    try {
      await watchAPI.rateMovie({ movie_id: id, rating });
      setUserRating(rating);
      toast.success('Rating saved!');
    } catch (error) {
      toast.error('Failed to save rating');
    }
  };

  const handleLike = async () => {
    if (!isAuthenticated) {
      toast.error('Please sign in');
      return;
    }

    try {
      await interactionsAPI.create({ movie_id: id, action: 'like' });
      toast.success('Added to favorites!');
    } catch (error) {
      toast.error('Failed to like');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <p className="text-text-secondary">Movie not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[80vh] overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <img
            src={movie.backdrop_url || movie.poster_url}
            alt={movie.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-transparent" />
        </div>

        {/* Back Button */}
        <button
          data-testid="back-button"
          onClick={() => navigate(-1)}
          className="absolute top-24 left-6 z-20 flex items-center gap-2 px-4 py-2 rounded-full glass-effect hover:bg-white/20 text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        {/* Content */}
        <div className="absolute bottom-0 left-0 right-0 p-6 md:p-12 z-10">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <h1 className="font-heading text-4xl md:text-6xl font-bold text-white">
                {movie.title}
              </h1>

              <div className="flex flex-wrap items-center gap-4 text-text-secondary">
                <div className="flex items-center gap-1">
                  <Star className="w-5 h-5 text-yellow-400 fill-current" />
                  <span className="text-white font-bold">{movie.rating?.toFixed(1)}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-5 h-5" />
                  <span>{movie.runtime} min</span>
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="w-5 h-5" />
                  <span>{movie.release_date}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {movie.genres?.map((genre) => (
                  <span
                    key={genre}
                    className="px-3 py-1 rounded-full bg-white/10 text-white text-sm"
                  >
                    {genre}
                  </span>
                ))}
              </div>

              <p className="text-lg text-text-secondary max-w-3xl">{movie.overview}</p>

              <div className="flex flex-wrap gap-4 pt-4">
                <button
                  data-testid="play-movie-button"
                  onClick={handlePlayClick}
                  disabled={showPlayer}
                  className="bg-primary hover:bg-primary-hover text-black font-bold py-3 px-8 rounded-full flex items-center gap-2 transition-transform hover:scale-105 shadow-glow disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Play className="w-5 h-5 fill-current" />
                  {showPlayer ? 'Now Playing' : 'Play Now'}
                </button>
                <button
                  data-testid="like-movie-button"
                  onClick={handleLike}
                  className="bg-white/10 hover:bg-white/20 text-white font-bold py-3 px-8 rounded-full flex items-center gap-2 transition-colors backdrop-blur-md"
                >
                  <Heart className="w-5 h-5" />
                  Add to Favorites
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Video Player Modal */}
      {showPlayer && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4"
          data-testid="video-player-modal"
        >
          <div className="w-full max-w-6xl relative">
            {/* Close Button */}
            <button
              onClick={handleClosePlayer}
              className="absolute -top-12 right-0 text-white hover:text-primary transition-colors z-10"
              data-testid="close-player-button"
            >
              <X className="w-8 h-8" />
            </button>

            {/* Player Container */}
            <div className="relative pt-[56.25%] bg-black rounded-lg overflow-hidden shadow-2xl">
              <div className="absolute inset-0">
                <ReactPlayer
                  ref={playerRef}
                  url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                  width="100%"
                  height="100%"
                  controls
                  playing={playing}
                  onPlay={() => setPlaying(true)}
                  onPause={() => setPlaying(false)}
                  onProgress={handleProgress}
                  onEnded={() => {
                    setPlaying(false);
                    toast.success('Movie finished!');
                  }}
                  onError={(e) => {
                    console.error('Player error:', e);
                    toast.error('Error playing video');
                  }}
                  config={{
                    file: {
                      attributes: {
                        controlsList: 'nodownload',
                      },
                    },
                  }}
                />
              </div>
            </div>

            {/* Movie Info Below Player */}
            <div className="mt-6 glass-effect rounded-lg p-6">
              <h2 className="font-heading text-2xl font-bold text-white mb-2">{movie.title}</h2>
              <div className="flex items-center gap-4 text-text-secondary text-sm">
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 text-yellow-400 fill-current" />
                  <span className="text-white font-bold">{movie.rating?.toFixed(1)}</span>
                </div>
                <span>•</span>
                <span>{movie.runtime} min</span>
                <span>•</span>
                <span>{movie.release_date}</span>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Rating Section */}
      {isAuthenticated && (
        <section className="py-12 px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="glass-effect rounded-2xl p-8"
            >
              <h2 className="font-heading text-2xl font-bold text-white mb-4">Rate this movie</h2>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button
                    key={rating}
                    data-testid={`rating-${rating}`}
                    onClick={() => handleRate(rating)}
                    className="group"
                  >
                    <Star
                      className={`w-8 h-8 transition-colors ${
                        rating <= userRating
                          ? 'text-yellow-400 fill-current'
                          : 'text-text-muted group-hover:text-yellow-400'
                      }`}
                    />
                  </button>
                ))}
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {/* Similar Movies */}
      {similarMovies.length > 0 && (
        <section className="py-12 px-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="font-heading text-3xl font-bold text-white mb-8">Similar Movies</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6" data-testid="similar-movies">
              {similarMovies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default MovieDetailPage;
