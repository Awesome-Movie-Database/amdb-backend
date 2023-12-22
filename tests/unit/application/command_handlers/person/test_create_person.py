from unittest.mock import Mock
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import Person
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_person import CreatePerson
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import CREATE_PERSON_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_person import CreatePersonCommand
from amdb.application.command_handlers.person.create_person import CreatePersonHandler


def test_create_person(
    system_user_id: UserId,
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    person = person_factory.build()
    create_person: CreatePerson = Mock(
        return_value=person,
    )
    current_access_policy = AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    create_person_command = CreatePersonCommand(
        name=person.name,
        sex=person.sex,
        birth_date=person.birth_date,
        birth_place=person.birth_place,
        death_date=person.death_date,
        death_place=person.death_place,
    )
    creaate_person_handler = CreatePersonHandler(
        access_concern=AccessConcern(),
        create_person=create_person,
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    person_id = creaate_person_handler.execute(
        command=create_person_command,
    )

    assert person_id == person.id


def test_create_person_should_raise_error_when_access_is_denied(
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    person = person_factory.build()
    current_access_policy = AccessPolicy(
        id=UserId(uuid4()),
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    create_person_command = CreatePersonCommand(
        name=person.name,
        sex=person.sex,
        birth_date=person.birth_date,
        birth_place=person.birth_place,
        death_date=person.death_date,
        death_place=person.death_place,
    )
    creaate_person_handler = CreatePersonHandler(
        access_concern=AccessConcern(),
        create_person=CreatePerson(),
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        creaate_person_handler.execute(
            command=create_person_command,
        )

    assert error.value.messsage == CREATE_PERSON_ACCESS_DENIED
