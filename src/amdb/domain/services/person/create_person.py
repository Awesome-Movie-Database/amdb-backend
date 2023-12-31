from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place
from amdb.domain.entities.person.person import PersonId, Person


class CreatePerson(Service):
    def __call__(
        self,
        *,
        id: PersonId,
        name: str,
        sex: Sex,
        timestamp: datetime,
        birth_date: Optional[Date] = None,
        birth_place: Optional[Place] = None,
        death_date: Optional[Date] = None,
        death_place: Optional[Place] = None,
    ) -> Person:
        return Person(
            id=id,
            name=name,
            sex=sex,
            created_at=timestamp,
            birth_date=birth_date,
            birth_place=birth_place,
            death_date=death_date,
            death_place=death_place,
            updated_at=None,
        )
