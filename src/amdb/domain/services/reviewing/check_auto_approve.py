from datetime import datetime, timedelta, timezone

from amdb.domain.services.base import Service
from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.profile import Profile


class CheckAutoApprove(Service):
    def __init__(
        self,
        *,
        days_from_creating: int,
        days_from_verification: int,
        approved_review_count: int,
    ) -> None:
        self._days_from_creating = days_from_creating
        self._days_from_verification = days_from_verification
        self._approved_review_count = approved_review_count

    def __call__(
        self,
        *,
        access_policy: AccessPolicy,
        profile: Profile,
    ) -> bool:
        return (
            access_policy.is_verified
            and datetime.now(timezone.utc) - access_policy.verified_at  # type: ignore
            >= timedelta(days=self._days_from_verification)
            and datetime.now(timezone.utc) - access_policy.created_at
            >= timedelta(days=self._days_from_creating)
            and profile.approved_reviews >= self._approved_review_count
        )
