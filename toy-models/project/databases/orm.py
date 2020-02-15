import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    # note to self: recipe

    __tablename__ = "events"

    id = sa.Column(sa.Integer())

    name = sa.Column(sa.Text(), primary_key=True)

    venue = sa.Column(sa.Text(), sa.ForeignKey("venues.name"))

    hosts = sa.Column()

    start_time = sa.Column(sa.TIMESTAMP(timezone=True))


class Venue(Base):

    __tablename__ = "venues"

    name = sa.Column(sa.Text(), primary_key=True)

    managers = sa.Column(sa.Text(), sa.ForeignKey("managers.name"))

    events = sa.orm.relationship("Event")


class Manager(Base):

    __tablename__ = "managers"

    name = sa.Column(sa.Text(), primary_key=True)


class Person(Base):
    # note to self: material

    __tablename__ = "people"

    name = sa.Column(sa.Text(), primary_key=True)