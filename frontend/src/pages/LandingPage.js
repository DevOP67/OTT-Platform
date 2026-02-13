import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Play, Sparkles, TrendingUp, Brain } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const LandingPage = ({ onAuthClick }) => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/browse');
    } else {
      onAuthClick();
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1725612218029-ae9961db0d96?w=1920"
            alt="Hero Background"
            className="w-full h-full object-cover opacity-30"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent" />
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/30 text-primary text-sm font-medium"
          >
            <Sparkles className="w-4 h-4" />
            AI-Powered Recommendations
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-white leading-tight"
          >
            Your Next Favorite Movie
            <br />
            <span className="text-gradient">Discovered by AI</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl text-text-secondary max-w-2xl mx-auto"
          >
            Experience intelligent movie recommendations powered by advanced machine learning.
            Personalized suggestions that understand your taste and mood.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <button
              data-testid="hero-get-started-button"
              onClick={handleGetStarted}
              className="bg-primary hover:bg-primary-hover text-black font-bold py-4 px-8 rounded-full flex items-center gap-2 transition-transform hover:scale-105 shadow-glow"
            >
              <Play className="w-5 h-5 fill-current" />
              Get Started
            </button>
            <button
              data-testid="hero-explore-button"
              onClick={() => window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })}
              className="bg-white/10 hover:bg-white/20 text-white font-bold py-4 px-8 rounded-full backdrop-blur-md border border-white/10 transition-colors"
            >
              Explore Features
            </button>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <div className="w-6 h-10 border-2 border-white/30 rounded-full flex items-start justify-center p-2">
            <motion.div
              animate={{ y: [0, 12, 0] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
              className="w-1.5 h-1.5 bg-primary rounded-full"
            />
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4">
              Intelligent Features
            </h2>
            <p className="text-xl text-text-secondary max-w-2xl mx-auto">
              Powered by cutting-edge AI and machine learning
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: 'AI Recommendations',
                description: 'Hybrid collaborative and content-based filtering learns your unique taste',
              },
              {
                icon: TrendingUp,
                title: 'Real-time Adaptation',
                description: 'Recommendations evolve based on your watch patterns and ratings',
              },
              {
                icon: Sparkles,
                title: 'Smart Discovery',
                description: 'Find hidden gems with intelligent similarity matching and mood detection',
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="rec-card group"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-heading text-xl font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-text-secondary">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto text-center glass-heavy rounded-3xl p-12"
        >
          <h2 className="font-heading text-4xl lg:text-5xl font-bold text-white mb-4">
            Ready to Discover?
          </h2>
          <p className="text-xl text-text-secondary mb-8">
            Join thousands of movie lovers using AI to find their perfect match
          </p>
          <button
            data-testid="cta-get-started-button"
            onClick={handleGetStarted}
            className="bg-primary hover:bg-primary-hover text-black font-bold py-4 px-8 rounded-full transition-transform hover:scale-105 shadow-glow"
          >
            Start Watching Now
          </button>
        </motion.div>
      </section>
    </div>
  );
};

export default LandingPage;
