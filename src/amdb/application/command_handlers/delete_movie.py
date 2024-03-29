from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.delete_movie import DeleteMovieCommand


class DeleteMovieHandler:
    def __init__(
        self,
        *,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._review_gateway = review_gateway
        self._unit_of_work = unit_of_work

    def execute(self, command: DeleteMovieCommand) -> None:
        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        self._movie_gateway.delete(movie)
        self._rating_gateway.delete_with_movie_id(command.movie_id)
        self._review_gateway.delete_with_movie_id(command.movie_id)

        self._unit_of_work.commit()
