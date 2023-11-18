from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class MovieScreenWriter(Entity):

    person_id: UUID
    movie_id: UUID
    created_at: datetime

    @classmethod
    def create(
        cls, person_id: UUID, movie_id: UUID,
        created_at: datetime
    ) -> "MovieScreenWriter":
        return MovieScreenWriter(
            person_id=person_id, movie_id=movie_id,
            created_at=created_at
        )