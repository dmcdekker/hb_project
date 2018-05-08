"""Models and database functions for HB project."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask



db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(32), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    twitter = db.Column(db.String(32), nullable=True)
    linkedin = db.Column(db.String(32), nullable=True)
    website_url = db.Column(db.String(64), nullable=True)
    description = db.Column(db.Text, nullable=True)
    # photo = db.Column(db.String(64), nullable=True)
    # active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User: {fname}\t{lname}\tEmail:{email}\t{loc}>".format(fname=self.fname, lname=self.lname,
                                                                email=self.email, loc=self.location)
                                                    
                                                    

class Mentee(db.Model):

    __tablename__ = "mentees"

    mentee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User", backref="mentees")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Mentee: {id}\t{user}>".format(id=mentee_id, user=user_id)


# class Mentor(db.model):

#     __tablename__ = "mentors"

#     mentor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = FK user_id

#     return "<Mentor: {id}\t{user}>".format(id=mentor_id, user=user_id)
    

class Relationship(db.Model):

    __tablename__ = "relationships"

    relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentees.mentee_id'))

    mentee = db.relationship("Mentee", backref="relationships")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Relationship: {rel}\t{mentee}>".format(rel=self.relationship_id,
                                                        mentee=mentee_id)                                                                          


class Keyword(db.Model):

    __tablename__ = "keywords"
    
    keyword_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    keyword = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""


        return "<Keyword: {id} {keyword} >".format(id=self.keyword_id, keyword=self.keyword)


class KeyMiddle(db.Model):

    __tablename__ = 'key_middles'

    key_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.keyword_id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User", backref="key_middles")
    keyword = db.relationship("Keyword", backref="key_middles")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Key Middle ID: {id}\n{key_id} {user}>".format(id=self.key_middle_id,
                                                            key_id=self.keyword_id,
                                                            user=self.user_id)


class Education(db.Model):

    __tablename__ = "educations"
    
    education_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    school_state = db.Column(db.String(2), nullable=True)
    degree_level = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)
    year = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Education ID: {id}\n{name} {city} {state} {degree} {major} {date} >".format(id=self.education_id,
                                                                    name=self.school_name, 
                                                                    city=self.city,
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


class Engineer(db.Model):

    __tablename__ = "engineers"

    engineer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    engineer_type = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Engineering Category ID: {id}\t{type}>".format(id=self.engineer_id, type=engineer_type)


class EngineerMiddle(db.Model):

    __tablename__ = "eng_middles"

    eng_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    engineer_id = db.Column(db.Integer, db.ForeignKey('engineers.engineer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User", backref="eng_middles")
    engineer = db.relationship("Engineer", backref="eng_middles")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Engineering Middle ID: {id}\n{eng_id} {user}>".format(id=self.eng_middle_id,
                                                                eng_id=self.engineer_id,
                                                                user=self.user_id)


def seed_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a game and adds it to the database.

    user_1 = User(fname='Denise', lname='Dekker', email='dd@me.com', password='xxxxxx',
                  location='Oakland', state='CA', twitter='dmcdekker', linkedin='denise-m-dekker', 
                  website_url='dmdekker.io', description='Some long and lovely text about me')

    mentee = Mentee(user=user_1)
    relationship = Relationship(mentee=mentee)

    engineer = Engineer(engineer_type='Full Stack')
    eng_id = EngineerMiddle(engineer=engineer, user=user_1)
    
    keyword = Keyword(keyword='Python')
    keyword_id = KeyMiddle(keyword=keyword, user=user_1)

    education = Education(school_name='Mills College', city='Oakland', school_state='CA', degree_level='BA',
                  major='CS', year='2017')
    ed_id = EducationMiddle(education=education, user=user_1)

    db.session.add_all([user_1, engineer, eng_id, keyword, keyword_id, education, 
                        ed_id, mentee, relationship])
    db.session.commit()
    

#########################################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///shero'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()





