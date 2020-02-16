import datetime

from project import orm


def small_example():
    # Many-to-many relationship between managers and venues
    eve = orm.Manager(name="Eve")
    adam = orm.Manager(name="Adam")

    garden = orm.Venue(name="Garden", managers=[eve])
    pool = orm.Venue(name="Pool Garden", managers=[adam])
    dinning_hall = orm.Venue(name="Dining Hall", managers=[adam])
    library = orm.Venue(name="Library", managers=[eve, adam])
    dancing_hall = orm.Venue(name="Dancing Hall", managers=[])

    # Many-to-one relationship between events and venues
    wedding = orm.Event(
        name="C & T Wedding",
        venue=dinning_hall,
        start_time=datetime.datetime(2018, 2, 3, 18, 0),
    )
    conference = orm.Event(
        name="Medical conference",
        venue=library,
        start_time=datetime.datetime(2018, 9, 1, 9, 0),
    )
    comic_con = orm.Event(
        name="Comic Con",
        venue=garden,
        start_time=datetime.datetime(2018, 11, 2, 9, 0),
    )
    bible_study = orm.Event(
        name="Bible study",
        venue=library,
        start_time=datetime.datetime(2019, 3, 1, 9, 0),
    )

    return [
        # managers
        eve, adam,
        # venues
        garden, pool, dinning_hall, library, dancing_hall,
        # events
        wedding, conference, comic_con, bible_study,
    ]
