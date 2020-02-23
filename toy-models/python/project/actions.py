
import contextlib

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from project import orm


@contextlib.contextmanager
def session_scope(connectable):
    session = sessionmaker(bind=connectable)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def populate_db(engine, instances, reset=False):
    if reset:
        orm.Base.metadata.drop_all(engine)

    orm.Base.metadata.create_all(engine)

    with engine.begin() as connection:
        with session_scope(connection) as session:
            for instance in instances:
                session.add(instance)


def count_managers(engine):
    """ Return the number of managers."""
    with engine.begin() as conn, session_scope(conn) as session:
        return session.query(orm.Manager).count()


def get_manager_by_name(engine, name):
    """ Return a Manager for a given name."""
    with engine.begin() as conn, session_scope(conn) as session:
        manager = session.query(orm.Manager).filter(
            orm.Manager.name == name
        ).one()
        session.expunge(manager)
    return manager


def get_managers_by_venue(engine, venue_name):
    """ Return all managers for a given venue."""
    with engine.begin() as conn, session_scope(conn) as session:
        query = session.query(orm.Venue)\
            .options(sa.orm.joinedload(orm.Venue.managers))\
            .filter(orm.Venue.name == venue_name)
        try:
            venue = query.one()
        except sa.orm.exc.NoResultFound:
            raise ValueError(f"No venues found for name: {venue_name!r}")
        managers = venue.managers
        session.expunge_all()
    return managers


def get_manager_by_venue_like(engine, patterns):
    """ Return managers for venues with a name matching any of the given
    patterns.
    """
    with engine.begin() as conn, session_scope(conn) as session:
        managers = session.query(orm.Manager).filter(
            orm.Manager.venues.any(
                sa.or_(
                    orm.Venue.name.like(pattern)
                    for pattern in patterns
                )
            )
        ).all()
        session.expunge_all()
    return managers


def get_all_venue_names(engine):
    """ Return all venue names."""
    with engine.begin() as conn, session_scope(conn) as session:
        values = sorted(
            v for v, in session.query(orm.Venue.name).distinct().all()
        )
    return values


def get_venue_name_match_any(engine, patterns):
    """ Return the venue names that match any of the given patterns"""
    with engine.begin() as conn, session_scope(conn) as session:
        values = sorted(
            v for v, in session.query(orm.Venue.name).filter(
                sa.or_(
                    orm.Venue.name.like(pattern)
                    for pattern in patterns
                )
            ).all()
        )
    return values


def get_events_by_date_range(engine, start_date, end_date):
    """ Return events with a start time within the given date range."""
    with engine.begin() as conn, session_scope(conn) as session:
        events = session.query(orm.Event).filter(
            sa.and_(
                orm.Event.start_time >= start_date,
                orm.Event.start_time <= end_date,
            )
        ).all()
        session.expunge_all()
    return events


def get_events_in_venue(engine, venue_name):
    """ Return events hosted in a given venue. """
    with engine.begin() as conn, session_scope(conn) as session:
        events = session.query(orm.Event)\
                    .join(orm.Venue)\
                    .filter(orm.Venue.name == venue_name).all()
        session.expunge_all()
    return events
