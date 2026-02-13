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
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const playerRef = useRef(null);
  const wsRef = useRef(null);
  const [isHost, setIsHost] = useState(false);
  const [position, setPosition] = useState(0);
  const [onlineUsers, setOnlineUsers] = useState([]);

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
        toast.success('Connected to watch party');
      };
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'state_sync':
            setPlaying(data.state.is_playing || false);
            break;
          
          case 'playback_update':
            setPlaying(data.state.is_playing || false);
            break;
          
          case 'chat_message':
            setChatMessages(prev => [...prev, {
              user_id: data.user_id,
              message: data.message,
              timestamp: data.timestamp
            }]);
            break;
          
          case 'user_joined':
            toast.success('Someone joined the party');
            break;
          
          default:
            break;
        }
      };
      
      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        toast.error('Connection error - chat may not work');
      };
      
      wsRef.current.onclose = () => {
        console.log('WebSocket disconnected');
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      toast.error('Could not connect to chat');
    }
  };

  const sendMessage = () => {
    if (newMessage.trim() && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const message = {
        type: 'chat_message',
        message: newMessage.trim(),
        user_id: user.id
      };
      wsRef.current.send(JSON.stringify(message));
      setNewMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
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
            </div>
            <button
              onClick={() => navigate('/groups')}
              className="bg-white/10 hover:bg-white/20 text-white p-3 rounded-full transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Video Player */}
        <div className="glass-effect rounded-2xl overflow-hidden mb-6">
          <div className="relative pt-[56.25%] bg-black">
            <div className="absolute inset-0">
              <ReactPlayer
                ref={playerRef}
                url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                width="100%"
                height="100%"
                controls
                playing={playing}
              />
            </div>
          </div>
        </div>

        {/* Chat Section */}
        <div className="glass-effect rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Users className="w-5 h-5 text-primary" />
            <h2 className="font-heading text-xl font-bold text-white">
              Chat ({session.member_count} members)
            </h2>
          </div>
          
          <div className="h-64 overflow-y-auto mb-4 space-y-3">
            {chatMessages.map((msg, index) => (
              <div key={index} className="bg-white/5 rounded-lg p-3">
                <p className="text-white text-sm">{msg.message}</p>
              </div>
            ))}
          </div>
          
          <div className="flex gap-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type a message..."
              className="flex-1 bg-zinc-900/50 border border-white/10 rounded-lg text-white px-4 py-2"
            />
            <button 
              onClick={sendMessage}
              className="bg-primary hover:bg-primary-hover text-black p-2 rounded-lg"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GroupWatchPage;
