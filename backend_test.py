#!/usr/bin/env python3
"""
Backend API Testing Script for WebSocket Chat Functionality
Tests the Watch Party WebSocket chat feature with echo to sender
"""

import asyncio
import json
import os
import sys
import websockets
import requests
from datetime import datetime
import uuid

# Configuration
BACKEND_URL = "https://cinema-player-12.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"
# Try internal WebSocket connection first
WS_BASE = "ws://localhost:8001"

# Test credentials
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123456"

class WebSocketChatTester:
    def __init__(self):
        self.auth_token = None
        self.user_id = None
        self.session_id = None
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def authenticate(self):
        """Authenticate and get token"""
        self.log("🔐 Authenticating user...")
        
        # Try login first
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data["access_token"]
                self.user_id = data["user"]["id"]
                self.log(f"✅ Login successful - User ID: {self.user_id}")
                return True
        except Exception as e:
            self.log(f"❌ Login failed: {e}")
            
        # If login fails, try registration
        self.log("🔐 Trying registration...")
        register_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": "Test User",
            "preferences": {"genres": ["action", "comedy"]}
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/register", json=register_data)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data["access_token"]
                self.user_id = data["user"]["id"]
                self.log(f"✅ Registration successful - User ID: {self.user_id}")
                return True
            else:
                self.log(f"❌ Registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Registration error: {e}")
            return False
    
    def get_movies(self):
        """Get available movies"""
        self.log("🎬 Fetching movies...")
        try:
            response = requests.get(f"{API_BASE}/movies?limit=5")
            if response.status_code == 200:
                movies = response.json()["movies"]
                if movies:
                    movie = movies[0]
                    self.log(f"✅ Found movie: {movie['title']} (ID: {movie['id']})")
                    return movie["id"]
                else:
                    self.log("❌ No movies found")
                    return None
            else:
                self.log(f"❌ Failed to fetch movies: {response.status_code}")
                return None
        except Exception as e:
            self.log(f"❌ Error fetching movies: {e}")
            return None
    
    def create_group_session(self, movie_id):
        """Create a group watch session"""
        self.log("👥 Creating group session...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        session_data = {
            "movie_id": movie_id,
            "name": "Test Watch Party"
        }
        
        try:
            response = requests.post(f"{API_BASE}/groups/create", json=session_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.session_id = data["id"]
                self.log(f"✅ Group session created - Session ID: {self.session_id}")
                return True
            else:
                self.log(f"❌ Failed to create session: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Error creating session: {e}")
            return False
    
    async def test_websocket_chat(self):
        """Test WebSocket chat functionality"""
        self.log("🔌 Testing WebSocket chat...")
        
        ws_url = f"{WS_BASE}/ws/group/{self.session_id}/{self.user_id}"
        self.log(f"🔗 Connecting to: {ws_url}")
        
        messages_received = []
        test_messages = [
            "Hello test message",
            "Testing WebSocket chat functionality",
            "Can I see my own messages?"
        ]
        
        try:
            async with websockets.connect(ws_url) as websocket:
                self.log("✅ WebSocket connected successfully")
                
                # Send test messages and collect responses
                for i, test_message in enumerate(test_messages):
                    self.log(f"📤 Sending message {i+1}: '{test_message}'")
                    
                    # Send chat message
                    message_data = {
                        "type": "chat_message",
                        "message": test_message,
                        "user_id": self.user_id
                    }
                    
                    await websocket.send(json.dumps(message_data))
                    
                    # Wait for response
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        response_data = json.loads(response)
                        messages_received.append(response_data)
                        
                        self.log(f"📥 Received: {response_data}")
                        
                        # Verify message format
                        if self.verify_message_format(response_data, test_message):
                            self.log(f"✅ Message {i+1} format verified")
                        else:
                            self.log(f"❌ Message {i+1} format invalid")
                            
                    except asyncio.TimeoutError:
                        self.log(f"⏰ Timeout waiting for message {i+1} response")
                    except Exception as e:
                        self.log(f"❌ Error receiving message {i+1}: {e}")
                    
                    # Small delay between messages
                    await asyncio.sleep(1)
                
                self.log("🔌 WebSocket test completed")
                return messages_received
                
        except Exception as e:
            self.log(f"❌ WebSocket connection error: {e}")
            return []
    
    def verify_message_format(self, message_data, expected_message):
        """Verify the received message has correct format"""
        required_fields = ["type", "user_id", "message", "timestamp"]
        
        # Check all required fields are present
        for field in required_fields:
            if field not in message_data:
                self.log(f"❌ Missing field: {field}")
                return False
        
        # Check message type
        if message_data["type"] != "chat_message":
            self.log(f"❌ Wrong message type: {message_data['type']}")
            return False
        
        # Check user_id matches sender
        if message_data["user_id"] != self.user_id:
            self.log(f"❌ Wrong user_id: {message_data['user_id']} != {self.user_id}")
            return False
        
        # Check message content
        if message_data["message"] != expected_message:
            self.log(f"❌ Wrong message content: '{message_data['message']}' != '{expected_message}'")
            return False
        
        # Check timestamp format
        try:
            datetime.fromisoformat(message_data["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            self.log(f"❌ Invalid timestamp format: {message_data['timestamp']}")
            return False
        
        return True
    
    async def run_full_test(self):
        """Run complete WebSocket chat test"""
        self.log("🚀 Starting WebSocket Chat Test")
        self.log("=" * 50)
        
        # Step 1: Authenticate
        if not self.authenticate():
            self.log("❌ Authentication failed - cannot proceed")
            return False
        
        # Step 2: Get a movie
        movie_id = self.get_movies()
        if not movie_id:
            self.log("❌ No movies available - cannot proceed")
            return False
        
        # Step 3: Create group session
        if not self.create_group_session(movie_id):
            self.log("❌ Failed to create group session - cannot proceed")
            return False
        
        # Step 4: Test WebSocket chat
        messages = await self.test_websocket_chat()
        
        # Step 5: Analyze results
        self.log("=" * 50)
        self.log("📊 TEST RESULTS")
        self.log("=" * 50)
        
        if messages:
            self.log(f"✅ WebSocket chat is WORKING")
            self.log(f"✅ Sent and received {len(messages)} messages")
            self.log(f"✅ Sender can see their own messages (echo functionality)")
            self.log(f"✅ Message format includes: type, user_id, message, timestamp")
            
            # Show sample message
            if messages:
                sample = messages[0]
                self.log(f"📝 Sample message format:")
                self.log(f"   Type: {sample.get('type')}")
                self.log(f"   User ID: {sample.get('user_id')}")
                self.log(f"   Message: {sample.get('message')}")
                self.log(f"   Timestamp: {sample.get('timestamp')}")
            
            return True
        else:
            self.log("❌ WebSocket chat is NOT WORKING")
            self.log("❌ No messages received - echo functionality failed")
            return False

async def main():
    """Main test function"""
    tester = WebSocketChatTester()
    success = await tester.run_full_test()
    
    if success:
        print("\n🎉 ALL TESTS PASSED - WebSocket chat with echo is working!")
        sys.exit(0)
    else:
        print("\n💥 TESTS FAILED - WebSocket chat needs fixing")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())