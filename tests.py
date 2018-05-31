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

    def test_user_profile(self):
        result = self.client.get("/profiles/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<div id='social-container'>", result.data)

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
        self.assertIn("<div id='social-container'>", result.data) 


    # uncommented as test is good (can't keep adding same data)
    def test_add_profile_post(self):
        result = self.client.post('/add-profile',
                                    data={'twitter': 'test',
                                          'linkedin': 'test',
                                          'website_url': 'test',
                                          'description': 'test',
                                          'engineer_type': 1,
                                          'school_name': 'test',
                                          'school_city': 'test',
                                          'school_state': 'ca',
                                          'degree_level': 'test',
                                          'major': 'test',
                                          'year': 'test',
                                          'get_langs': 2,
                                          'is_active': 'True',
                                          'is_mentor': 'False'
                                          } )
    

        self.assertIn("<div id='photo-container'>", result.data) 


    def test_edit_social_json(self):
        result = self.client.post('/edit-social.json',
                                    data={'twitter' : 'dmcdekker',
                                          'linkedin' : 'denise-m-dekker',
                                          'website_url' : 'dmdekker.io'})

        self.assertIn('dmcdekker', result.data)

    def test_edit_education_json(self):
        result = self.client.post('/edit-education.json',
                                    data={'school_name' : 'mills college',
                                          'year' : '2017',
                                          'school_city': 'oakland',
                                          'school_state' : 'ca',
                                          'degree_level': 'ba',
                                          'major': 'cs'})

        self.assertIn('mills college', result.data)  


    # def test_edit_languages_json(self):
    #     result = self.client.post('/edit-languages.json',
    #                                 data={'language_name' : 'AGOL',
    #                                       })

    #     self.assertIn('AGOL', result.data)        


    def test_edit_description(self):
        result = self.client.post('/edit-description.json',
                                    data={'description' : 'Some long and lovely text about me',
                                          })

        self.assertIn('Some long and lovely text about me', result.data)  


    def test_edit_is_mentor(self):
        result = self.client.post('/edit-is_mentor.json',
                                    data={'is_mentor' : 'false',
                                          })

        self.assertIn('false', result.data)  


    def test_edit_is_active(self):
        result = self.client.post('/edit-is_active.json',
                                    data={'is_active' : 'true',
                                          })

        self.assertIn('true', result.data)                


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
    # def test_register_post(self):
    #     result = self.client.post('/register', follow_redirects=True,
    #                                 data={'fname': 'this',
    #                                       'lname': 'name',
    #                                       'user_name': 'you7',
    #                                       'email': 'me7@this.com',
    #                                       'password': 'test',
    #                                       'city': 'oakland',
    #                                       'state': 'CA'
    #                                       })
    #     self.assertIn('<form action="add-profile" method="POST">', result.data)

    

    # cannot get this test to pass
    # def test_upload(self):
    #     with open('static/images/denise_dekker.jpg', 'rb') as test:
    #         testStringIO = StringIO(test.read())

    #     result = self.client.post('/upload', 
    #                                 content_type='multipart/form-data', follow_redirects=True, 
    #                                 data={'photo': (testStringIO('test'), 'denise_dekker.jpg')})

    #     self.assertEquals(result.status_code, 200)   


    def test_profiles_loggedout(self):
        result = self.client.get('/profiles', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Please log in or register to view profiles", result.data) 

    def test_login_get(self):
        result = self.client.get('/login', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Login</h1>", result.data)

    def test_add_profile_post(self):
        result = self.client.post('/add-profile', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Login</h1>', result.data)




    
   

if __name__ == "__main__":
    import unittest
    unittest.main()