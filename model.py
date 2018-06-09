"""Models and database functions for HB project."""
from flask import Flask

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
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


