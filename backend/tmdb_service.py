import httpx
import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

async def fetch_popular_movies(page: int = 1) -> List[Dict[str, Any]]:
    """Fetch popular movies from TMDB"""
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not set, returning mock data")
        return get_mock_movies()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/movie/popular",
                params={"api_key": TMDB_API_KEY, "page": page}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            logger.error(f"Error fetching from TMDB: {e}")
            return get_mock_movies()

async def fetch_movie_genres() -> Dict[int, str]:
    """Fetch genre mapping from TMDB"""
    if not TMDB_API_KEY:
        return get_mock_genres()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/genre/movie/list",
                params={"api_key": TMDB_API_KEY}
            )
            response.raise_for_status()
            data = response.json()
            return {genre["id"]: genre["name"] for genre in data.get("genres", [])}
        except Exception as e:
            logger.error(f"Error fetching genres: {e}")
            return get_mock_genres()

async def search_movies(query: str, page: int = 1) -> List[Dict[str, Any]]:
    """Search movies by query"""
    if not TMDB_API_KEY:
        return get_mock_movies()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/search/movie",
                params={"api_key": TMDB_API_KEY, "query": query, "page": page}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            return get_mock_movies()

def transform_tmdb_movie(tmdb_movie: Dict[str, Any], genre_map: Dict[int, str]) -> Dict[str, Any]:
    """Transform TMDB movie to our format"""
    genres = [genre_map.get(gid, "Unknown") for gid in tmdb_movie.get("genre_ids", [])]
    
    return {
        "tmdb_id": tmdb_movie.get("id"),
        "title": tmdb_movie.get("title", "Unknown"),
        "overview": tmdb_movie.get("overview", ""),
        "genres": genres,
        "release_date": tmdb_movie.get("release_date", "2024-01-01"),
        "rating": tmdb_movie.get("vote_average", 0.0),
        "poster_url": f"{TMDB_IMAGE_BASE}{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get("poster_path") else "",
        "backdrop_url": f"{TMDB_IMAGE_BASE}{tmdb_movie.get('backdrop_path', '')}" if tmdb_movie.get("backdrop_path") else "",
        "runtime": 120,  # Default, would need another API call for exact
        "language": tmdb_movie.get("original_language", "en"),
        "popularity": tmdb_movie.get("popularity", 0.0),
    }

def get_mock_movies() -> List[Dict[str, Any]]:
    """Return mock movie data when TMDB is unavailable"""
    return [
        {
            "id": 550,
            "title": "Fight Club",
            "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club.",
            "genre_ids": [18, 53],
            "release_date": "1999-10-15",
            "vote_average": 8.4,
            "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
            "backdrop_path": "/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
            "original_language": "en",
            "popularity": 85.5
        },
        {
            "id": 13,
            "title": "Forrest Gump",
            "overview": "The story of several decades in the life of Forrest Gump, a slow-witted but kind-hearted man.",
            "genre_ids": [18, 10749],
            "release_date": "1994-07-06",
            "vote_average": 8.5,
            "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "backdrop_path": "/7c9UVPPiTPltouxRVY6N9udhf0y.jpg",
            "original_language": "en",
            "popularity": 90.2
        },
        {
            "id": 278,
            "title": "The Shawshank Redemption",
            "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption.",
            "genre_ids": [18, 80],
            "release_date": "1994-09-23",
            "vote_average": 8.7,
            "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "backdrop_path": "/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
            "original_language": "en",
            "popularity": 95.8
        },
        {
            "id": 238,
            "title": "The Godfather",
            "overview": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
            "genre_ids": [18, 80],
            "release_date": "1972-03-14",
            "vote_average": 8.7,
            "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "backdrop_path": "/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
            "original_language": "en",
            "popularity": 88.4
        },
        {
            "id": 155,
            "title": "The Dark Knight",
            "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and DA Harvey Dent.",
            "genre_ids": [28, 80, 18],
            "release_date": "2008-07-18",
            "vote_average": 8.5,
            "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "backdrop_path": "/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg",
            "original_language": "en",
            "popularity": 92.1
        }
    ]

def get_mock_genres() -> Dict[int, str]:
    """Return mock genre mapping"""
    return {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }
