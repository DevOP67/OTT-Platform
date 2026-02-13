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
        },
        {
            "id": 424,
            "title": "Schindler's List",
            "overview": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce.",
            "genre_ids": [18, 36, 10752],
            "release_date": "1993-12-15",
            "vote_average": 8.6,
            "poster_path": "/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
            "backdrop_path": "/loRmRzQXZeqG78TqZuyvSlEQfZb.jpg",
            "original_language": "en",
            "popularity": 82.3
        },
        {
            "id": 680,
            "title": "Pulp Fiction",
            "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            "genre_ids": [53, 80],
            "release_date": "1994-10-14",
            "vote_average": 8.5,
            "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "backdrop_path": "/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg",
            "original_language": "en",
            "popularity": 88.7
        },
        {
            "id": 389,
            "title": "12 Angry Men",
            "overview": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
            "genre_ids": [18],
            "release_date": "1957-04-10",
            "vote_average": 8.5,
            "poster_path": "/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg",
            "backdrop_path": "/qqHQsStV6exghCM7zbObuYBiYxw.jpg",
            "original_language": "en",
            "popularity": 75.4
        },
        {
            "id": 496243,
            "title": "Parasite",
            "overview": "All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood.",
            "genre_ids": [35, 53, 18],
            "release_date": "2019-05-30",
            "vote_average": 8.5,
            "poster_path": "/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
            "backdrop_path": "/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
            "original_language": "ko",
            "popularity": 91.2
        },
        {
            "id": 122,
            "title": "The Lord of the Rings: The Return of the King",
            "overview": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam.",
            "genre_ids": [12, 14, 28],
            "release_date": "2003-12-17",
            "vote_average": 8.5,
            "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
            "backdrop_path": "/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
            "original_language": "en",
            "popularity": 89.3
        },
        {
            "id": 429,
            "title": "The Good, the Bad and the Ugly",
            "overview": "A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold.",
            "genre_ids": [37],
            "release_date": "1966-12-23",
            "vote_average": 8.5,
            "poster_path": "/bX2xnavhMYjWDoZp1VM6VnU1xwe.jpg",
            "backdrop_path": "/Adrip2Jqzw56KeuV2nAxucKMNXA.jpg",
            "original_language": "it",
            "popularity": 78.6
        },
        {
            "id": 19404,
            "title": "Dilwale Dulhania Le Jayenge",
            "overview": "Raj is a rich, carefree, happy-go-lucky second generation NRI who meets Simran on a trip to Europe.",
            "genre_ids": [35, 18, 10749],
            "release_date": "1995-10-20",
            "vote_average": 8.7,
            "poster_path": "/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
            "backdrop_path": "/90ez6ArvpO8bvpyIngBuwXOqJm5.jpg",
            "original_language": "hi",
            "popularity": 65.4
        },
        {
            "id": 769,
            "title": "GoodFellas",
            "overview": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill.",
            "genre_ids": [18, 80],
            "release_date": "1990-09-19",
            "vote_average": 8.5,
            "poster_path": "/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
            "backdrop_path": "/hAPeXBdGDGmXRPj4OZZ0poH65Iu.jpg",
            "original_language": "en",
            "popularity": 84.2
        },
        {
            "id": 346,
            "title": "Seven Samurai",
            "overview": "A poor village under attack by bandits recruits seven unemployed samurai to help them defend themselves.",
            "genre_ids": [28, 18],
            "release_date": "1954-04-26",
            "vote_average": 8.5,
            "poster_path": "/8OKmBV5BUFzmozIC3pPWKHy17kx.jpg",
            "backdrop_path": "/sJNNMCc6B7KZIY3LH3JMYJJNH5j.jpg",
            "original_language": "ja",
            "popularity": 71.8
        },
        {
            "id": 372058,
            "title": "Your Name",
            "overview": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?",
            "genre_ids": [16, 18, 14],
            "release_date": "2016-08-26",
            "vote_average": 8.5,
            "poster_path": "/q719jXXEzOoYaps6babgKnONONX.jpg",
            "backdrop_path": "/7prYzufdIOy1KCTZKVWpjBFqqNr.jpg",
            "original_language": "ja",
            "popularity": 87.5
        },
        {
            "id": 539,
            "title": "Psycho",
            "overview": "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run, and checks into a remote motel.",
            "genre_ids": [27, 53],
            "release_date": "1960-09-08",
            "vote_average": 8.4,
            "poster_path": "/yz4QVqPx3h1hD1DfqqQkCq3rmxW.jpg",
            "backdrop_path": "/3MD5vQE0Tz5Hyj5i8Fg...BVO.jpg",
            "original_language": "en",
            "popularity": 76.3
        },
        {
            "id": 510,
            "title": "One Flew Over the Cuckoo's Nest",
            "overview": "A criminal pleads insanity and is admitted to a mental institution, where he rebels against the oppressive nurse.",
            "genre_ids": [18],
            "release_date": "1975-11-19",
            "vote_average": 8.4,
            "poster_path": "/2Sns5oJSTdT5pVdyGIOIxhj7MoC.jpg",
            "backdrop_path": "/6xGw9ZfVKVZITfm5iQJzW8JvC0e.jpg",
            "original_language": "en",
            "popularity": 79.1
        },
        {
            "id": 129,
            "title": "Spirited Away",
            "overview": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits.",
            "genre_ids": [16, 10751, 14],
            "release_date": "2001-07-20",
            "vote_average": 8.5,
            "poster_path": "/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
            "backdrop_path": "/Ab8mkHmkYADjU7wQiOkia9BzGvS.jpg",
            "original_language": "ja",
            "popularity": 93.7
        },
        {
            "id": 637,
            "title": "Life Is Beautiful",
            "overview": "A touching story of an Italian book seller of Jewish ancestry who lives in his own little fairy tale.",
            "genre_ids": [35, 18],
            "release_date": "1997-12-20",
            "vote_average": 8.4,
            "poster_path": "/74hLDKjD5aGYOotO6esUVaeISa2.jpg",
            "backdrop_path": "/bORe0eI72D874TMawAgpC6IPZto.jpg",
            "original_language": "it",
            "popularity": 77.2
        },
        {
            "id": 11216,
            "title": "Cinema Paradiso",
            "overview": "A filmmaker recalls his childhood, when he fell in love with the movies at his village's theater.",
            "genre_ids": [18, 10749],
            "release_date": "1988-11-17",
            "vote_average": 8.4,
            "poster_path": "/8SRUfRUi6x4O68n0VCbDNRa6iGL.jpg",
            "backdrop_path": "/gnqhEJTxQ...jpg",
            "original_language": "it",
            "popularity": 68.9
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
