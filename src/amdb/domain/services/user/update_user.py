from datetime import date, datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import User
from amdb.domain.constants.common import Unset, unset, Sex
from amdb.domain.value_objects import Place


class UpdateUser(Service):
    def __call__(
        self,
        *,
        user: User,
        timestamp: datetime,
        name: Union[str, Unset] = unset,
        password: Union[str, Unset] = unset,
        is_active: Union[bool, Unset] = unset,
        sex: Union[Sex, None, Unset] = unset,
        birth_date: Union[date, None, Unset] = unset,
        location: Union[Place, None, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=user,
            name=name,
            password=password,
            is_active=is_active,
            sex=sex,
            birth_date=birth_date,
            location=location,
            updated_at=timestamp,
        )
