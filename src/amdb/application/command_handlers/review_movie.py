from datetime import datetime, timezone
from typing import cast

from uuid_extensions import uuid7

from amdb.domain.entities.user import User
from amdb.domain.entities.review import ReviewId
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.review_movie import ReviewMovie
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    REVIEW_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_REVIEWED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.review_movie import ReviewMovieCommand


class ReviewMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        review_movie: ReviewMovie,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._review_movie = review_movie
        self._permissions_gateway = permissions_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._review_gateway = review_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: ReviewMovieCommand) -> ReviewId:
        current_permissions = self._identity_provider.permissions()
        required_permissions = self._permissions_gateway.for_review_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(REVIEW_MOVIE_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        current_user_id = self._identity_provider.user_id()

        review = self._review_gateway.with_movie_id_and_user_id(
            user_id=current_user_id,
            movie_id=movie.id,
        )
        if review:
            raise ApplicationError(MOVIE_ALREADY_REVIEWED)

        user = self._user_gateway.with_id(current_user_id)
        user = cast(User, user)

        new_review = self._review_movie(
            id=ReviewId(uuid7()),
            user=user,
            movie=movie,
            title=command.title,
            content=command.content,
            type=command.type,
            current_timestamp=datetime.now(timezone.utc),
        )
        self._review_gateway.save(new_review)

        self._unit_of_work.commit()

        return new_review.id
