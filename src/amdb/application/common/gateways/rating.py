from typing import Optional, Protocol

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId, Rating


class RatingGateway(Protocol):
    def with_id(self, rating_id: RatingId) -> Optional[Rating]:
        raise NotImplementedError

    def with_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[Rating]:
        raise NotImplementedError

    def save(self, rating: Rating) -> None:
        raise NotImplementedError

    def delete(self, rating: Rating) -> None:
        raise NotImplementedError

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        raise NotImplementedError
