from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.application.common.view_models.non_detailed_movie import (
    NonDetailedMovieViewModel,
)
from amdb.application.queries.non_detailed_movies import (
    GetNonDetailedMoviesQuery,
)
from amdb.application.query_handlers.non_detailed_movies import (
    GetNonDetailedMoviesHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerMaker = CreateHandler[GetNonDetailedMoviesHandler]


@inject
async def get_non_detailed_movies(
    *,
    create_handler: Annotated[HandlerMaker, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[NonDetailedMovieViewModel]:
    """
    Returns list of non detailed movies and non detailed current
    user rating.
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    query = GetNonDetailedMoviesQuery(
        limit=limit,
        offset=offset,
    )

    return handler.execute(query)
