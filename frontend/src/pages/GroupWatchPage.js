import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Users, Send, X, Loader, MessageCircle, Play, Pause } from 'lucide-react';
import ReactPlayer from 'react-player';
import { groupAPI, moviesAPI } from '../api';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

// Demo movie URL
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
  const playerRef = useRef(null);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);
  const [isHost, setIsHost] = useState(false);

  useEffect(() => {
    fetchSession();
  }, [sessionId]);

  useEffect(() => {
    if (session && user) {
      connectWebSocket();
    }
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [session, user]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);

  const fetchSession = async () => {
    try {
      const response = await groupAPI.getSession(sessionId);
      setSession(response.data);
      setIsHost(response.data.host_user_id === user?.id);
      
      // Fetch movie trailer URL if available
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
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    // Convert HTTPS to WSS and HTTP to WS
    const wsProtocol = backendUrl.includes('https') ? 'wss' : 'ws';
    const cleanUrl = backendUrl.replace('https://', '').replace('http://', '');
    const wsUrl = `${wsProtocol}://${cleanUrl}/ws/group/${sessionId}/${user.id}`;
    
    console.log('Connecting to WebSocket:', wsUrl);
    
    try {
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
        setWsConnected(true);
        toast.success('Connected to watch party chat!');
      };
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);
        
        switch (data.type) {
          case 'state_sync':
            setPlaying(data.state?.is_playing || false);
            break;
          
          case 'playback_update':
            setPlaying(data.state?.is_playing || false);
            break;
          
          case 'chat_message':
            setChatMessages(prev => [...prev, {
              user_id: data.user_id,
              message: data.message,
              timestamp: data.timestamp,
              isOwn: data.user_id === user.id
            }]);
            break;
          
          case 'user_joined':
            toast.success('Someone joined the party!');
            break;
          
          case 'user_left':
            toast.info('Someone left the party');
            break;
          
          default:
            console.log('Unknown message type:', data.type);
            break;
        }
      };
      
      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setWsConnected(false);
        toast.error('Connection error - chat may not work');
      };
      
      wsRef.current.onclose = () => {
        console.log('WebSocket disconnected');
        setWsConnected(false);
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      toast.error('Could not connect to chat');
    }
  };

  const handleSendMessage = useCallback(() => {
    const trimmedMessage = newMessage.trim();
    
    if (!trimmedMessage) {
      return;
    }
    
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      toast.error('Not connected to chat. Please refresh the page.');
      return;
    }
    
    const message = {
      type: 'chat_message',
      message: trimmedMessage,
      user_id: user.id
    };
    
    try {
      wsRef.current.send(JSON.stringify(message));
      setNewMessage('');
      console.log('Message sent:', message);
    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error('Failed to send message');
    }
  }, [newMessage, user?.id]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  }, [handleSendMessage]);

  const handlePlayPause = useCallback(() => {
    const newPlayingState = !playing;
    setPlaying(newPlayingState);
    
    // Sync with other users
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'playback_update',
        state: {
          is_playing: newPlayingState
        }
      }));
    }
  }, [playing]);

  const getVideoUrl = () => {
    // Use trailer URL if available, otherwise use demo video
    return trailerUrl || DEMO_MOVIE_URL;
  };

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
      <div className="max-w-7xl mx-auto p-6">
        {/* Session Info */}
        <div className="glass-effect rounded-2xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-heading text-3xl font-bold text-white mb-2">{session.name}</h1>
              <p className="text-text-secondary">{session.movie?.title}</p>
              <div className="flex items-center gap-2 mt-2">
                <span className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span className="text-sm text-text-secondary">
                  {wsConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
            <button
              onClick={() => navigate('/groups')}
              className="bg-white/10 hover:bg-white/20 text-white p-3 rounded-full transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Video Player */}
          <div className="lg:col-span-2">
            <div className="glass-effect rounded-2xl overflow-hidden">
              <div className="relative pt-[56.25%] bg-black">
                <div className="absolute inset-0">
                  <ReactPlayer
                    ref={playerRef}
                    url={getVideoUrl()}
                    width="100%"
                    height="100%"
                    controls
                    playing={playing}
                    onPlay={() => setPlaying(true)}
                    onPause={() => setPlaying(false)}
                    config={{
                      youtube: {
                        playerVars: {
                          showinfo: 1,
                          rel: 0,
                          modestbranding: 1
                        }
                      },
                      file: {
                        attributes: {
                          controlsList: 'nodownload',
                          playsInline: true,
                        },
                      },
                    }}
                  />
                </div>
              </div>
              
              {/* Custom Play/Pause Control */}
              <div className="p-4 flex items-center gap-4">
                <button
                  onClick={handlePlayPause}
                  className="bg-primary hover:bg-primary-hover text-black p-3 rounded-full transition-colors"
                >
                  {playing ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                </button>
                <span className="text-white text-sm">
                  {playing ? 'Playing' : 'Paused'}
                </span>
                {trailerUrl && (
                  <span className="text-xs text-text-secondary ml-auto">
                    Playing: {session.movie?.title} Trailer
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Chat Section */}
          <div className="glass-effect rounded-2xl p-6 flex flex-col h-[500px]">
            <div className="flex items-center gap-2 mb-4">
              <MessageCircle className="w-5 h-5 text-primary" />
              <h2 className="font-heading text-xl font-bold text-white">
                Chat
              </h2>
              <span className="text-sm text-text-secondary ml-auto">
                {session.member_count} member{session.member_count !== 1 ? 's' : ''}
              </span>
            </div>
            
            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto mb-4 space-y-3 pr-2">
              {chatMessages.length === 0 ? (
                <div className="text-center text-text-secondary py-8">
                  <MessageCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>No messages yet.</p>
                  <p className="text-sm">Start the conversation!</p>
                </div>
              ) : (
                chatMessages.map((msg, index) => (
                  <motion.div 
                    key={index} 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`rounded-lg p-3 ${
                      msg.isOwn 
                        ? 'bg-primary/20 ml-4' 
                        : 'bg-white/5 mr-4'
                    }`}
                  >
                    <p className="text-white text-sm">{msg.message}</p>
                    <p className="text-text-secondary text-xs mt-1">
                      {msg.isOwn ? 'You' : `User`}
                      {msg.timestamp && ` • ${new Date(msg.timestamp).toLocaleTimeString()}`}
                    </p>
                  </motion.div>
                ))
              )}
              <div ref={chatEndRef} />
            </div>
            
            {/* Message Input */}
            <div className="flex gap-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={wsConnected ? "Type a message..." : "Connecting..."}
                disabled={!wsConnected}
                className="flex-1 bg-zinc-900/50 border border-white/10 rounded-lg text-white px-4 py-2 placeholder:text-text-muted disabled:opacity-50"
              />
              <button 
                onClick={handleSendMessage}
                disabled={!wsConnected || !newMessage.trim()}
                className="bg-primary hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed text-black p-2 rounded-lg transition-colors"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            
            {!wsConnected && (
              <p className="text-red-400 text-xs mt-2">
                Chat disconnected. Please refresh the page.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GroupWatchPage;
