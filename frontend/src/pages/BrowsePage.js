import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Loader } from 'lucide-react';
import { moviesAPI } from '../api';
import { MovieCard } from '../components/MovieCard';
import { toast } from 'sonner';

export const BrowsePage = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller'];

  useEffect(() => {
    fetchMovies();
  }, [page, selectedGenre]);

  const fetchMovies = async () => {
    try {
      setLoading(true);
      const params = { page, limit: 20 };
      if (selectedGenre) params.genre = selectedGenre;
      
      const response = await moviesAPI.getMovies(params);
      setMovies(response.data.movies);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      toast.error('Failed to load movies');
      console.error('Error fetching movies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchMovies();
      return;
    }

    try {
      setLoading(true);
      const response = await moviesAPI.searchMovies(searchQuery);
      setMovies(response.data.movies);
    } catch (error) {
      toast.error('Search failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4">
            Browse Movies
          </h1>
          <p className="text-xl text-text-secondary">
            Explore our collection of amazing films
          </p>
        </motion.div>

        {/* Search and Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 space-y-4"
        >
          {/* Search Bar */}
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" />
              <input
                data-testid="search-input"
                type="text"
                placeholder="Search movies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-12 pr-4 py-3 bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white placeholder:text-text-muted"
              />
            </div>
            <button
              data-testid="search-button"
              onClick={handleSearch}
              className="bg-primary hover:bg-primary-hover text-black font-bold px-6 py-3 rounded-lg transition-transform hover:scale-105"
            >
              Search
            </button>
          </div>

          {/* Genre Filters */}
          <div className="flex items-center gap-3 overflow-x-auto pb-2">
            <Filter className="w-5 h-5 text-text-secondary flex-shrink-0" />
            <button
              data-testid="filter-all"
              onClick={() => setSelectedGenre('')}
              className={`px-4 py-2 rounded-full whitespace-nowrap transition-colors ${
                !selectedGenre
                  ? 'bg-primary text-black font-bold'
                  : 'bg-white/10 text-text-secondary hover:bg-white/20'
              }`}
            >
              All
            </button>
            {genres.map((genre) => (
              <button
                key={genre}
                data-testid={`filter-${genre.toLowerCase()}`}
                onClick={() => setSelectedGenre(genre)}
                className={`px-4 py-2 rounded-full whitespace-nowrap transition-colors ${
                  selectedGenre === genre
                    ? 'bg-primary text-black font-bold'
                    : 'bg-white/10 text-text-secondary hover:bg-white/20'
                }`}
              >
                {genre}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Movies Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader className="w-8 h-8 text-primary animate-spin" />
          </div>
        ) : movies.length > 0 ? (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6"
              data-testid="movies-grid"
            >
              {movies.map((movie, index) => (
                <motion.div
                  key={movie.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <MovieCard movie={movie} />
                </motion.div>
              ))}
            </motion.div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-4 mt-12">
                <button
                  data-testid="pagination-prev"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-6 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Previous
                </button>
                <span className="text-text-secondary">
                  Page {page} of {totalPages}
                </span>
                <button
                  data-testid="pagination-next"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-6 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-20">
            <p className="text-text-secondary text-lg">No movies found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrowsePage;
