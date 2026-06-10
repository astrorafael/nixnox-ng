# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import logging

from datetime import datetime
from typing import Optional, Any

# ---------------------
# Third party libraries
# ---------------------
from sqlalchemy import select, asc, label
from sqlalchemy.orm import aliased

from nixnox_dao import ValidState
from nixnox_dao.nixnox.noasync import Person, Organization

# -----------------------
# Module global variables
# -----------------------

# get the root logger
log = logging.getLogger(__name__.split(".")[-1])


def persons_lookup(session):
    """Person summary search with several constratints"""
    # Alias is needed to perform a table join on itself
    OrgAlias = aliased(Organization)
    q1 = (
        select(
            Person.observer_id.label("id"),
            Person.name,
            Person.nickname,
            OrgAlias.name.label("affiliation"),
            Person.valid_state,
            Person.valid_since,
            Person.valid_until,
        )
        .select_from(Person)
        .join(OrgAlias, Person.affiliation_id == OrgAlias.observer_id)
        .order_by(asc(Person.name), asc(Person.valid_since))
    )
    q2 = (
        select(
            Person.observer_id,
            Person.name,
            Person.nickname,
            label("affiliation", None),
            Person.valid_state,
            Person.valid_since,
            Person.valid_until,
        )
        .where(Person.affiliation_id == None)  # noqa: E711
        .order_by(asc(Person.name), asc(Person.valid_since))
    )
    # make the union at the result set point
    # because return q1.union(q2) yields an SQLOperational Error
    return session.execute(q1).all() + session.execute(q2).all()
    # return session.execute(q1.union(q2)).all()


def person_affiliation(session: Any, observer_id: int) -> Optional[str]:
    q = select(Person).where(Person.observer_id == observer_id)
    person = session.scalars(q).one_or_none()
    if not person or not person.affiliation:
        return None
    return person.affiliation.name


def person_delete(session: Any, observer_id: int) -> None:
    with session.begin():
        q = select(Person).where(Person.observer_id == observer_id)
        person = session.scalars(q).one_or_none()
        if person:
            session.delete(person)


def person_clone(
    session,
    name: str,
    nickname: str,
    affiliation: str,
    valid_since: datetime,
    valid_until: datetime,
    valid_state: ValidState,
) -> None:
    with session.begin():
        qo = select(Organization.observer_id).where(Organization.name == affiliation)
        affiliation_id = session.scalars(qo).one_or_none()
        person = Person(
            name=name,
            nickname=nickname,
            affiliation_id=affiliation_id,
            valid_since=valid_since,
            valid_until=valid_until,
            valid_state=ValidState.CURRENT,
        )
        session.add(person)


def person_update(
    session,
    observer_id: int,
    name: str,
    nickname: str,
    affiliation: str,
    valid_since: datetime,
    valid_until: datetime,
    valid_state: ValidState,
) -> None:
    with session.begin():
        qp = select(Person).where(Person.observer_id == observer_id)
        qo = select(Organization).where(Organization.name == affiliation)
        org = session.scalars(qo).one_or_none()
        person = session.scalars(qp).one_or_none()
        # new person ?
        if not person:
            person = Person(
                name=name,
                nickname=nickname,
                valid_since=valid_since,
                valid_until=valid_until,
                valid_state=valid_state,
            )
        else:
            person.nickname = nickname
            person.affiliation = org
            person.valid_since = valid_since
            person.valid_until = valid_until
            person.valid_state = valid_state
        if org:
            person.affiliation = org
        session.add(person)


def orgs_names_lookup(session):
    q = select(Organization.name).order_by(asc(Organization.name))
    return session.scalars(q).all()


def orgs_lookup(session):
    q = select(
        Organization.name,
        Organization.org_acronym,
        Organization.org_website_url,
        Organization.org_email,
    ).order_by(asc(Organization.name))
    return session.execute(q).all()


def org_update(
    session: Any, name: str, org_acronym: str, org_website_url: str, org_email: str
) -> None:
    with session.begin():
        q = select(Organization).where(Organization.name == name)
        organization = session.scalars(q).one_or_none()
        log.info("ORGANIZATION %s", organization)
        if organization:
            organization.org_acronym = org_acronym
            organization.org_website_url = org_website_url
            organization.org_email = org_email
            log.info("YA EXISTE Y LA MODIFICAMOS A %s", organization)
        else:
            organization = Organization(
                name=name,
                org_acronym=org_acronym,
                org_website_url=org_website_url,
                org_email=org_email,
            )
        session.add(organization)


def org_delete(session: Any, name: str) -> None:
    with session.begin():
        q = select(Organization).where(Organization.name == name)
        organization = session.scalars(q).one_or_none()
        if organization:
            session.delete(organization)
