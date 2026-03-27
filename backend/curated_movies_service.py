"""
Curated Movie Database Service
This service provides a comprehensive collection of popular movies with:
- Real movie data (titles, descriptions, genres, ratings)
- High-quality poster images from public sources
- YouTube trailer URLs for in-app playback
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Curated movie database with real data and YouTube trailers
CURATED_MOVIES: List[Dict[str, Any]] = [
    # Action/Adventure Movies
    {
        "tmdb_id": 299536,
        "title": "Avengers: Infinity War",
        "overview": "As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos. A despot of intergalactic infamy, his goal is to collect all six Infinity Stones, artifacts of unimaginable power, and use them to inflict his twisted will on all of reality.",
        "genres": ["Action", "Adventure", "Science Fiction"],
        "release_date": "2018-04-25",
        "rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/bOGkgRGdhrBYJSLpXaxhXVstddV.jpg",
        "runtime": 149,
        "language": "en",
        "popularity": 98.5,
        "trailer_url": "https://www.youtube.com/watch?v=6ZfuNTqbHE8"
    },
    {
        "tmdb_id": 299534,
        "title": "Avengers: Endgame",
        "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "genres": ["Action", "Adventure", "Science Fiction"],
        "release_date": "2019-04-24",
        "rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg",
        "runtime": 181,
        "language": "en",
        "popularity": 99.2,
        "trailer_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c"
    },
    {
        "tmdb_id": 155,
        "title": "The Dark Knight",
        "overview": "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets. The partnership proves to be effective, but they soon find themselves prey to a reign of chaos unleashed by a rising criminal mastermind known to the terrified citizens of Gotham as the Joker.",
        "genres": ["Drama", "Action", "Crime", "Thriller"],
        "release_date": "2008-07-16",
        "rating": 9.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg",
        "runtime": 152,
        "language": "en",
        "popularity": 96.8,
        "trailer_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY"
    },
    {
        "tmdb_id": 27205,
        "title": "Inception",
        "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible: inception, the implantation of another person's idea into a target's subconscious.",
        "genres": ["Action", "Science Fiction", "Adventure"],
        "release_date": "2010-07-15",
        "rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/s3TBrRGB1iav7gFOCNx3H31MoES.jpg",
        "runtime": 148,
        "language": "en",
        "popularity": 95.4,
        "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0"
    },
    {
        "tmdb_id": 157336,
        "title": "Interstellar",
        "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        "genres": ["Adventure", "Drama", "Science Fiction"],
        "release_date": "2014-11-05",
        "rating": 8.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
        "runtime": 169,
        "language": "en",
        "popularity": 94.7,
        "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E"
    },
    # Drama Movies
    {
        "tmdb_id": 278,
        "title": "The Shawshank Redemption",
        "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an pointy warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates for his integrity and unquenchable sense of hope.",
        "genres": ["Drama", "Crime"],
        "release_date": "1994-09-23",
        "rating": 9.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
        "runtime": 142,
        "language": "en",
        "popularity": 97.5,
        "trailer_url": "https://www.youtube.com/watch?v=6hB3S9bIaco"
    },
    {
        "tmdb_id": 238,
        "title": "The Godfather",
        "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch Vito Corleone barely survives an attempt on his life, his youngest son Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.",
        "genres": ["Drama", "Crime"],
        "release_date": "1972-03-14",
        "rating": 9.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
        "runtime": 175,
        "language": "en",
        "popularity": 96.2,
        "trailer_url": "https://www.youtube.com/watch?v=sY1S34973zA"
    },
    {
        "tmdb_id": 550,
        "title": "Fight Club",
        "overview": "A ticking-Loss-Loss-Loss corporate box, the Narrator stumbles upon something that can cure his restlessness: an underground fight club. Founded by the charismatic Tyler Durden, this secret society offers a brutal form of therapy. The two men bond over bare-knuckle brawls and pranks, until things spiral dangerously out of control.",
        "genres": ["Drama", "Thriller"],
        "release_date": "1999-10-15",
        "rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLWE2ZWQtMjBlM2MyMWFkYjE5XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
        "runtime": 139,
        "language": "en",
        "popularity": 94.1,
        "trailer_url": "https://www.youtube.com/watch?v=SUXWAEX2jlg"
    },
    {
        "tmdb_id": 680,
        "title": "Pulp Fiction",
        "overview": "A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in this sprawling, comedic crime caper. Their adventures unfold in three stories that ingeniously trip back and forth in time.",
        "genres": ["Thriller", "Crime"],
        "release_date": "1994-09-10",
        "rating": 8.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg",
        "runtime": 154,
        "language": "en",
        "popularity": 93.8,
        "trailer_url": "https://www.youtube.com/watch?v=s7EdQ4FqbhY"
    },
    {
        "tmdb_id": 13,
        "title": "Forrest Gump",
        "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events—in each case, far exceeding what anyone imagined he could do. But despite all he has achieved, his one true love eludes him.",
        "genres": ["Comedy", "Drama", "Romance"],
        "release_date": "1994-07-06",
        "rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/7c9UVPPiTPltouxRVY6N9udhf0y.jpg",
        "runtime": 142,
        "language": "en",
        "popularity": 95.6,
        "trailer_url": "https://www.youtube.com/watch?v=bLvqoHBptjg"
    },
    # Sci-Fi Movies
    {
        "tmdb_id": 603,
        "title": "The Matrix",
        "overview": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
        "genres": ["Action", "Science Fiction"],
        "release_date": "1999-03-30",
        "rating": 8.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg",
        "runtime": 136,
        "language": "en",
        "popularity": 94.9,
        "trailer_url": "https://www.youtube.com/watch?v=vKQi3bBA1y8"
    },
    {
        "tmdb_id": 11,
        "title": "Star Wars: A New Hope",
        "overview": "Princess Leia is captured and held hostage by the evil Imperial forces in their effort to take over the galactic Empire. Venturesome Luke Skywalker and dashing captain Han Solo team together with the loveable robot duo R2-D2 and C-3PO to rescue the beautiful princess and restore peace and justice in the Empire.",
        "genres": ["Adventure", "Action", "Science Fiction"],
        "release_date": "1977-05-25",
        "rating": 8.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/zqkmTXzjkAgXmEWLRsY4UpTWCeo.jpg",
        "runtime": 121,
        "language": "en",
        "popularity": 93.2,
        "trailer_url": "https://www.youtube.com/watch?v=1g3_CFmnU7k"
    },
    {
        "tmdb_id": 329865,
        "title": "Arrival",
        "overview": "Taking place after alien crafts land around the world, an expert linguist is recruited by the military to determine whether they come in peace or are a threat.",
        "genres": ["Drama", "Science Fiction", "Mystery"],
        "release_date": "2016-11-10",
        "rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/yIZ1xendyqKvY3FGeeUYUd5X9Mm.jpg",
        "runtime": 116,
        "language": "en",
        "popularity": 88.4,
        "trailer_url": "https://www.youtube.com/watch?v=tFMo3UJ4B4g"
    },
    {
        "tmdb_id": 335984,
        "title": "Blade Runner 2049",
        "overview": "Thirty years after the events of the first film, a new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos. K's discovery leads him on a quest to find Rick Deckard, a former LAPD blade runner who has been missing for 30 years.",
        "genres": ["Science Fiction", "Drama"],
        "release_date": "2017-10-04",
        "rating": 7.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/sAtoMqDVhNDQBc3QJL3RF6hlhGq.jpg",
        "runtime": 164,
        "language": "en",
        "popularity": 87.6,
        "trailer_url": "https://www.youtube.com/watch?v=gCcx85zbxz4"
    },
    # Comedy Movies
    {
        "tmdb_id": 120467,
        "title": "The Grand Budapest Hotel",
        "overview": "The Grand Budapest Hotel tells of a legendary concierge at a famous European hotel between the wars and his friendship with a young employee who becomes his trusted protégé. The story involves the theft and recovery of a priceless Renaissance painting, the battle for an enormous family fortune, and the slow and then sudden upheavals that transformed Europe during the first half of the 20th century.",
        "genres": ["Comedy", "Drama"],
        "release_date": "2014-02-26",
        "rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/nX5XotM9yprCKarRH4fzOq1VM1J.jpg",
        "runtime": 99,
        "language": "en",
        "popularity": 89.3,
        "trailer_url": "https://www.youtube.com/watch?v=1Fg5iWmQjwk"
    },
    {
        "tmdb_id": 107,
        "title": "Snatch",
        "overview": "Unscrupulous boxing promoters, violent bookmakers, a Russian gangster, incompetent amateur robbers and supposedly Jewish jewelers fight to track down a priceless stolen diamond.",
        "genres": ["Thriller", "Crime", "Comedy"],
        "release_date": "2000-09-01",
        "rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTA2NDYxOGYtYjU1Mi00Y2QzLTgxMTQtMWI1MGI0ZGQ5MmU4XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/7SqMYPJTjZeKjjfSKFT0FzG6pCI.jpg",
        "runtime": 102,
        "language": "en",
        "popularity": 86.7,
        "trailer_url": "https://www.youtube.com/watch?v=ni4tEtuTccc"
    },
    # Thriller Movies
    {
        "tmdb_id": 745,
        "title": "The Sixth Sense",
        "overview": "Following an attack on his life, a child psychologist meets an eight year old boy who can see into the world of the dead.",
        "genres": ["Mystery", "Thriller", "Drama"],
        "release_date": "1999-08-06",
        "rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWM4NTFhYjctNzUyNi00NGMwLTk3NTYtMDIyNTZmMzRlYmQyXkEyXkFqcGdeQXVyMTAwMzUyOTc@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/lY0bCMLTLFKfBOM6Uq39r4PFXQ3.jpg",
        "runtime": 107,
        "language": "en",
        "popularity": 90.1,
        "trailer_url": "https://www.youtube.com/watch?v=VG9AGf66tXM"
    },
    {
        "tmdb_id": 694,
        "title": "The Shining",
        "overview": "Jack Torrance accepts a caretaker job at the Overlook Hotel, where he, along with his wife Wendy and their son Danny, must live isolated from the rest of the world for the winter. But they aren't prepared for the madness that lurks within.",
        "genres": ["Horror", "Thriller"],
        "release_date": "1980-05-23",
        "rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTg0YjQtYzY1ZGE3NTA5NGQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/mmd1HnuvAzFc4iuVJcnBrhDNEKr.jpg",
        "runtime": 144,
        "language": "en",
        "popularity": 91.5,
        "trailer_url": "https://www.youtube.com/watch?v=S014oGZiSdI"
    },
    {
        "tmdb_id": 807,
        "title": "Se7en",
        "overview": "Two homicide detectives are on a desperate hunt for a serial killer whose crimes are based on the seven deadly sins in this dark and haunting film that takes viewers from the opening credits to the last frame on a ride they will never forget.",
        "genres": ["Crime", "Mystery", "Thriller"],
        "release_date": "1995-09-22",
        "rating": 8.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
        "runtime": 127,
        "language": "en",
        "popularity": 92.3,
        "trailer_url": "https://www.youtube.com/watch?v=znmZoVkCjpI"
    },
    {
        "tmdb_id": 77,
        "title": "Memento",
        "overview": "Leonard Shelby is tracking down the man who raped and murdered his wife. The difficulty of locating his wife's killer, however, is compounded by the fact that he suffers from a rare, untreatable form of short-term memory loss. Although he can recall details of life before his accident, Leonard cannot remember what happened fifteen minutes ago, where he's going, or why.",
        "genres": ["Mystery", "Thriller"],
        "release_date": "2000-10-11",
        "rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZTcyNjk1MjgtOWI3Mi00YzQwLWI5MTktMzY4ZmI2NDAyNzYzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/9xAwAdD8FOLw0gVIXofWBKi46Y7.jpg",
        "runtime": 113,
        "language": "en",
        "popularity": 88.9,
        "trailer_url": "https://www.youtube.com/watch?v=4CV41hoyS8A"
    },
    # Animation Movies
    {
        "tmdb_id": 129,
        "title": "Spirited Away",
        "overview": "A young girl, Chihiro, becomes trapped in a strange new world of spirits. When her parents undergo a mysterious transformation, she must call upon the courage she never knew she had to free her family.",
        "genres": ["Animation", "Family", "Fantasy"],
        "release_date": "2001-07-20",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/Ab8mkHmkYADjU7wQiOkia9BzGvS.jpg",
        "runtime": 125,
        "language": "ja",
        "popularity": 94.3,
        "trailer_url": "https://www.youtube.com/watch?v=ByXuk9QqQkk"
    },
    {
        "tmdb_id": 862,
        "title": "Toy Story",
        "overview": "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.",
        "genres": ["Animation", "Adventure", "Family", "Comedy"],
        "release_date": "1995-10-30",
        "rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/Bo5PoWQ3XZET3WAGjllSptlVYgV.jpg",
        "runtime": 81,
        "language": "en",
        "popularity": 92.8,
        "trailer_url": "https://www.youtube.com/watch?v=v-PjgYDrg70"
    },
    {
        "tmdb_id": 508442,
        "title": "Soul",
        "overview": "Joe Gardner is a middle school teacher with a love for jazz music. After a successful audition at the Half Note Club, he suddenly gets into an accident that separates his soul from his body and is transported to the You Seminar, a center in which souls develop and gain passions before being transported to a newborn child.",
        "genres": ["Animation", "Comedy", "Drama", "Music", "Fantasy"],
        "release_date": "2020-12-25",
        "rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZGE1MDg5M2MtNTkyZS00MTY5LTg1YzUtZTlhZmM1Y2EwNmFmXkEyXkFqcGdeQXVyNjA3OTI0MDc@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/kf456ZqeC45XTvo6W9pW5clYKfQ.jpg",
        "runtime": 100,
        "language": "en",
        "popularity": 89.7,
        "trailer_url": "https://www.youtube.com/watch?v=xOsLIiBStEs"
    },
    # Horror Movies
    {
        "tmdb_id": 493922,
        "title": "Hereditary",
        "overview": "After the family matriarch passes away, a grieving family is haunted by tragic and disturbing occurrences, and begin to unravel dark secrets.",
        "genres": ["Horror", "Mystery", "Thriller"],
        "release_date": "2018-06-07",
        "rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTU5MDg3OGItZWQ1Ny00ZGVmLTg2YTUtMzBkYzQ1YWIwZjlhXkEyXkFqcGdeQXVyNTAzMTY4MDA@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/5GbkL1NFsAuHf5bx7bSKQOapKVa.jpg",
        "runtime": 127,
        "language": "en",
        "popularity": 85.2,
        "trailer_url": "https://www.youtube.com/watch?v=V6wWKNij_1M"
    },
    {
        "tmdb_id": 419430,
        "title": "Get Out",
        "overview": "Chris and his girlfriend Rose go upstate to visit her parents for the weekend. At first, Chris reads the family's overly accommodating behavior as nervous attempts to deal with their daughter's interracial relationship, but as the weekend progresses, a series of increasingly disturbing discoveries lead him to a truth that he never could have imagined.",
        "genres": ["Mystery", "Thriller", "Horror"],
        "release_date": "2017-02-24",
        "rating": 7.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/hUGTrAGPnQTII3nRvHWz7raSuVl.jpg",
        "runtime": 104,
        "language": "en",
        "popularity": 87.4,
        "trailer_url": "https://www.youtube.com/watch?v=DzfpyUB60YY"
    },
    # Romance/Drama
    {
        "tmdb_id": 597,
        "title": "Titanic",
        "overview": "101-year-old Rose DeWitt Bukater tells the story of her life aboard the Titanic, 84 years later. A young Rose boards the ship with her mother and fiancé. Meanwhile, Jack Dawson and Fabrizio De Rossi win third-class tickets aboard the ship. Rose tells the whole story from Titanic's departure through to its death—Loss-Loss-Loss-Loss-Loss-Loss-Loss-Loss-Loss-Loss-Loss-Loss to the \"Unsinkable Ship\".",
        "genres": ["Drama", "Romance"],
        "release_date": "1997-11-18",
        "rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/kHXEpyfl6zqn8a6YuozZUujufXf.jpg",
        "runtime": 194,
        "language": "en",
        "popularity": 93.1,
        "trailer_url": "https://www.youtube.com/watch?v=kVrqfYjkTdQ"
    },
    {
        "tmdb_id": 313369,
        "title": "La La Land",
        "overview": "Mia, an aspiring actress, serves lattes to movie stars in between auditions and Sebastian, a jazz musician, scrapes by playing cocktail party gigs in dingy bars, but as success mounts they are faced with decisions that begin to fray the fragile fabric of their love affair, and the dreams they worked so hard to maintain in each other threaten to rip them apart.",
        "genres": ["Comedy", "Drama", "Romance", "Music"],
        "release_date": "2016-11-29",
        "rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/bC6xZ4HqFD2wkPEJy6G2BvmGe3P.jpg",
        "runtime": 128,
        "language": "en",
        "popularity": 90.6,
        "trailer_url": "https://www.youtube.com/watch?v=0pdqf4P9MB8"
    },
    # Recent Blockbusters
    {
        "tmdb_id": 872585,
        "title": "Oppenheimer",
        "overview": "The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.",
        "genres": ["Drama", "History"],
        "release_date": "2023-07-19",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/rLb2cwF3Pazuxaj0sRXQ037tGI1.jpg",
        "runtime": 180,
        "language": "en",
        "popularity": 97.8,
        "trailer_url": "https://www.youtube.com/watch?v=uYPbbksJxIg"
    },
    {
        "tmdb_id": 346698,
        "title": "Barbie",
        "overview": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.",
        "genres": ["Comedy", "Adventure", "Fantasy"],
        "release_date": "2023-07-19",
        "rating": 7.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjU3N2QxNzYtMjk1NC00MTc4LTk1NTQtMmUxNTljM2I0NDA5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/nHf61UzkfFno5dHMZ5hJ7wVpFun.jpg",
        "runtime": 114,
        "language": "en",
        "popularity": 95.4,
        "trailer_url": "https://www.youtube.com/watch?v=pBk4NYhWNMM"
    },
    {
        "tmdb_id": 569094,
        "title": "Spider-Man: Across the Spider-Verse",
        "overview": "After reuniting with Gwen Stacy, Brooklyn's full-time, friendly neighborhood Spider-Man is catapulted across the Multiverse, where he encounters the Spider Society, a team of Spider-People charged with protecting the Multiverse's very existence.",
        "genres": ["Animation", "Action", "Adventure"],
        "release_date": "2023-05-31",
        "rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/4HodYYKEIsGOdinkGi2Ucz6X9i0.jpg",
        "runtime": 140,
        "language": "en",
        "popularity": 96.7,
        "trailer_url": "https://www.youtube.com/watch?v=cqGjhVJWtEg"
    },
    {
        "tmdb_id": 505642,
        "title": "Black Panther: Wakanda Forever",
        "overview": "Queen Ramonda, Shuri, M'Baku, Okoye and the Dora Milaje fight to protect their nation from intervening world powers in the wake of King T'Challa's death. As the Wakandans strive to embrace their next chapter, the heroes must band together with Nakia and Everett Ross to forge a new path for their beloved kingdom.",
        "genres": ["Action", "Adventure", "Science Fiction"],
        "release_date": "2022-11-09",
        "rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTM4NjIxNmEtYWE5NS00NDczLTkyNWQtYThhNmQyZGQzMjM0XkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/xDMIl84Qo5Tsu62c9DGWhmPI67A.jpg",
        "runtime": 161,
        "language": "en",
        "popularity": 91.2,
        "trailer_url": "https://www.youtube.com/watch?v=_Z3QKkl1WyM"
    },
    {
        "tmdb_id": 453395,
        "title": "Doctor Strange in the Multiverse of Madness",
        "overview": "Doctor Strange, with the help of mystical allies both old and new, traverses the mind-bending and dangerous alternate realities of the Multiverse to confront a mysterious new adversary.",
        "genres": ["Fantasy", "Action", "Adventure"],
        "release_date": "2022-05-04",
        "rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNWM0ZGJlMzMtZmYwMi00NzI3LTgzMzMtNjMzNjliNDRmZmFlXkEyXkFqcGdeQXVyMTM1MTE1NDMx._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/zInXopSvtKpd84fAkPe5jEvXBPH.jpg",
        "runtime": 126,
        "language": "en",
        "popularity": 90.8,
        "trailer_url": "https://www.youtube.com/watch?v=aWzlQ2N6qqg"
    },
    # International Films
    {
        "tmdb_id": 496243,
        "title": "Parasite",
        "overview": "All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood until they get entangled in an unexpected incident.",
        "genres": ["Comedy", "Thriller", "Drama"],
        "release_date": "2019-05-30",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
        "runtime": 132,
        "language": "ko",
        "popularity": 93.5,
        "trailer_url": "https://www.youtube.com/watch?v=5xH0HfJHsaY"
    },
    {
        "tmdb_id": 372058,
        "title": "Your Name",
        "overview": "High schoolers Mitsuha and Taki are complete strangers living separate lives. But one night, they suddenly switch places. Mitsuha wakes up in Taki's body, and he in hers. This bizarre occurrence continues to happen randomly, and the two must adjust their lives around each other.",
        "genres": ["Animation", "Romance", "Drama"],
        "release_date": "2016-08-26",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODRmZDVmNzUtZDA4ZC00NjhkLWI2M2UtN2M0ZDIzNDcxYThjL2ltYWdlXkEyXkFqcGdeQXVyNTk0MzMzODA@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/7prYzufdIOy1KCTZKVWpjBFqqNr.jpg",
        "runtime": 106,
        "language": "ja",
        "popularity": 91.8,
        "trailer_url": "https://www.youtube.com/watch?v=xU47nhruN-Q"
    },
    # Classic Films
    {
        "tmdb_id": 424,
        "title": "Schindler's List",
        "overview": "The true story of how businessman Oskar Schindler saved over a thousand Jewish lives from the Nazis while they worked as slaves in his factory during World War II.",
        "genres": ["Drama", "History", "War"],
        "release_date": "1993-12-15",
        "rating": 8.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/loRmRzQXZeqG78TqZuyvSlEQfZb.jpg",
        "runtime": 195,
        "language": "en",
        "popularity": 89.4,
        "trailer_url": "https://www.youtube.com/watch?v=gG22XNhtnoY"
    },
    {
        "tmdb_id": 389,
        "title": "12 Angry Men",
        "overview": "The defense and the prosecution have rested and the jury is filing into the jury room to decide if a young Spanish-American is guilty or innocent of murdering his father. What begins as an open and shut case soon becomes a mini-Loss-Loss-Loss-Loss-Loss-Loss as one juror asserts that the facts can be interpreted in more than one way.",
        "genres": ["Drama"],
        "release_date": "1957-04-10",
        "rating": 9.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/qqHQsStV6exghCM7zbObuYBiYxw.jpg",
        "runtime": 96,
        "language": "en",
        "popularity": 86.5,
        "trailer_url": "https://www.youtube.com/watch?v=TEN-2uTi2c0"
    },
    # More Action Movies
    {
        "tmdb_id": 245891,
        "title": "John Wick",
        "overview": "Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.",
        "genres": ["Action", "Thriller"],
        "release_date": "2014-10-22",
        "rating": 7.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/umC04Cozevu8nn3JTCM1GceWjpr.jpg",
        "runtime": 101,
        "language": "en",
        "popularity": 92.4,
        "trailer_url": "https://www.youtube.com/watch?v=2AUmvWm5ZDQ"
    },
    {
        "tmdb_id": 361743,
        "title": "Top Gun: Maverick",
        "overview": "After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him.",
        "genres": ["Action", "Drama"],
        "release_date": "2022-05-24",
        "rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWYzOGEwNTgtNWU3NS00ZTQ0LWJkODUtMmVhMjIwMjA1ZmQwXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/AaV1YIdWLJB0cAcB5evqWIDEonq.jpg",
        "runtime": 130,
        "language": "en",
        "popularity": 95.9,
        "trailer_url": "https://www.youtube.com/watch?v=giXco2jaZ_4"
    },
    {
        "tmdb_id": 76600,
        "title": "Avatar: The Way of Water",
        "overview": "Set more than a decade after the events of the first film, learn the story of the Sully family, the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
        "genres": ["Science Fiction", "Adventure", "Action"],
        "release_date": "2022-12-14",
        "rating": 7.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/s16H6tpK2utvwDtzZ8Qy4qm5Emw.jpg",
        "runtime": 192,
        "language": "en",
        "popularity": 94.6,
        "trailer_url": "https://www.youtube.com/watch?v=d9MyW72ELq0"
    },
    {
        "tmdb_id": 436270,
        "title": "Black Adam",
        "overview": "Nearly 5,000 years after he was bestowed with the almighty powers of the Egyptian gods—and imprisoned just as quickly—Black Adam is freed from his earthly tomb, ready to unleash his unique form of justice on the modern world.",
        "genres": ["Action", "Fantasy", "Science Fiction"],
        "release_date": "2022-10-19",
        "rating": 7.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzZkOGUwMzMtMTgyNS00YjFlLTg5NzYtZTE3Y2E5YTA5NWIyXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/bQXAqRx2Fgc46uCVWgoPz5L5Dtr.jpg",
        "runtime": 125,
        "language": "en",
        "popularity": 88.3,
        "trailer_url": "https://www.youtube.com/watch?v=X0tOpBuYasI"
    },
    # More Drama
    {
        "tmdb_id": 539,
        "title": "Psycho",
        "overview": "When larcenous real estate clerk Marion Crane goes on the lam with a wad of cash and hopes of starting a new life, she ends up at the notorious Bates Motel, where manager Norman Bates cares for his invalid mother.",
        "genres": ["Horror", "Drama", "Thriller"],
        "release_date": "1960-06-22",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTQwNDM1YzItNDAxZC00NWY2LTk0M2UtNDIwNWI5OGUyNWUxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/yz4QVqPx3h1hD1DfqqQkCq3rmxW.jpg",
        "runtime": 109,
        "language": "en",
        "popularity": 85.7,
        "trailer_url": "https://www.youtube.com/watch?v=DTJQfFQ40lI"
    },
    {
        "tmdb_id": 510,
        "title": "One Flew Over the Cuckoo's Nest",
        "overview": "While serving time for insanity at a state mental hospital, impertinent con man Randle Patrick McMurphy inspires his fellow patients to rebel against the authoritarian rule of head nurse Mildred Ratched.",
        "genres": ["Drama"],
        "release_date": "1975-11-19",
        "rating": 8.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjA0OWVhOTAtYWQxNi00YzNhLWI4ZjYtNjFjZTEyYjJlNDVlL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/6xGw9ZfVKVZITfm5iQJzW8JvC0e.jpg",
        "runtime": 133,
        "language": "en",
        "popularity": 87.9,
        "trailer_url": "https://www.youtube.com/watch?v=OXrcDonY-B8"
    },
    {
        "tmdb_id": 637,
        "title": "Life Is Beautiful",
        "overview": "A touching story of an Italian book seller of Jewish ancestry who lives in his own little fairy tale. His creative and joyous character helps Guido through hard times, even one of the most difficult circumstances possible: the Holocaust.",
        "genres": ["Comedy", "Drama"],
        "release_date": "1997-12-20",
        "rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmJmM2Q4NmMtYThmNC00ZjRlLWEyZmItZTIwOTBlZDQ3NTQ1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/bORe0eI72D874TMawAgpC6IPZto.jpg",
        "runtime": 116,
        "language": "it",
        "popularity": 86.2,
        "trailer_url": "https://www.youtube.com/watch?v=pAYEQP8gx3w"
    },
    # More Recent Films
    {
        "tmdb_id": 438631,
        "title": "Dune",
        "overview": "Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.",
        "genres": ["Science Fiction", "Adventure"],
        "release_date": "2021-09-15",
        "rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDQ0NjgyN2YtNWViNS00YjA3LTkxNDktYzFkZTExZGMxZDkxXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/jYEW5xZkZk2WTrdbMGAPFuBqbDc.jpg",
        "runtime": 155,
        "language": "en",
        "popularity": 94.1,
        "trailer_url": "https://www.youtube.com/watch?v=8g18jFHCLXk"
    },
    {
        "tmdb_id": 693134,
        "title": "Dune: Part Two",
        "overview": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.",
        "genres": ["Science Fiction", "Adventure"],
        "release_date": "2024-02-27",
        "rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2QyZGU4ZDctOWMzMy00NTc5LThlOGQtODhmNDI1NmY5YzAwXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
        "runtime": 166,
        "language": "en",
        "popularity": 97.2,
        "trailer_url": "https://www.youtube.com/watch?v=Way9Dexny3w"
    },
    {
        "tmdb_id": 1022789,
        "title": "Inside Out 2",
        "overview": "Teenager Riley's mind headquarters is undergoing a sudden demolition to make room for something entirely unexpected: new Emotions! Joy, Sadness, Anger, Fear and Disgust, who've long been running a successful operation by all accounts, aren't sure how to feel when Anxiety shows up.",
        "genres": ["Animation", "Family", "Adventure", "Comedy"],
        "release_date": "2024-06-11",
        "rating": 7.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTc1MDQ3NjAtOWEzMi00YzE1LWI2OWUtNjQ0OWJkMzI3MDhmXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/p5ozvmdgsmbWe0H8Xk7Rc8SCwAB.jpg",
        "runtime": 96,
        "language": "en",
        "popularity": 96.3,
        "trailer_url": "https://www.youtube.com/watch?v=LEjhY15eCx0"
    },
    {
        "tmdb_id": 823464,
        "title": "Godzilla x Kong: The New Empire",
        "overview": "Following their fruit-Fight fight against Mechagodzilla, Godzilla and Kong are now allies. But when an undiscovered threat hidden within our world emerges, they must embark on a journey together to defend the very existence of our species.",
        "genres": ["Action", "Adventure", "Science Fiction"],
        "release_date": "2024-03-27",
        "rating": 7.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY2QyNWVlZDMtNzYwOS00NWQ1LTk5MWMtZDJhNjE4ZjM4NDcyXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg",
        "backdrop_url": "https://image.tmdb.org/t/p/original/xRd1eJIDe7JHO5u4gtEYwGn5wtf.jpg",
        "runtime": 115,
        "language": "en",
        "popularity": 93.7,
        "trailer_url": "https://www.youtube.com/watch?v=lV1OOlGwExM"
    }
]

def get_all_curated_movies() -> List[Dict[str, Any]]:
    """Return all curated movies"""
    return CURATED_MOVIES

def get_movie_genres() -> Dict[int, str]:
    """Return genre mapping"""
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

def search_curated_movies(query: str) -> List[Dict[str, Any]]:
    """Search movies by title or overview"""
    query_lower = query.lower()
    results = []
    for movie in CURATED_MOVIES:
        if query_lower in movie["title"].lower() or query_lower in movie["overview"].lower():
            results.append(movie)
    return results

def get_movies_by_genre(genre: str) -> List[Dict[str, Any]]:
    """Get movies filtered by genre"""
    genre_lower = genre.lower()
    results = []
    for movie in CURATED_MOVIES:
        movie_genres = [g.lower() for g in movie.get("genres", [])]
        if genre_lower in movie_genres:
            results.append(movie)
    return results

def transform_curated_movie(movie: Dict[str, Any]) -> Dict[str, Any]:
    """Transform curated movie to our format"""
    return {
        "tmdb_id": movie.get("tmdb_id"),
        "title": movie.get("title", "Unknown"),
        "overview": movie.get("overview", ""),
        "genres": movie.get("genres", []),
        "release_date": movie.get("release_date", "2024-01-01"),
        "rating": movie.get("rating", 0.0),
        "poster_url": movie.get("poster_url", ""),
        "backdrop_url": movie.get("backdrop_url", ""),
        "runtime": movie.get("runtime", 120),
        "language": movie.get("language", "en"),
        "popularity": movie.get("popularity", 0.0),
        "trailer_url": movie.get("trailer_url", ""),
    }
