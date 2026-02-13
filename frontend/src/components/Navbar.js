import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Film, Search, User, LogOut, Home, TrendingUp } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { toast } from 'sonner';

export const Navbar = ({ onAuthClick }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-40 glass-effect border-b border-white/5"
    >
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" data-testid="navbar-logo" className="flex items-center gap-2 group">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary-hover rounded-lg flex items-center justify-center">
              <Film className="w-6 h-6 text-black" />
            </div>
            <span className="font-heading text-xl font-bold text-white group-hover:text-primary transition-colors">
              CineAI
            </span>
          </Link>

          {/* Nav Links */}
          {isAuthenticated && (
            <div className="hidden md:flex items-center gap-6">
              <Link
                to="/"
                data-testid="nav-link-home"
                className="flex items-center gap-2 text-text-secondary hover:text-white transition-colors"
              >
                <Home className="w-5 h-5" />
                Home
              </Link>
              <Link
                to="/browse"
                data-testid="nav-link-browse"
                className="flex items-center gap-2 text-text-secondary hover:text-white transition-colors"
              >
                <Search className="w-5 h-5" />
                Browse
              </Link>
              <Link
                to="/recommendations"
                data-testid="nav-link-recommendations"
                className="flex items-center gap-2 text-text-secondary hover:text-white transition-colors"
              >
                <TrendingUp className="w-5 h-5" />
                For You
              </Link>
            </div>
          )}

          {/* User Actions */}
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/profile"
                  data-testid="nav-link-profile"
                  className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
                >
                  <User className="w-5 h-5" />
                  <span className="hidden sm:inline">{user?.name}</span>
                </Link>
                <button
                  data-testid="nav-logout-button"
                  onClick={handleLogout}
                  className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </>
            ) : (
              <button
                data-testid="nav-signin-button"
                onClick={onAuthClick}
                className="bg-primary hover:bg-primary-hover text-black font-bold py-2 px-6 rounded-full transition-transform hover:scale-105"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>
    </motion.nav>
  );
};
