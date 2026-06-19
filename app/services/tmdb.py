import os
import httpx
from fastapi import HTTPException

from app.models import FilmGenre

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

TMDB_GENRE_MAP: dict[int, FilmGenre] = {
    28:    FilmGenre.ACTION,
    12:    FilmGenre.AVENTURE,
    35:    FilmGenre.COMEDIE,
    18:    FilmGenre.DRAME,
    27:    FilmGenre.HORREUR,
    878:   FilmGenre.SCIENCE_FICTION,
    53:    FilmGenre.THRILLER,
    16:    FilmGenre.ANIMATION,
    99:    FilmGenre.DOCUMENTAIRE,
    10749: FilmGenre.ROMANCE,
    14:    FilmGenre.FANTASTIQUE,
    80:    FilmGenre.POLICIER,
    36:    FilmGenre.HISTORIQUE,
    10402: FilmGenre.MUSICAL,
}


def _get_headers() -> dict:
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB_API_KEY not configured")
    return {"Authorization": f"Bearer {api_key}"}


def fetch_film_data(tmdb_id: int) -> dict:
    headers = _get_headers()

    with httpx.Client() as client:
        movie_resp = client.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}",
            headers=headers,
            params={"language": "EN"},
        )
        if movie_resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"TMDB movie {tmdb_id} not found")
        movie_resp.raise_for_status()
        movie = movie_resp.json()

        credits_resp = client.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}/credits",
            headers=headers,
        )
        credits_resp.raise_for_status()
        credits = credits_resp.json()

    director = next(
        (p["name"] for p in credits.get("crew", []) if p["job"] == "Director"),
        "Inconnu",
    )

    actors = ", ".join(
        p["name"] for p in credits.get("cast", [])[:5]
    )

    tmdb_genres = movie.get("genres", [])
    genre = next(
        (TMDB_GENRE_MAP[g["id"]] for g in tmdb_genres if g["id"] in TMDB_GENRE_MAP),
        FilmGenre.DRAME,
    )

    poster_url = None
    if movie.get("poster_path"):
        poster_url = f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"

    release_date = movie.get("release_date") or None

    return {
        "title": movie.get("title") or movie.get("original_title"),
        "director": director,
        "actors": actors or None,
        "min_duration": movie.get("runtime") or 0,
        "genre": genre,
        "language": movie.get("original_language"),
        "poster_url": poster_url,
        "release_date": release_date,
    }
