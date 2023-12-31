from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_review import SeriesReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_review_vote import SeriesReviewVote
from amdb.domain.constants.common import VoteType
from amdb.domain.constants.exceptions import SERIES_REVIEW_NOT_APPROVED
from amdb.domain.exception import DomainError


class VoteSeriesReview(Service):
    def __call__(
        self,
        *,
        series_review: SeriesReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
        type: VoteType,
    ) -> SeriesReviewVote:
        if not series_review.is_approved:
            raise DomainError(SERIES_REVIEW_NOT_APPROVED)

        voter_profile.given_votes += 1
        reviewer_profile.gained_votes += 1

        if type is VoteType.LIKE:
            series_review.likes += 1
        elif type is VoteType.DISLIKE:
            series_review.dislikes += 1

        return SeriesReviewVote(
            series_review_id=series_review.id,
            user_id=voter_profile.user_id,
            type=type,
        )
