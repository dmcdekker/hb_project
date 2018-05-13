import unittest

from server import app
from model import db, seed_data, connect_to_db


class MyTests(unittest.TestCase):
    """Tests for my mentoring site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("SHERO landing page", result.data)

    def test_register(self):
        # FIXME: Add a test to show we see the profile form
        result = self.client.get("/register")
        self.assertIn("Please register and move on to create your profile page", result.data)
        #self.assertNotIn("Party Details", result.data)    

    def test_profile(self):
        # FIXME: Add a test to show we see the profile form
        result = self.client.get("/profile")
        self.assertIn("Please complete to make your public profile", result.data)
        #self.assertNotIn("Party Details", result.data)

    # def test_rsvp(self):
    #     result = self.client.post("/rsvp",
    #                               data={"name": "Jane",
    #                                     "email": "jane@jane.com"},
    #                               follow_redirects=True)
    #     self.assertNotIn("Please RSVP", result.data)
    #     self.assertIn("Party Details", result.data)


# class PartyTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         with self.client as c:
#                 with c.session_transaction() as sess:
#                     sess['user_id'] = True

#         # Connect to test database (uncomment when testing database)
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data (uncomment when testing database)
#         db.create_all()
#         seed_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         # (uncomment when testing database)
#         db.session.close()
#         db.drop_all()

#     # def test_games(self):
#     #     #FIXME: test that the games page displays the user info from seed_data()
#     #     result = self.client.get("/profiles")
#     #     self.assertIn("Denise Dekker", result.data)
        

if __name__ == "__main__":
    unittest.main()