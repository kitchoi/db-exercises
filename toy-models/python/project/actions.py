
import contextlib

import sqlalchemy as sa
from sqlalchemy import create_engine
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


def populate_db(url, reset=False):
    engine = create_engine(url)
    if reset:
        orm.Base.metadata.drop_all(engine)

    orm.Base.metadata.create_all(engine)

    with engine.begin() as connection:
        # Many-to-many relationship between managers and venues
        eve = orm.Manager(name="Eve")
        adam = orm.Manager(name="Adam")

        garden = orm.Venue(name="Garden", managers=[eve])
        pool = orm.Venue(name="Pool Garden", managers=[adam])
        dinning_hall = orm.Venue(name="Dining Hall", managers=[adam])
        library = orm.Venue(name="Library", managers=[eve, adam])
        dancing_hall = orm.Venue(name="Dancing Hall", managers=[])

        instances = [
            # managers
            eve, adam,
            # venues
            garden, pool, dinning_hall, library, dancing_hall,
        ]
        with session_scope(connection) as session:
            session.add_all(instances)


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
