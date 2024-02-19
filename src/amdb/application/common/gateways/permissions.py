from typing import Protocol, Optional

from amdb.domain.entities.user import UserId


class PermissionsGateway(Protocol):
    def with_user_id(self, user_id: UserId) -> Optional[int]:
        raise NotImplementedError

    def set(self, user_id: UserId, permissions: int) -> None:
        raise NotImplementedError

    def for_new_user(self) -> int:
        raise NotImplementedError

    def for_login(self) -> int:
        raise NotImplementedError

    def for_get_movies(self) -> int:
        raise NotImplementedError

    def for_get_movie(self) -> int:
        raise NotImplementedError

    def for_create_movie(self) -> int:
        raise NotImplementedError

    def for_delete_movie(self) -> int:
        raise NotImplementedError

    def for_rate_movie(self) -> int:
        raise NotImplementedError

    def for_unrate_movie(self) -> int:
        raise NotImplementedError

    def for_get_reviews(self) -> int:
        raise NotImplementedError

    def for_review_movie(self) -> int:
        raise NotImplementedError