import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table

Base = declarative_base()

# Many-to-One relationship between events and venues


class Event(Base):

    __tablename__ = "events"

    id = sa.Column(sa.Integer())

    name = sa.Column(sa.Text(), primary_key=True)

    venue = sa.Column(sa.Text(), sa.ForeignKey("venues.name"))

    start_time = sa.Column(sa.TIMESTAMP(timezone=True))


# Many-to-many relationship between managers and venues
manager_venue_table = Table(
    "manager_venue",
    Base.metadata,
    sa.Column("manager_name", sa.Text, sa.ForeignKey("managers.name")),
    sa.Column("venue_name", sa.Text, sa.ForeignKey("venues.name")),
)


class Venue(Base):

    __tablename__ = "venues"

    name = sa.Column(sa.Text(), primary_key=True)

    managers = sa.orm.relationship(
        "Manager",
        secondary=manager_venue_table,
        back_populates="venues",
    )

    events = sa.orm.relationship("Event")


class Manager(Base):

    __tablename__ = "managers"

    name = sa.Column(sa.Text(), primary_key=True)

    venues = sa.orm.relationship(
        "Venue",
        secondary=manager_venue_table,
        back_populates="managers",
    )


class Person(Base):
    # note to self: material

    __tablename__ = "people"

    name = sa.Column(sa.Text(), primary_key=True)
