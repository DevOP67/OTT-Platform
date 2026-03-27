import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Users, Send, X, Loader, MessageCircle, Play, Pause } from 'lucide-react';
import { groupAPI, moviesAPI } from '../api';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

const DEMO_MOVIE_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";

export const GroupWatchPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [trailerUrl, setTrailerUrl] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);
  const videoRef = useRef(null);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    if (user) {
      fetchSession();
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId, user]);

  useEffect(() => {
    if (session && user && !wsRef.current) {
      connectWebSocket();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, user]);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);

  const fetchSession = async () => {
    try {
      const response = await groupAPI.getSession(sessionId);
      setSession(response.data);
      
      if (response.data.movie?.id) {
        try {
          const movieResponse = await moviesAPI.getMovie(response.data.movie.id);
          if (movieResponse.data.trailer_url) {
            setTrailerUrl(movieResponse.data.trailer_url);
          }
        } catch (error) {
          console.error('Failed to fetch movie details:', error);
        }
      }
    } catch (error) {
      toast.error('Failed to load session');
      navigate('/groups');
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      return;
    }

    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const wsProtocol = backendUrl.includes('https') ? 'wss' : 'ws';
    const cleanUrl = backendUrl.replace('https://', '').replace('http://', '');
    const wsUrl = `${wsProtocol}://${cleanUrl}/ws/group/${sessionId}/${user.id}`;
    
    console.log('Connecting to WebSocket:', wsUrl);
    
    try {
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
        setWsConnected(true);
        toast.success('Connected to chat!');
      };
      
      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Received:', data);
          
          if (data.type === 'chat_message') {
            setChatMessages(prev => [...prev, {
              user_id: data.user_id,
              message: data.message,
              timestamp: data.timestamp,
              isOwn: data.user_id === user.id
            }]);
          } else if (data.type === 'playback_update') {
            setPlaying(data.state?.is_playing || false);
          } else if (data.type === 'user_joined') {
            toast.success('Someone joined!');
          } else if (data.type === 'user_left') {
            toast.info('Someone left');
          }
        } catch (e) {
          console.error('Failed to parse message:', e);
        }
      };
      
      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setWsConnected(false);
      };
      
      wsRef.current.onclose = () => {
        console.log('WebSocket closed');
        setWsConnected(false);
        // Try to reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          if (session && user) {
            connectWebSocket();
          }
        }, 3000);
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      toast.error('Could not connect to chat');
    }
  };

  const handleSendMessage = useCallback(async () => {
    const trimmedMessage = newMessage.trim();
    
    if (!trimmedMessage) {
      return;
    }

    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      // Add message locally anyway for better UX
      setChatMessages(prev => [...prev, {
        user_id: user.id,
        message: trimmedMessage,
        timestamp: new Date().toISOString(),
        isOwn: true,
        pending: true
      }]);
      setNewMessage('');
      toast.error('Chat is reconnecting...');
      return;
    }
    
    setSendingMessage(true);
    
    try {
      const message = {
        type: 'chat_message',
        message: trimmedMessage,
        user_id: user.id
      };
      
      wsRef.current.send(JSON.stringify(message));
      setNewMessage('');
      console.log('Message sent:', message);
    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error('Failed to send message');
    } finally {
      setSendingMessage(false);
    }
  }, [newMessage, user]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  }, [handleSendMessage]);

  const handlePlayPause = () => {
    const newState = !playing;
    setPlaying(newState);
    
    if (videoRef.current) {
      if (newState) {
        videoRef.current.play();
      } else {
        videoRef.current.pause();
      }
    }
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'playback_update',
        state: { is_playing: newState }
      }));
    }
  };

  const getVideoUrl = () => {
    return trailerUrl || DEMO_MOVIE_URL;
  };

  const getYouTubeVideoId = (url) => {
    if (!url) return null;
    const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s]+)/);
    return match ? match[1] : null;
  };

  const youtubeId = getYouTubeVideoId(trailerUrl);

  if (loading) {
    return (
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="max-w-7xl mx-auto p-4">
        {/* Header */}
        <div className="glass-effect rounded-xl p-4 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-heading text-2xl font-bold text-white">{session.name}</h1>
              <p className="text-text-secondary text-sm">{session.movie?.title}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-xs text-text-secondary">{wsConnected ? 'Connected' : 'Reconnecting...'}</span>
              </div>
            </div>
            <button onClick={() => navigate('/groups')} className="bg-white/10 hover:bg-white/20 text-white p-2 rounded-full">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-4">
          {/* Video Player */}
          <div className="lg:col-span-2">
            <div className="glass-effect rounded-xl overflow-hidden">
              <div className="relative pt-[56.25%] bg-black">
                <div className="absolute inset-0">
                  {youtubeId ? (
                    <iframe
                      src={`https://www.youtube.com/embed/${youtubeId}?autoplay=0&rel=0`}
                      className="w-full h-full"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      title="Watch Party Video"
                    />
                  ) : (
                    <video
                      ref={videoRef}
                      src={getVideoUrl()}
                      className="w-full h-full"
                      controls
                    />
                  )}
                </div>
              </div>
              
              <div className="p-3 flex items-center gap-3">
                <button onClick={handlePlayPause} className="bg-primary hover:bg-primary-hover text-black p-2 rounded-full">
                  {playing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                </button>
                <span className="text-white text-sm">{playing ? 'Playing' : 'Paused'}</span>
              </div>
            </div>
          </div>

          {/* Chat */}
          <div className="glass-effect rounded-xl p-4 flex flex-col h-[500px]">
            <div className="flex items-center gap-2 mb-3">
              <MessageCircle className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-bold text-white">Chat</h2>
              <span className="text-xs text-text-secondary ml-auto">{session.member_count} member(s)</span>
            </div>
            
            <div className="flex-1 overflow-y-auto mb-3 space-y-2">
              {chatMessages.length === 0 ? (
                <div className="text-center text-text-secondary py-8">
                  <MessageCircle className="w-10 h-10 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No messages yet</p>
                  <p className="text-xs">Start chatting!</p>
                </div>
              ) : (
                chatMessages.map((msg, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`rounded-lg p-2 text-sm ${msg.isOwn ? 'bg-primary/20 ml-8' : 'bg-white/5 mr-8'} ${msg.pending ? 'opacity-50' : ''}`}
                  >
                    <p className="text-white">{msg.message}</p>
                    <p className="text-text-secondary text-xs mt-1">
                      {msg.isOwn ? 'You' : 'User'}
                      {msg.timestamp && ` • ${new Date(msg.timestamp).toLocaleTimeString()}`}
                    </p>
                  </motion.div>
                ))
              )}
              <div ref={chatEndRef} />
            </div>
            
            <div className="flex gap-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={wsConnected ? "Type a message..." : "Reconnecting..."}
                className="flex-1 bg-zinc-900/50 border border-white/10 rounded-lg text-white px-3 py-2 text-sm"
              />
              <button
                onClick={handleSendMessage}
                disabled={sendingMessage || !newMessage.trim()}
                className="bg-primary hover:bg-primary-hover disabled:opacity-50 text-black p-2 rounded-lg"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GroupWatchPage;
