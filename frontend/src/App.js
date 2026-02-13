import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { AuthModal } from './components/AuthModal';
import LandingPage from './pages/LandingPage';
import BrowsePage from './pages/BrowsePage';
import MovieDetailPage from './pages/MovieDetailPage';
import RecommendationsPage from './pages/RecommendationsPage';
import IntelligentRecommendationsPage from './pages/IntelligentRecommendationsPage';
import GroupSessionsPage from './pages/GroupSessionsPage';
import GroupWatchPage from './pages/GroupWatchPage';
import ProfilePage from './pages/ProfilePage';
import { moviesAPI } from './api';
import { Toaster, toast } from 'sonner';
import '@/App.css';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-primary">Loading...</div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/" />;
};

const AppContent = () => {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { isAuthenticated } = useAuth();
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    // Initialize data on first load
    const initializeData = async () => {
      try {
        // Sync movies from TMDB
        await moviesAPI.syncMovies();
        setInitialized(true);
      } catch (error) {
        console.error('Failed to initialize data:', error);
        // Continue anyway - there might be existing data
        setInitialized(true);
      }
    };

    if (!initialized) {
      initializeData();
    }
  }, []);

  return (
    <div className="App">
      <Toaster position="top-right" theme="dark" richColors />
      <Navbar onAuthClick={() => setShowAuthModal(true)} />
      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />

      <Routes>
        <Route path="/" element={<LandingPage onAuthClick={() => setShowAuthModal(true)} />} />
        <Route
          path="/browse"
          element={
            <ProtectedRoute>
              <BrowsePage />
            </ProtectedRoute>
          }
        />
        <Route path="/movie/:id" element={<MovieDetailPage />} />
        <Route
          path="/recommendations"
          element={
            <ProtectedRoute>
              <RecommendationsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
