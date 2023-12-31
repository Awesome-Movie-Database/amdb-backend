from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place


PersonId = NewType("PersonId", UUID)


@dataclass(slots=True)
class Person(Entity):
    id: PersonId
    name: str
    sex: Sex
    created_at: datetime

    birth_date: Optional[Date]
    birth_place: Optional[Place]
    death_date: Optional[Date]
    death_place: Optional[Place]
    updated_at: Optional[datetime]
