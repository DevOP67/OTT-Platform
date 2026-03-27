#!/usr/bin/env python3
"""
Focused Testing for Curated Movie Database with YouTube Trailers
Tests the specific endpoints mentioned in the review request:
1. GET /api/movies - Verify trailer_url field
2. GET /api/movies/{movie_id}/trailer - New trailer endpoint
3. POST /api/admin/sync-movies - Sync curated movies
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class CuratedMovieTester:
    def __init__(self, base_url="https://cinema-player-12.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
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
            result["response_sample"] = str(response_data)[:300]  # Truncate for readability
            
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
            
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
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

    def test_sync_curated_movies(self):
        """Test POST /api/admin/sync-movies - Sync curated movies"""
        print("🔄 Testing curated movie synchronization...")
        success, response = self.make_request('POST', 'admin/sync-movies')
        
        if success:
            message = response.get('message', '')
            if 'Synced' in message or 'movies' in message.lower():
                details = f"Sync successful: {message}"
            else:
                details = f"Sync completed but unclear result: {message}"
        else:
            details = f"Sync failed - Status: {response.get('status_code', 'Unknown')}"
            
        self.log_test("Sync Curated Movies", success, details, response)
        return success

    def test_get_movies_with_trailers(self):
        """Test GET /api/movies - Verify movies have trailer_url field"""
        print("🎬 Testing movies endpoint for trailer URLs...")
        success, response = self.make_request('GET', 'movies')
        
        if not success:
            details = f"Failed to get movies - Status: {response.get('status_code', 'Unknown')}"
            self.log_test("Get Movies with Trailers", False, details, response)
            return False, []
        
        if 'movies' not in response:
            details = "Response missing 'movies' field"
            self.log_test("Get Movies with Trailers", False, details, response)
            return False, []
            
        movies = response['movies']
        if not movies:
            details = "No movies found in response"
            self.log_test("Get Movies with Trailers", False, details, response)
            return False, []
        
        # Check if movies have trailer_url field
        movies_with_trailers = 0
        total_movies = len(movies)
        sample_movie = None
        
        for movie in movies:
            if 'trailer_url' in movie and movie['trailer_url']:
                movies_with_trailers += 1
                if not sample_movie:
                    sample_movie = movie
        
        if movies_with_trailers > 0:
            details = f"Found {movies_with_trailers}/{total_movies} movies with trailer URLs"
            if sample_movie:
                details += f". Sample: '{sample_movie.get('title', 'Unknown')}' has trailer: {sample_movie.get('trailer_url', '')[:50]}..."
            success = True
        else:
            details = f"No movies have trailer_url field out of {total_movies} movies"
            success = False
            
        self.log_test("Get Movies with Trailers", success, details, response)
        return success, movies

    def test_movie_trailer_endpoint(self, movie_id: str, movie_title: str = "Unknown"):
        """Test GET /api/movies/{movie_id}/trailer - Get specific movie trailer"""
        print(f"🎥 Testing trailer endpoint for movie: {movie_title}")
        success, response = self.make_request('GET', f'movies/{movie_id}/trailer')
        
        if success:
            if 'trailer_url' in response and 'title' in response:
                trailer_url = response.get('trailer_url', '')
                title = response.get('title', '')
                if trailer_url and 'youtube.com' in trailer_url:
                    details = f"Retrieved trailer for '{title}': {trailer_url[:50]}..."
                else:
                    details = f"Trailer endpoint returned data but invalid YouTube URL: {trailer_url}"
                    success = False
            else:
                details = "Response missing required fields (trailer_url, title)"
                success = False
        else:
            status_code = response.get('status_code', 'Unknown')
            details = f"Failed to get trailer for movie {movie_id} - Status: {status_code}"
            
        self.log_test(f"Get Movie Trailer ({movie_title})", success, details, response)
        return success

    def test_invalid_movie_trailer(self):
        """Test GET /api/movies/{invalid_id}/trailer - Should return 404"""
        print("🚫 Testing trailer endpoint with invalid movie ID...")
        invalid_id = "invalid-movie-id-12345"
        success, response = self.make_request('GET', f'movies/{invalid_id}/trailer', expected_status=404)
        
        if success:
            details = f"Correctly returned 404 for invalid movie ID: {invalid_id}"
        else:
            actual_status = response.get('status_code', 'Unknown')
            details = f"Expected 404 but got {actual_status} for invalid movie ID"
            
        self.log_test("Invalid Movie Trailer (404 Test)", success, details, response)
        return success

    def run_curated_movie_tests(self):
        """Run all curated movie tests"""
        print("🎬 Starting Curated Movie Database Testing")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test 1: Sync curated movies
        sync_success = self.test_sync_curated_movies()
        
        # Test 2: Get movies with trailer URLs
        movies_success, movies = self.test_get_movies_with_trailers()
        
        # Test 3: Test trailer endpoint with valid movie IDs
        if movies_success and movies:
            # Test with first few movies that have trailer URLs
            tested_trailers = 0
            for movie in movies[:3]:  # Test first 3 movies
                movie_id = movie.get('id')
                movie_title = movie.get('title', 'Unknown')
                trailer_url = movie.get('trailer_url', '')
                
                if movie_id and trailer_url:
                    self.test_movie_trailer_endpoint(movie_id, movie_title)
                    tested_trailers += 1
                    
            if tested_trailers == 0:
                self.log_test("Movie Trailer Endpoints", False, "No movies with valid IDs and trailer URLs found for testing")
        else:
            self.log_test("Movie Trailer Endpoints", False, "Cannot test trailer endpoints - no movies available")
        
        # Test 4: Test invalid movie ID (should return 404)
        self.test_invalid_movie_trailer()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All curated movie tests passed!")
            return True
        else:
            failed_tests = [r for r in self.test_results if not r['success']]
            print(f"❌ {len(failed_tests)} tests failed:")
            for test in failed_tests:
                print(f"   - {test['test_name']}: {test['details']}")
            return False

def main():
    """Main test execution"""
    tester = CuratedMovieTester()
    
    try:
        success = tester.run_curated_movie_tests()
        
        # Save detailed results
        with open('/app/curated_movie_test_results.json', 'w') as f:
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