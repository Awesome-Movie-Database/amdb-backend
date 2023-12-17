from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.relation import Relation
from amdb.domain.entities.person.marriage import Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_person import CreatePerson
from amdb.domain.services.person.update_person import UpdatePerson
from amdb.domain.services.person.create_relation import CreateRelation
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.application.commands.person.create_person import (
    RelationData,
    MarriageData,
    CreatePersonCommand,
)
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.gateways.person.relation import RelationGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_PERSON_ACCESS_DENIED,
    PERSONS_DO_NOT_EXIST,
    NO_HOMO,
)
from amdb.application.common.exception import ApplicationError


class CreatePersonHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        create_person: CreatePerson,
        update_person: UpdatePerson,
        create_relation: CreateRelation,
        create_marriage: CreateMarriage,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        marriage_gateway: MarriageGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._create_person = create_person
        self._update_person = update_person
        self._create_relation = create_relation
        self._create_marriage = create_marriage
        self._access_policy_gateway = access_policy_gateway
        self._person_gateway = person_gateway
        self._relation_gateway = relation_gateway
        self._marriage_gateway = marriage_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: CreatePersonCommand) -> PersonId:
        current_access_policy = self._identity_provider.get_access_policy()
        required_access_policy = self._access_policy_gateway.for_create_person()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(CREATE_PERSON_ACCESS_DENIED)

        current_timestamp = datetime.now(timezone.utc)

        person = self._create_person(
            id=PersonId(uuid4()),
            name=command.name,
            sex=command.sex,
            timestamp=current_timestamp,
            birth_date=command.birth_date,
            birth_place=command.birth_place,
            death_date=command.death_date,
            death_place=command.death_place,
        )
        self._person_gateway.save(
            person=person,
        )

        if command.relations_data:
            relations = self._create_relations(
                person=person,
                relations_data=command.relations_data,
                timestamp=current_timestamp,
            )
            self._relation_gateway.save_list(
                relations=relations,
            )
        if command.marriages_data:
            marriages = self._create_marriages(
                person=person,
                marriages_data=command.marriages_data,
                timestamp=current_timestamp,
            )
            self._marriage_gateway.save_list(
                marriages=marriages,
            )

        self._unit_of_work.commit()

        return person.id

    def _create_relations(
        self,
        *,
        person: Person,
        relations_data: list[RelationData],
        timestamp: datetime,
    ) -> list[Relation]:
        relatives = self._get_persons_with_ids(
            *(relation_data.person_id for relation_data in relations_data),
        )

        relations = []
        for relative, relation_data in zip(relatives, relations_data):
            relation = self._create_relation(
                person=person,
                relative=relative,
                type=relation_data.type,
                timestamp=timestamp,
            )
            relations.append(relation)

        self._person_gateway.update_list(
            persons=relatives,
        )

        return relations

    def _create_marriages(
        self,
        *,
        person: Person,
        marriages_data: list[MarriageData],
        timestamp: datetime,
    ) -> list[Marriage]:
        spouses = self._get_persons_with_ids(
            *(marriage_data.person_id for marriage_data in marriages_data),
        )

        marriages = []
        for spouse, marriage_data in zip(spouses, marriages_data):
            children = self._get_persons_with_ids(
                *(child_id for child_id in marriage_data.child_ids),
            )

            if person.sex is Sex.MALE and spouse.sex is Sex.FEMALE:
                husband = person
                wife = spouse
            elif person.sex is Sex.FEMALE and spouse.sex is Sex.MALE:
                husband = spouse
                wife = person
            else:
                raise ApplicationError(NO_HOMO)

            marriage = self._create_marriage(
                husband=husband,
                wife=wife,
                children=children,
                status=marriage_data.status,
                timestamp=timestamp,
                start_date=marriage_data.start_date,
                end_date=marriage_data.end_date,
            )
            marriages.append(marriage)

            self._person_gateway.update_list(
                persons=children,
            )

        self._person_gateway.update_list(
            persons=spouses,
        )

        return marriages

    def _get_persons_with_ids(
        self,
        *person_ids: PersonId,
    ) -> list[Person]:
        persons = self._person_gateway.list_with_ids(*person_ids)

        if len(person_ids) != len(persons):
            person_ids_from_gateway = [person.id for person in persons]

            invalid_person_ids = []
            for person_id in person_ids:
                if person_id in person_ids_from_gateway:
                    continue
                invalid_person_ids.append(person_id)

            raise ApplicationError(
                messsage=PERSONS_DO_NOT_EXIST,
                extra={"invalid_person_ids": invalid_person_ids},
            )

        return persons