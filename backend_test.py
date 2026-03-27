#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for AI Movie Recommendation Platform
Tests all endpoints using the public URL for production-like testing
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class MoviePlatformTester:
    def __init__(self, base_url="https://cinema-player-12.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
        # Test data
        self.test_user = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
        
    def log_test(self, name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if response_data and isinstance(response_data, dict):
            result["response_sample"] = str(response_data)[:200]  # Truncate for readability
            
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def make_request(self, method: str, endpoint: str, expected_status: int = 200, 
                    data: Optional[Dict] = None, params: Optional[Dict] = None) -> tuple:
        """Make HTTP request and return success status and response"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
            
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}
                
            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"status_code": response.status_code, "text": response.text[:200]}
                
            return success, response_data
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}

    def test_health_check(self):
        """Test basic connectivity"""
        success, response = self.make_request('GET', 'health')
        self.log_test(
            "Health Check", 
            success, 
            f"Backend connectivity test",
            response
        )
        return success

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.make_request('GET', '')
        self.log_test(
            "Root Endpoint", 
            success, 
            "API root endpoint accessibility",
            response
        )
        return success

    def test_user_registration(self):
        """Test user registration"""
        # First try to register new user with timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%H%M%S")
        test_data = {
            "email": f"testuser_{timestamp}@example.com",
            "password": "testpass123",
            "name": "Test User Registration",
            "preferences": {
                "favorite_genres": ["Action", "Sci-Fi"],
                "mood": "excited"
            }
        }
        
        success, response = self.make_request('POST', 'auth/register', 200, test_data)
        
        if success and 'access_token' in response:
            details = f"Successfully registered user: {test_data['email']}"
        else:
            details = f"Registration failed for {test_data['email']}"
            
        self.log_test("User Registration", success, details, response)
        return success

    def test_user_login(self):
        """Test user login with provided test credentials"""
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        
        success, response = self.make_request('POST', 'auth/login', 200, login_data)
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response.get('user', {}).get('id')
            details = f"Successfully logged in as {self.test_user['email']}"
        else:
            details = f"Login failed for {self.test_user['email']}"
            
        self.log_test("User Login", success, details, response)
        return success

    def test_get_current_user(self):
        """Test getting current user info"""
        if not self.token:
            self.log_test("Get Current User", False, "No auth token available")
            return False
            
        success, response = self.make_request('GET', 'auth/me')
        
        if success and 'email' in response:
            details = f"Retrieved user info for {response.get('email')}"
        else:
            details = "Failed to get current user info"
            
        self.log_test("Get Current User", success, details, response)
        return success

    def test_sync_movies(self):
        """Test movie synchronization from TMDB"""
        success, response = self.make_request('POST', 'admin/sync-movies')
        
        if success:
            details = f"Movie sync completed: {response.get('message', 'Success')}"
        else:
            details = "Movie sync failed - may use mock data"
            
        self.log_test("Sync Movies", success, details, response)
        return success

    def test_get_movies(self):
        """Test getting movies list"""
        success, response = self.make_request('GET', 'movies')
        
        if success and 'movies' in response:
            movie_count = len(response['movies'])
            total = response.get('total', 0)
            details = f"Retrieved {movie_count} movies (total: {total})"
        else:
            details = "Failed to retrieve movies"
            
        self.log_test("Get Movies", success, details, response)
        return success, response.get('movies', []) if success else []

    def test_search_movies(self):
        """Test movie search functionality"""
        search_params = {"q": "action"}
        success, response = self.make_request('GET', 'movies/search/query', params=search_params)
        
        if success and 'movies' in response:
            movie_count = len(response['movies'])
            details = f"Search returned {movie_count} movies for 'action'"
        else:
            details = "Movie search failed"
            
        self.log_test("Search Movies", success, details, response)
        return success

    def test_get_movie_details(self, movie_id: str):
        """Test getting specific movie details"""
        success, response = self.make_request('GET', f'movies/{movie_id}')
        
        if success and 'title' in response:
            details = f"Retrieved details for movie: {response.get('title')}"
        else:
            details = f"Failed to get details for movie ID: {movie_id}"
            
        self.log_test("Get Movie Details", success, details, response)
        return success

    def test_start_watching(self, movie_id: str):
        """Test starting to watch a movie"""
        if not self.token:
            self.log_test("Start Watching", False, "No auth token available")
            return False
            
        success, response = self.make_request('POST', f'watch/start?movie_id={movie_id}')
        
        if success:
            details = f"Started watching movie {movie_id}: {response.get('message')}"
        else:
            details = f"Failed to start watching movie {movie_id}"
            
        self.log_test("Start Watching", success, details, response)
        return success

    def test_rate_movie(self, movie_id: str):
        """Test rating a movie"""
        if not self.token:
            self.log_test("Rate Movie", False, "No auth token available")
            return False
            
        rating_data = {
            "movie_id": movie_id,
            "rating": 4.5
        }
        
        success, response = self.make_request('POST', 'watch/rate', 200, rating_data)
        
        if success:
            details = f"Successfully rated movie {movie_id} with 4.5 stars"
        else:
            details = f"Failed to rate movie {movie_id}"
            
        self.log_test("Rate Movie", success, details, response)
        return success

    def test_get_watch_history(self):
        """Test getting user watch history"""
        if not self.token:
            self.log_test("Get Watch History", False, "No auth token available")
            return False
            
        success, response = self.make_request('GET', 'watch/history')
        
        if success and 'history' in response:
            history_count = len(response['history'])
            details = f"Retrieved {history_count} watch history items"
        else:
            details = "Failed to get watch history"
            
        self.log_test("Get Watch History", success, details, response)
        return success

    def test_personalized_recommendations(self):
        """Test getting personalized recommendations"""
        if not self.token:
            self.log_test("Personalized Recommendations", False, "No auth token available")
            return False
            
        success, response = self.make_request('GET', 'recommendations/personalized')
        
        if success and 'recommendations' in response:
            rec_count = len(response['recommendations'])
            details = f"Retrieved {rec_count} personalized recommendations"
        else:
            details = "Failed to get personalized recommendations"
            
        self.log_test("Personalized Recommendations", success, details, response)
        return success

    def test_trending_recommendations(self):
        """Test getting trending recommendations"""
        success, response = self.make_request('GET', 'recommendations/trending')
        
        if success and 'recommendations' in response:
            rec_count = len(response['recommendations'])
            details = f"Retrieved {rec_count} trending recommendations"
        else:
            details = "Failed to get trending recommendations"
            
        self.log_test("Trending Recommendations", success, details, response)
        return success

    def test_similar_movies(self, movie_id: str):
        """Test getting similar movies"""
        success, response = self.make_request('GET', f'recommendations/similar/{movie_id}')
        
        if success and 'recommendations' in response:
            rec_count = len(response['recommendations'])
            details = f"Retrieved {rec_count} similar movies for {movie_id}"
        else:
            details = f"Failed to get similar movies for {movie_id}"
            
        self.log_test("Similar Movies", success, details, response)
        return success

    def test_platform_stats(self):
        """Test getting platform statistics"""
        success, response = self.make_request('GET', 'admin/stats')
        
        if success:
            stats = {
                'users': response.get('total_users', 0),
                'movies': response.get('total_movies', 0),
                'watches': response.get('total_watches', 0)
            }
            details = f"Platform stats: {stats}"
        else:
            details = "Failed to get platform statistics"
            
        self.log_test("Platform Stats", success, details, response)
        return success

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🎬 Starting AI Movie Platform Backend Testing")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Basic connectivity tests
        if not self.test_health_check():
            print("❌ Backend is not accessible. Stopping tests.")
            return False
            
        self.test_root_endpoint()
        
        # Authentication tests
        self.test_user_registration()
        
        if not self.test_user_login():
            print("❌ Cannot login with test credentials. Stopping authenticated tests.")
            return False
            
        self.test_get_current_user()
        
        # Data initialization
        self.test_sync_movies()
        
        # Movie catalog tests
        movies_success, movies = self.test_get_movies()
        self.test_search_movies()
        
        # Test with first available movie if any
        test_movie_id = None
        if movies_success and movies:
            test_movie_id = movies[0].get('id')
            if test_movie_id:
                self.test_get_movie_details(test_movie_id)
                self.test_start_watching(test_movie_id)
                self.test_rate_movie(test_movie_id)
                self.test_similar_movies(test_movie_id)
        
        # User interaction tests
        self.test_get_watch_history()
        
        # Recommendation tests
        self.test_personalized_recommendations()
        self.test_trending_recommendations()
        
        # Admin tests
        self.test_platform_stats()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            failed_tests = [r for r in self.test_results if not r['success']]
            print(f"❌ {len(failed_tests)} tests failed:")
            for test in failed_tests:
                print(f"   - {test['test_name']}: {test['details']}")
            return False

def main():
    """Main test execution"""
    tester = MoviePlatformTester()
    
    try:
        success = tester.run_comprehensive_test()
        
        # Save detailed results
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': tester.tests_run,
                    'passed_tests': tester.tests_passed,
                    'success_rate': tester.tests_passed / tester.tests_run if tester.tests_run > 0 else 0,
                    'timestamp': datetime.now().isoformat()
                },
                'detailed_results': tester.test_results
            }, f, indent=2)
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"💥 Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())