import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';

export const AuthModal = ({ isOpen, onClose, defaultMode = 'login' }) => {
  const [mode, setMode] = useState(defaultMode);
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let result;
      if (mode === 'login') {
        result = await login(formData.email, formData.password);
      } else {
        result = await register(formData.name, formData.email, formData.password);
      }

      if (result.success) {
        toast.success(mode === 'login' ? 'Welcome back!' : 'Account created successfully!');
        onClose();
      } else {
        toast.error(result.error);
      }
    } catch (error) {
      toast.error('Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="glass-heavy rounded-2xl p-8 max-w-md w-full relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              data-testid="auth-modal-close"
              onClick={onClose}
              className="absolute top-4 right-4 text-text-secondary hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="text-center mb-6">
              <h2 className="font-heading text-3xl font-bold text-white mb-2">
                {mode === 'login' ? 'Welcome Back' : 'Create Account'}
              </h2>
              <p className="text-text-secondary">
                {mode === 'login' ? 'Sign in to continue' : 'Start your cinematic journey'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4" data-testid="auth-form">
              {mode === 'register' && (
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">
                    Name
                  </label>
                  <input
                    data-testid="auth-input-name"
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-3"
                    placeholder="John Doe"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  Email
                </label>
                <input
                  data-testid="auth-input-email"
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-3"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  Password
                </label>
                <input
                  data-testid="auth-input-password"
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-3"
                  placeholder="••••••••"
                />
              </div>

              <button
                data-testid="auth-submit-button"
                type="submit"
                disabled={loading}
                className="w-full bg-primary hover:bg-primary-hover text-black font-bold py-3 px-6 rounded-full transition-transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : mode === 'login' ? 'Sign In' : 'Create Account'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                data-testid="auth-toggle-mode"
                onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
                className="text-text-secondary hover:text-primary transition-colors"
              >
                {mode === 'login' ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
