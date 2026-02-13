import React from 'react';
import { motion } from 'framer-motion';
import { Play, Star, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const MovieCard = ({ movie, onClick }) => {
  const navigate = useNavigate();
  
  const handleClick = () => {
    if (onClick) {
      onClick(movie);
    } else {
      navigate(`/movie/${movie.id}`);
    }
  };

  return (
    <motion.div
      data-testid={`movie-card-${movie.id}`}
      className="movie-card group relative aspect-[2/3] overflow-hidden rounded-xl bg-zinc-900 border border-white/5 hover:border-primary/50 cursor-pointer"
      whileHover={{ y: -4 }}
      transition={{ duration: 0.3 }}
      onClick={handleClick}
    >
      {/* Movie Poster */}
      <img
        src={movie.poster_url || 'https://images.unsplash.com/photo-1762356121454-877acbd554bb?w=500'}
        alt={movie.title}
        className="w-full h-full object-cover"
      />
      
      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div className="absolute bottom-0 left-0 right-0 p-4 space-y-2">
          <h3 className="font-heading font-bold text-lg text-white line-clamp-2">{movie.title}</h3>
          
          <div className="flex items-center gap-3 text-sm">
            <div className="flex items-center gap-1 text-yellow-400">
              <Star className="w-4 h-4 fill-current" />
              <span>{movie.rating?.toFixed(1)}</span>
            </div>
            {movie.runtime && (
              <div className="flex items-center gap-1 text-text-secondary">
                <Clock className="w-4 h-4" />
                <span>{movie.runtime}min</span>
              </div>
            )}
          </div>
          
          <div className="flex flex-wrap gap-2">
            {movie.genres?.slice(0, 2).map((genre, idx) => (
              <span key={idx} className="text-xs px-2 py-1 rounded-full bg-white/10 text-text-secondary">
                {genre}
              </span>
            ))}
          </div>
          
          <button
            data-testid={`play-button-${movie.id}`}
            className="w-full mt-2 bg-primary hover:bg-primary-hover text-black font-bold py-2 px-4 rounded-full flex items-center justify-center gap-2 transition-transform hover:scale-105"
          >
            <Play className="w-4 h-4 fill-current" />
            Watch Now
          </button>
        </div>
      </div>
      
      {/* Rating Badge */}
      <div className="absolute top-3 right-3 bg-black/80 backdrop-blur-sm px-2 py-1 rounded-lg flex items-center gap-1">
        <Star className="w-3 h-3 text-yellow-400 fill-current" />
        <span className="text-xs font-bold text-white">{movie.rating?.toFixed(1)}</span>
      </div>
    </motion.div>
  );
};
