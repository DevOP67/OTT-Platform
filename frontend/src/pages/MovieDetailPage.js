import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Star, Clock, Calendar, ArrowLeft, Loader, Heart, X, Film } from 'lucide-react';
import { moviesAPI, watchAPI, recommendationsAPI, interactionsAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

// Demo movie URL
const DEMO_MOVIE_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";

// Extract YouTube video ID
const getYouTubeVideoId = (url) => {
  if (!url) return null;
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s]+)/);
  return match ? match[1] : null;
};

export const MovieDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [movie, setMovie] = useState(null);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showPlayer, setShowPlayer] = useState(false);
  const [playerType, setPlayerType] = useState(null);
  const [userRating, setUserRating] = useState(0);
  const [trailerUrl, setTrailerUrl] = useState(null);
  const [videoLoading, setVideoLoading] = useState(true);

  useEffect(() => {
    fetchMovieDetails();
    fetchSimilarMovies();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchMovieDetails = async () => {
    try {
      const response = await moviesAPI.getMovie(id);
      setMovie(response.data);
      if (response.data.trailer_url) {
        setTrailerUrl(response.data.trailer_url);
      }
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

  const handleWatchTrailer = useCallback(() => {
    if (!trailerUrl) {
      toast.error('Trailer not available for this movie');
      return;
    }
    setVideoLoading(true);
    setPlayerType('trailer');
    setShowPlayer(true);
  }, [trailerUrl]);

  const handleWatchMovie = useCallback(async () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to watch movies');
      return;
    }
    try {
      await watchAPI.startWatching(id);
    } catch (error) {
      console.error('Failed to record watch start:', error);
    }
    setVideoLoading(true);
    setPlayerType('movie');
    setShowPlayer(true);
  }, [id, isAuthenticated]);

  const handleClosePlayer = useCallback(() => {
    setShowPlayer(false);
    setPlayerType(null);
  }, []);

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

  const getCurrentUrl = () => {
    return playerType === 'trailer' ? trailerUrl : DEMO_MOVIE_URL;
  };

  const isYouTubeUrl = (url) => {
    return url && (url.includes('youtube.com') || url.includes('youtu.be'));
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

  const youtubeId = playerType === 'trailer' ? getYouTubeVideoId(trailerUrl) : null;

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[80vh] overflow-hidden">
        <div className="absolute inset-0">
          <img
            src={movie.backdrop_url || movie.poster_url}
            alt={movie.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-transparent" />
        </div>

        <button
          onClick={() => navigate(-1)}
          className="absolute top-24 left-6 z-20 flex items-center gap-2 px-4 py-2 rounded-full glass-effect hover:bg-white/20 text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

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
                  <span key={genre} className="px-3 py-1 rounded-full bg-white/10 text-white text-sm">
                    {genre}
                  </span>
                ))}
              </div>

              <p className="text-lg text-text-secondary max-w-3xl">{movie.overview}</p>

              {/* Action Buttons - Watch Movie and Watch Trailer */}
              <div className="flex flex-wrap gap-4 pt-4">
                <button
                  onClick={handleWatchMovie}
                  className="bg-primary hover:bg-primary-hover text-black font-bold py-3 px-8 rounded-full flex items-center gap-2 transition-all hover:scale-105 shadow-glow"
                >
                  <Play className="w-5 h-5 fill-current" />
                  Watch Movie
                </button>

                <button
                  onClick={handleWatchTrailer}
                  disabled={!trailerUrl}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded-full flex items-center gap-2 transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  <Film className="w-5 h-5" />
                  {trailerUrl ? 'Watch Trailer' : 'No Trailer'}
                </button>

                <button
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

      {/* Video Player Modal - Using native iframe for YouTube */}
      <AnimatePresence>
        {showPlayer && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black z-50 flex items-center justify-center"
          >
            <div className="w-full h-full relative">
              {/* Close Button */}
              <button
                onClick={handleClosePlayer}
                className="absolute top-4 right-4 text-white hover:text-primary transition-colors z-20 bg-black/50 p-2 rounded-full"
              >
                <X className="w-8 h-8" />
              </button>

              {/* Loading Indicator */}
              {videoLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black z-10">
                  <div className="text-center">
                    <Loader className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
                    <p className="text-white">Loading {playerType === 'trailer' ? 'trailer' : 'movie'}...</p>
                  </div>
                </div>
              )}

              {/* Video Content */}
              <div className="w-full h-full">
                {playerType === 'trailer' && youtubeId ? (
                  <iframe
                    src={`https://www.youtube.com/embed/${youtubeId}?autoplay=1&rel=0&modestbranding=1`}
                    className="w-full h-full"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
                    allowFullScreen
                    onLoad={() => setVideoLoading(false)}
                    title={movie.title + ' Trailer'}
                    frameBorder="0"
                  />
                ) : (
                  <video
                    src={getCurrentUrl()}
                    className="w-full h-full"
                    controls
                    autoPlay
                    onLoadedData={() => setVideoLoading(false)}
                    onError={() => {
                      setVideoLoading(false);
                      toast.error('Error loading video');
                    }}
                  />
                )}
              </div>

              {/* Movie Info Overlay */}
              <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black to-transparent">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-3 py-1 text-white text-sm font-bold rounded ${playerType === 'trailer' ? 'bg-red-600' : 'bg-primary'}`}>
                    {playerType === 'trailer' ? 'TRAILER' : 'MOVIE'}
                  </span>
                  <h2 className="text-xl font-bold text-white">{movie.title}</h2>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Rating Section */}
      {isAuthenticated && (
        <section className="py-12 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="glass-effect rounded-2xl p-8">
              <h2 className="font-heading text-2xl font-bold text-white mb-4">Rate this movie</h2>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button key={rating} onClick={() => handleRate(rating)} className="group">
                    <Star className={`w-8 h-8 transition-colors ${rating <= userRating ? 'text-yellow-400 fill-current' : 'text-text-muted group-hover:text-yellow-400'}`} />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Similar Movies */}
      {similarMovies.length > 0 && (
        <section className="py-12 px-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="font-heading text-3xl font-bold text-white mb-8">Similar Movies</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
              {similarMovies.map((m) => (
                <MovieCard key={m.id} movie={m} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default MovieDetailPage;
