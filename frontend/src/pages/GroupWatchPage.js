import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Users, Send, X, Loader } from 'lucide-react';
import ReactPlayer from 'react-player';
import { groupAPI } from '../api';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

export const GroupWatchPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState(false);
  const [position, setPosition] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [onlineUsers, setOnlineUsers] = useState([]);
  const playerRef = useRef(null);
  const wsRef = useRef(null);
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

  const fetchSession = async () => {
    try {
      const response = await groupAPI.getSession(sessionId);
      setSession(response.data);
      setIsHost(response.data.host_user_id === user?.id);
    } catch (error) {
      toast.error('Failed to load session');
      console.error(error);
      navigate('/groups');
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');
    const wsUrl = `${backendUrl}/ws/group/${sessionId}/${user.id}`;
    
    wsRef.current = new WebSocket(wsUrl);
    
    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      toast.success('Connected to watch party');
    };
    
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'state_sync':
          // Sync playback state
          setPosition(data.state.position);
          setPlaying(data.state.is_playing);
          if (playerRef.current) {
            playerRef.current.seekTo(data.state.position, 'seconds');
          }
          break;
        
        case 'playback_update':
          // Update playback from other users
          setPosition(data.state.position);
          setPlaying(data.state.is_playing);
          if (playerRef.current) {
            playerRef.current.seekTo(data.state.position, 'seconds');
          }
          break;
        
        case 'chat_message':
          // Add chat message
          setChatMessages(prev => [...prev, {
            user_id: data.user_id,
            message: data.message,
            timestamp: data.timestamp
          }]);
          break;
        
        case 'user_joined':
          toast.success('Someone joined the party');
          setOnlineUsers(prev => [...prev, data.user_id]);
          break;
        
        case 'user_left':
          setOnlineUsers(prev => prev.filter(id => id !== data.user_id));
          break;
        
        default:
          break;
      }
    };
    
    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      toast.error('Connection error');
    };
    
    wsRef.current.onclose = () => {
      console.log('WebSocket disconnected');
    };
  };

  const handlePlayPause = () => {
    const newPlayingState = !playing;
    setPlaying(newPlayingState);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'playback_update',
        state: {
          position: position,
          is_playing: newPlayingState
        }
      }));
    }
  };

  const handleProgress = (state) => {
    setPosition(state.playedSeconds);
    
    // Sync position every 5 seconds (only if host)
    if (isHost && state.playedSeconds % 5 < 0.5) {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'playback_update',
          state: {
            position: state.playedSeconds,
            is_playing: playing
          }
        }));
      }
    }
  };

  const handleSeek = (seconds) => {
    setPosition(seconds);
    if (playerRef.current) {
      playerRef.current.seekTo(seconds, 'seconds');
    }
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'seek',
        position: seconds,
        is_playing: playing
      }));
    }
  };

  const handleSendMessage = () => {
    if (!newMessage.trim()) return;
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'chat_message',
        message: newMessage
      }));
      
      // Add own message locally
      setChatMessages(prev => [...prev, {
        user_id: user.id,
        message: newMessage,
        timestamp: new Date().toISOString()
      }]);
      
      setNewMessage('');
    }
  };

  const handleEndSession = async () => {
    if (window.confirm('Are you sure you want to end this watch party?')) {
      try {
        await groupAPI.endSession(sessionId);
        toast.success('Watch party ended');
        navigate('/groups');
      } catch (error) {
        toast.error('Failed to end session');
      }
    }
  };

  if (loading) {
    return (
      <div className=\"min-h-screen pt-24 flex items-center justify-center\">
        <Loader className=\"w-8 h-8 text-primary animate-spin\" />
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className=\"min-h-screen bg-black\">
      {/* Video Player */}
      <div className=\"relative\">
        {/* Player Container */}
        <div className=\"relative pt-[56.25%] bg-black\">
          <div className=\"absolute inset-0\">
            <ReactPlayer
              ref={playerRef}
              url=\"https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4\"
              width=\"100%\"
              height=\"100%\"
              playing={playing}
              onPlay={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              onProgress={handleProgress}
              controls={isHost}
              progressInterval={500}
            />
          </div>
        </div>

        {/* Top Bar */}
        <div className=\"absolute top-0 left-0 right-0 p-6 bg-gradient-to-b from-black/80 to-transparent z-10\">
          <div className=\"flex items-center justify-between\">
            <div>
              <h1 className=\"font-heading text-2xl font-bold text-white mb-1\">{session.name}</h1>
              <p className=\"text-text-secondary\">{session.movie?.title}</p>
            </div>
            <button
              onClick={() => navigate('/groups')}
              className=\"bg-white/10 hover:bg-white/20 text-white p-2 rounded-full backdrop-blur-md transition-colors\"
            >
              <X className=\"w-6 h-6\" />
            </button>
          </div>
        </div>

        {/* Host Controls */}
        {!isHost && (
          <div className=\"absolute bottom-6 left-6 glass-effect rounded-lg px-4 py-2 z-10\">
            <p className=\"text-sm text-text-secondary\">
              Playback controlled by host
            </p>
          </div>
        )}
      </div>

      {/* Bottom Panel */}
      <div className=\"flex h-[400px]\">
        {/* Chat */}
        <div className=\"flex-1 bg-background-paper p-6 flex flex-col\">
          <div className=\"flex items-center gap-2 mb-4\">
            <Users className=\"w-5 h-5 text-primary\" />
            <h2 className=\"font-heading text-xl font-bold text-white\">
              Chat ({session.member_count} online)
            </h2>
          </div>

          {/* Messages */}
          <div className=\"flex-1 overflow-y-auto space-y-3 mb-4\" data-testid=\"chat-messages\">
            {chatMessages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.user_id === user.id ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    msg.user_id === user.id
                      ? 'bg-primary text-black'
                      : 'bg-white/10 text-white'
                  }`}
                >
                  <p className=\"text-sm\">{msg.message}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className=\"flex gap-2\">
            <input
              type=\"text\"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder=\"Type a message...\"
              className=\"flex-1 bg-zinc-900/50 border border-white/10 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-lg text-white px-4 py-2\"
              data-testid=\"chat-input\"
            />
            <button
              onClick={handleSendMessage}
              className=\"bg-primary hover:bg-primary-hover text-black p-2 rounded-lg transition-colors\"
              data-testid=\"send-message-button\"
            >
              <Send className=\"w-5 h-5\" />
            </button>
          </div>
        </div>

        {/* Info Panel */}
        <div className=\"w-80 bg-background-subtle p-6\">
          <h3 className=\"font-heading text-lg font-bold text-white mb-4\">Party Info</h3>
          
          <div className=\"space-y-4\">
            <div>
              <p className=\"text-sm text-text-secondary mb-1\">Host</p>
              <p className=\"text-white\">{isHost ? 'You' : 'Another user'}</p>
            </div>
            
            <div>
              <p className=\"text-sm text-text-secondary mb-1\">Members</p>
              <p className=\"text-white\">{session.member_count} watching</p>
            </div>

            {isHost && (
              <button
                onClick={handleEndSession}
                className=\"w-full bg-secondary hover:bg-secondary-hover text-white font-bold py-3 px-4 rounded-lg transition-colors\"
                data-testid=\"end-session-button\"
              >
                End Watch Party
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GroupWatchPage;
