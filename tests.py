import unittest

from server import app
from model import db, seed_data, connect_to_db, User

import server
import flask

from StringIO import StringIO  

connect_to_db(app)

# stop user editing other profiles
# cannot go to user add-profile if profile already created
# access to info when not logged in
# 89-134: Post method for add-profile
# 146-156: Upload method
# 163-280: .json methods
# 322-349: events
# 375-382: user password

  
class MockFlaskTests(unittest.TestCase):
    """Flask tests that show off mocking."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        seed_data()

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1

        # Make mock
        def _mock_state_to_code(event_name):
            return "<h1>Events</h1>"

        server.state_to_code = _mock_state_to_code

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        

    def test_find_user(self):
        """Can we find a user in the sample data?"""
        denise = User.query.filter(User.fname == "Denise").first()
        self.assertEqual(denise.fname, "Denise")

    
    def test_user_by_name(self):
        """Find profile in profile page"""
        result = self.client.get("/profiles?user_id=1")
        self.assertIn("Denise", result.data)

    # def test_events(self):
    #     """Test events api"""
    #     self.client.get('/events')
    #     self.assertIn('events', result.data)



class DBTests(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        app.config['SECRET_KEY'] = 'key'

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        seed_data()

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1

        
    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_homepage(self):
        """Homepage"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<div class="jumbotron jumbotron-fluid">', result.data)
    
    def test_register_get(self):
        result = self.client.get('/register', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Please register and move on to create your profile page</h3>', result.data)            

    def test_add_profile_get(self):
        result = self.client.get('/add-profile')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<form action="add-profile" method="POST">', result.data)

    # def test_add_profile_post(self):
    #     result = self.client.post('/add-profile', follow_redirects=False)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("<h1>Upload Your profile photo</h1>", result.data)     


    def test_user_profile(self):
        result = self.client.get("/profiles/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<div id='photo-and-social'>", result.data)

    def test_profiles_loggedin(self):
        result = self.client.get("/profiles", follow_redirects=False)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Profiles</h1>", result.data) 
        
    def test_logout_get(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('<div class="jumbotron jumbotron-fluid">' , result.data)

    def test_login_get(self):
        result = self.client.post("/login",
                                  data={"email": "dd@me.com",
                                        "password": "xxxxxx"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<div id='photo-and-social'>", result.data)        
    
    


class NoSessionServerTests(unittest.TestCase):
    """Tests for server.py when no session"""

    def setUp(self):
         # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        seed_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()   


    #uncommented as test is good (can't keep adding same data)
    def test_register_post(self):
        result = self.client.post('/register', follow_redirects=True,
                                    data={'fname': 'this',
                                          'lname': 'name',
                                          'user_name': 'you7',
                                          'email': 'me7@this.com',
                                          'password': 'test',
                                          'city': 'oakland',
                                          'state': 'CA'
                                          })
        self.assertIn('<form action="add-profile" method="POST">', result.data)

    #uncommented as test is good (can't keep adding same data)
    def test_add_profile_post(self):
        result = self.client.post('/add-profile', follow_redirects=True,
                                    data={'user.twitter': 'twitter',
                                          'user.linkedin': 'linkedin',
                                          'user.website_url': 'weburl',
                                          'user.description': 'description',
                                          'school_name': 'test',
                                          'school_city': 'test',
                                          'school_state': 'test',
                                          'degree_level': 'test',
                                          'major': 'test',
                                          'year': 'test',
                                          'get_langs': 'test',
                                          'is_active': 'True',
                                          'is_mentor': 'False'
                                          } )

        self.assertIn("<div id='photo-container'>", result.data)

#     # cannot get this test to pass
#     # def test_upload(self):
#     #     with open('static/images/denise_dekker.jpg', 'rb') as test:
#     #         testStringIO = StringIO(test.read())

#     #     result = self.client.post('/upload', 
#     #                                 content_type='multipart/form-data', follow_redirects=True, 
#     #                                 data={'photo': (testStringIO('test'), 'denise_dekker.jpg')})

#     #     self.assertEquals(result.status_code, 200)   


    def test_profiles_loggedout(self):
        result = self.client.get('/profiles', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Please log in or register to view profiles", result.data) 

    def test_login_get(self):
        result = self.client.get("/login", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Login</h1>", result.data)



    ##<<<<<<_________________to do_________________>>>>>>>>>>    


    
    # def test_profile_user(self):
    #     client = server.app.test_client()
    #     result = client.post('/profiles/<int:user_id>', data={'twitter': 'dmcdekker'})
    #     self.assertIn('Twitter:', result.data)

    # def test_edit_profile(self):
    #     client = server.app.test_client()
    #     result = self.client.get("/edit-social.json")
    #     return client.get('/user_profile', follow_redirects=True)

    # def login(self):
    #     client = server.app.test_client()
    #     return client.post('/login', data=dict(email=email,
    #                                            password=password), follow_redirects=True)

    # def logout(client):
    #     client = server.app.test_client()
    #     return client.get('/logout', follow_redirects=True)




        

    # def test_rsvp(self):
    #     result = self.client.post("/rsvp",
    #                               data={"name": "Jane",
    #                                     "email": "jane@jane.com"},
    #                               follow_redirects=True)
    #     self.assertNotIn("Please RSVP", result.data)
    #     self.assertIn("Party Details", result.data)


# class FlaskTests(unittest.TestCase):
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


#     def test_find_user(self):
#         """Can we find a user in the sample data?"""

#         denise = User.query.filter(Employee.name == "Denise").first()
#         self.assertEqual(denise.name, "Denise")  

#     # def test_games(self):
#     #     #FIXME: test that the games page displays the user info from seed_data()
#     #     result = self.client.get("/profiles")
#     #     self.assertIn("Denise Dekker", result.data)
        

if __name__ == "__main__":
    import unittest
    unittest.main()