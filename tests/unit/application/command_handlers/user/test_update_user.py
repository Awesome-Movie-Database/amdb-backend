import pytest
from unittest.mock import Mock

from amdb.domain.entities.user.access_policy import AccessPolicyWithIdentity, RequiredAccessPolicy
from amdb.domain.entities.user.user import User
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.update_user import UpdateUser
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.user.update_user import UpdateUserCommand
from amdb.application.command_handlers.user.update_user import UpdateUserHandler
from amdb.application.common.constants.exceptions import UPDATE_USER_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


NEW_USER_NAME = "JohnDoe2"


@pytest.fixture(scope="module")
def required_access_policy() -> RequiredAccessPolicy:
    return RequiredAccessPolicy(
        is_active=True,
        is_verified=False,
        id=None,
    )


def test_update_user(
    user: User,
    required_access_policy: RequiredAccessPolicy,
    access_concern: AccessConcern,
    update_user: UpdateUser,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicyWithIdentity(
        is_active=True,
        is_verified=False,
        id=user.id,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    access_policy_gateway.for_update_user = Mock(
        return_value=required_access_policy,
    )
    user_gateway.with_id = Mock(
        return_value=user,
    )

    update_user_command = UpdateUserCommand(
        name=NEW_USER_NAME,
    )
    update_user_handler = UpdateUserHandler(
        access_concern=access_concern,
        update_user=update_user,
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    update_user_handler.execute(
        command=update_user_command,
    )


def test_update_user_raises_error_when_user_does_not_have_access(
    user: User,
    required_access_policy: RequiredAccessPolicy,
    access_concern: AccessConcern,
    update_user: UpdateUser,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicyWithIdentity(
        is_active=False,
        is_verified=False,
        id=user.id,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    access_policy_gateway.for_update_user = Mock(
        return_value=required_access_policy,
    )
    user_gateway.with_id = Mock(
        return_value=user,
    )

    update_user_command = UpdateUserCommand(
        name=NEW_USER_NAME,
    )
    update_user_handler = UpdateUserHandler(
        access_concern=access_concern,
        update_user=update_user,
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        update_user_handler.execute(
            command=update_user_command,
        )
    assert error.value.messsage == UPDATE_USER_ACCESS_DENIED
