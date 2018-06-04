"""Models and database functions for HB project."""
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from faker import Faker
from random import randint, choice

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    user_name = db.Column(db.String(64), nullable=True, unique=True)
    city = db.Column(db.String(32), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    twitter = db.Column(db.String(32), nullable=True)
    linkedin = db.Column(db.String(32), nullable=True)
    website_url = db.Column(db.String(64), nullable=True)
    description = db.Column(db.Text, nullable=True)
    engineer_type = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True)
    is_mentor = db.Column(db.Boolean, nullable=True)
    photo = db.Column(db.String(128), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""



        return "<User: {fname}\t{lname}\tEmail:{email}\t{city}>".format(fname=self.fname, lname=self.lname,
                                                                email=self.email, city=self.city)

                                                

# class Relationship(db.Model):

#     __tablename__ = "relationships"

#     relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     mentee_id = db.Column(db.Integer, db.ForeignKey('mentees.mentee_id'))
#     mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.mentor_id'))

#     mentee = db.relationship("Mentee", backref="relationships")
#     mentor = db.relationship("Mentor", backref="relationships")

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Relationship: {rel}\t{mentee}>".format(rel=self.relationship_id,
#                                                         mentee=mentee_id)                                                                          


class Language(db.Model):

    __tablename__ = "languages"
    
    language_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    language_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""


        return "<language: {id} {language} >".format(id=self.language_id, language=self.language_name)


class LanguageMiddle(db.Model):

    __tablename__ = 'lang_middles'

    lang_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.language_id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User", backref="lang_middles")
    language = db.relationship("Language", backref="lang_middles")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Lang Middle ID: {id}\n{lang_id} {user}>".format(id=self.lang_middle_id,
                                                            lang_id=self.language_id,
                                                            user=self.user_id)


class Education(db.Model):

    __tablename__ = "educations"
    
    education_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.String(64), nullable=True)
    school_city = db.Column(db.String(64), nullable=True)
    school_state = db.Column(db.String(2), nullable=True)
    degree_level = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)
    year = db.Column(db.String(64), nullable=True)
    
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Education ID: {id}\n{name} {city} {state} {degree} {major} {date} >".format(id=self.education_id,
                                                                    name=self.school_name,
                                                                    city=self.school_city,
                                                                    state=self.school_state,
                                                                    degree= self.degree_level,
                                                                    major=self.major,
                                                                    date=self.year)


class EducationMiddle(db.Model):

    __tablename__ = "education_middles"

    ed_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    education_id = db.Column(db.Integer, db.ForeignKey('educations.education_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User")
    education = db.relationship("Education", backref="education_middles")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Education Middle ID: {id}\t{ed_id}\t{user}>".format(id=self.ed_middle_id,
                                                                ed_id=self.education_id,
                                                                user=self.user_id)


class EngineeringType(db.Model):

    __tablename__ = "engineering_types"

    engineer_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    engineer_type = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Engineering Category ID: {id}\t{type}>".format(id=self.engineer_type_id, type=engineer_type)



def seed_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a game and adds it to the database.

    engineering_types = ['Full Stack', 'Front End', 'Back End', 'Web', 'Mobile', 'Game', 'DevOps', 'CRM', 'Test', 'Embedded', 'Security', 'Infrastucture', 'Architect', 'Platform', 'Other']
    for name in engineering_types:
        add_type = EngineeringType(engineer_type=name)
        db.session.add(add_type)


    lang_list = open("lang_list.txt")    
    for name in lang_list:
        add_lang = Language(language_name=name)
        db.session.add(add_lang)


    user_1 = User(fname='Denise', lname='Dekker', email='dd@me.com', user_name='dmcdekker', password='xxxxxx',
                  city='Oakland', state='CA', twitter='dmcdekker', linkedin='denise-m-dekker', 
                  website_url='dmdekker.io', description='Some long and lovely text about me', 
                  engineer_type=3, is_active=True, is_mentor=False, photo='/static/images/denise_dekker.jpg')


    #relationship = Relationship(mentee_id=user_1)
    
    language_id_1 = LanguageMiddle(language_id=3, user=user_1)
    language_id_2 = LanguageMiddle(language_id=6, user=user_1)
    language_id_3 = LanguageMiddle(language_id=10, user=user_1)
    language_id_3 = LanguageMiddle(language_id=16, user=user_1)
    language_id_3 = LanguageMiddle(language_id=8, user=user_1)

    education = Education(school_name='Mills College', school_city='Oakland', school_state='CA', degree_level='BA',
                  major='CS', year='2017')

    ed_id = EducationMiddle(education=education, user=user_1)


    db.session.add_all([user_1, language_id_1, language_id_2, language_id_3, education, ed_id])
    db.session.commit()

def fake_profiles(fake):
    """Create fake data"""

    for i in range(15):

        user = User(fname=fake.first_name_female(), lname=fake.last_name(), email=fake.email(), user_name=fake.user_name(), password='test1',
                      city=fake.city(), state=fake.state_abbr(), twitter=fake.user_name(), linkedin=fake.user_name(), 
                      website_url=fake.url(), description=fake.text(), 
                      engineer_type=randint(1, 16), is_active=True, is_mentor=choice([True, False]), photo='https://placeimg.com/640/480/any')

        education = Education(school_name=fake.name(), school_city=fake.city(), school_state=fake.state_abbr(), degree_level='BA',
                      major=fake.name(), year=fake.year())

        
        language_id_1 = LanguageMiddle(language_id=randint(1, 16), user=user)
        language_id_2 = LanguageMiddle(language_id=randint(1, 16), user=user)
        language_id_3 = LanguageMiddle(language_id=randint(1, 16), user=user)
        language_id_4 = LanguageMiddle(language_id=randint(1, 16), user=user)
        language_id_5 = LanguageMiddle(language_id=randint(1, 16), user=user)

        ed_id = EducationMiddle(education=education, user=user)

        db.session.add_all([user, language_id_1, language_id_2, language_id_3, language_id_4, language_id_5, education, ed_id])
        db.session.commit()


#########################################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///shero"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interis_actively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB"

    # fake = Faker()
    # db.create_all()
    # seed_data()
    # fake_profiles(fake)
    # print "DB populated"




