from datetime import datetime
from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_review import SeriesReviewId, SeriesReview
from amdb.domain.constants import ReviewType


class ReviewSeries(Service):
    @overload
    def __init__(
        self,
        *,
        auto_approve: Literal[True],
        approved_reviews_for_auto_approve: int,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        *,
        auto_approve: Literal[False],
        approved_reviews_for_auto_approve: None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        auto_approve: bool,
        approved_reviews_for_auto_approve: Optional[int],
    ) -> None:
        self._auto_approve = auto_approve
        self._approved_reviews_for_auto_approve = approved_reviews_for_auto_approve

    def __call__(
        self,
        *,
        series: Series,
        profile: Profile,
        id: SeriesReviewId,
        type: ReviewType,
        title: str,
        content: str,
        likes: int,
        dislikes: int,
        created_at: datetime,
    ) -> SeriesReview:
        profile.series_reviews += 1

        if (
            self._auto_approve
            and self._approved_reviews_for_auto_approve <= profile.series_reviews # type: ignore
        ):
            profile.approved_reviews += 1
            is_approved = True
        else:
            is_approved = False

        return SeriesReview(
            id=id,
            series_id=series.id,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=likes,
            dislikes=dislikes,
            is_approved=is_approved,
            created_at=created_at,
        )
