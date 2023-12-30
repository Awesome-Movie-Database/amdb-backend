from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class UnrateMovieCommand:
    movie_id: MovieId
