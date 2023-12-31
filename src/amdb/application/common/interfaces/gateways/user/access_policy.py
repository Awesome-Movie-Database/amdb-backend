from typing import Protocol

from amdb.domain.entities.user.access_policy import RequiredAccessPolicy


class AccessPolicyGateway(Protocol):
    def for_update_user(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_verify_user(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_create_person(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_update_person(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_create_marriage(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_update_marriage(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_delete_marriage(self) -> RequiredAccessPolicy:
        raise NotImplementedError

    def for_create_relation(self) -> RequiredAccessPolicy:
        raise NotImplementedError
