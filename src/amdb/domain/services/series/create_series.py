from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import SeriesId, SeriesTitle, Series
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


class CreateSeries(Service):
    def __call__(
        self,
        *,
        id: SeriesId,
        title: SeriesTitle,
        created_at: datetime,
        genres: list[Genre] = [],
        countries: list[str] = [],
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_vote_count: Optional[int] = None,
    ) -> Series:
        return Series(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
            genres=genres,
            countries=countries,
            created_at=created_at,
            runtime=None,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            description=description,
            summary=summary,
            budget=budget,
            mpaa=mpaa,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
            updated_at=None,
        )
