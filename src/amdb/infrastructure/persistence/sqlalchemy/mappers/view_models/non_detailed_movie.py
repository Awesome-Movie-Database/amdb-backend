from typing import Optional

from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.application.common.view_models.non_detailed_movie import (
    MovieViewModel,
    UserRatingViewModel,
    NonDetailedMovieViewModel,
)


class NonDetailedMovieViewModelsMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def get(
        self,
        current_user_id: Optional[UserId],
        limit: int,
        offset: int,
    ) -> list[NonDetailedMovieViewModel]:
        statement = text(
            """
            SELECT
                m.id movie_id,
                m.title movie_title,
                m.release_date movie_release_date,
                m.rating movie_rating,
                urt.id user_rating_id,
                urt.value user_rating_value
            FROM
                movies m
            LEFT JOIN ratings urt
                ON urt.user_id = :current_user_id
            LIMIT :limit OFFSET :offset
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
            "limit": limit,
            "offset": offset,
        }
        rows = self._connection.execute(statement, parameters).fetchall()

        view_models = []
        for row in rows:
            row_as_dict = row._mapping  # noqa: SLF001

            movie = MovieViewModel(
                id=MovieId(row_as_dict["movie_id"]),
                title=row_as_dict["movie_title"],
                release_date=row_as_dict["movie_release_date"],
                rating=row_as_dict["movie_rating"],
            )

            rating_exists = row_as_dict["user_rating_id"] is not None
            if rating_exists:
                user_rating = UserRatingViewModel(
                    id=RatingId(row_as_dict["user_rating_id"]),
                    value=row_as_dict["user_rating_value"],
                )
            else:
                user_rating = None

            view_model = NonDetailedMovieViewModel(
                movie=movie,
                user_rating=user_rating,
            )
            view_models.append(view_model)

        return view_models
