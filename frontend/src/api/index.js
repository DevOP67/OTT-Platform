import api from './client';

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
  updatePreferences: (preferences) => api.put('/auth/preferences', preferences),
};

export const moviesAPI = {
  getMovies: (params) => api.get('/movies', { params }),
  getMovie: (id) => api.get(`/movies/${id}`),
  searchMovies: (query) => api.get('/movies/search/query', { params: { q: query } }),
  syncMovies: () => api.post('/admin/sync-movies'),
};

export const recommendationsAPI = {
  getPersonalized: (limit = 20) => api.get('/recommendations/personalized', { params: { limit } }),
  getTrending: (limit = 20) => api.get('/recommendations/trending', { params: { limit } }),
  getSimilar: (movieId, limit = 10) => api.get(`/recommendations/similar/${movieId}`, { params: { limit } }),
  getIntelligent: (limit = 20) => api.get('/recommendations/intelligent', { params: { limit } }),
};

export const watchAPI = {
  startWatching: (movieId) => api.post('/watch/start', null, { params: { movie_id: movieId } }),
  updateProgress: (data) => api.put('/watch/progress', data),
  rateMovie: (data) => api.post('/watch/rate', data),
  getHistory: (limit = 50) => api.get('/watch/history', { params: { limit } }),
};

export const interactionsAPI = {
  create: (data) => api.post('/interactions', data),
};

export const behaviorAPI = {
  getProfile: () => api.get('/behavior/profile'),
  recordSignal: (signal) => api.post('/behavior/signal', signal),
};

export const groupAPI = {
  createSession: (data) => api.post('/groups/create', data),
  getSession: (sessionId) => api.get(`/groups/${sessionId}`),
  joinSession: (sessionId) => api.post(`/groups/${sessionId}/join`),
  getUserSessions: () => api.get('/groups'),
  endSession: (sessionId) => api.post(`/groups/${sessionId}/end`),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
};
