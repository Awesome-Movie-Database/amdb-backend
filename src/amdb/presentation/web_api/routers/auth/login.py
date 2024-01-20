from typing import Annotated

from fastapi import Response, Depends
from pydantic import BaseModel

from amdb.domain.entities.user import UserId
from amdb.application.queries.login import LoginQuery
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


class LoginSchema(BaseModel):
    name: str
    password: str


async def login(
    ioc: Annotated[HandlerFactory, Depends()],
    session_processor: Annotated[SessionProcessor, Depends(Stub(SessionProcessor))],
    session_gateway: Annotated[RedisSessionGateway, Depends(Stub(RedisSessionGateway))],
    data: LoginSchema,
    response: Response,
) -> UserId:
    with ioc.login() as login_handler:
        login_query = LoginQuery(
            name=data.name,
            password=data.password,
        )
        user_id = login_handler.execute(login_query)

    session = session_processor.create(user_id=user_id)
    session_gateway.save(session)

    response.set_cookie(
        key=SESSION_ID_COOKIE,
        value=session.id,
        httponly=True,
    )

    return user_id
