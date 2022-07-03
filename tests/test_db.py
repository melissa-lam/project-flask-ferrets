

import unittest
from peewee import *
# from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Blind model classes to test db. Since we have a complete list of all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live for the duration fo the connection, and in the next step we close the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # create 2 timeline posts.
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello worldm I\'m John!")
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello worldm I\'m Jane!")
        assert second_post.id == 2
        # TODO: Get timeline posts and assert that they are correct

        posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        assert posts[1].name == "John Doe"
        assert posts[1].email == "john@example.com"
        assert posts[1].content == "Hello worldm I\'m John!"
        assert posts[0].name == "Jane Doe"
        assert posts[0].email == "jane@example.com"
        assert posts[0].content == "Hello worldm I\'m Jane!"


if __name__ == "__main__":
    unittest.main()
