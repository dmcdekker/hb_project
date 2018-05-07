"""Models and database functions for HB project."""

from flask_sqlalchemy import SQLAlchemy


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

        return "<User: {fname}\t{lname}\tEmail:{email}\t{loc}>"
                                                    .format(
                                                    fname=self.fname, lname=self.lname
                                                    email=self.email, loc=self.location)
                                                    

class Mentee(db.Model):

    __tablename__ = "mentees"

    mentee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    mentee = db.relationship("User", backref="mentees")

    return "<Mentee: {id}\t{user}>".format(id=mentee_id, user=user_id)


# class Mentor(db.model):

#     __tablename__ = "mentors"

#     mentor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = FK user_id

#     return "<Mentor: {id}\t{user}>".format(id=mentor_id, user=user_id)
    

class Relationship(db.Model):

     __tablename__ = "relationships"

    relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.mentee_id'))
    # mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.mentor_id'))
    # matched = db.Column(db.Boolean(1), nullable=False)

    mentee_rel = db.relationship("Mentee", backref="relationships")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Relationship: {rel}\t{mentee}\t{mentor}>".format(rel=self.relationship_id,
                                                                          mentee=mentee_id,
                                                                          mentor=mentor_id)


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
    state = db.Column(db.String(2), nullable=True)
    degree_level = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)
    date_graduated = db.Column(db.DateTime)

    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Education ID: {id}\n{name} {city} {state} {degree} {major} {date} >".format(id=self.education_id,
                                                                    name=self.school_name, 
                                                                    city=self.city,
                                                                    state=self.state,
                                                                    degree= self.degree_level,
                                                                    major=self.major
                                                                    date=self.date_graduated)


class EducationMiddle(db.Model):

     __tablename__ = "education_middles"

    ed_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    education_id = db.Column(db.Integer, db.ForeignKey('educations.education_id'), nullable=False)
    
    user = db.relationship("User", backref="education_middles")
    education = db.relationship("Education", backref="education_middles")


     def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Education Middle ID: {id}\t{ed_id}\t{user}>".format(id=self.ed_middle_id,
                                                                ed_id=self.education_id,
                                                                user=self.user_id)


class EngineeringCategory(db.Model):

     __tablename__ = "engineering_categories"

    engineer_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    engineer_type = db.Column(db.String(64), nullable=True)

    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Engineering Category ID: {id}\t{type}>".format(id=self.engineer_id, type=engineer_type)


class EngineeringCategoryMiddle(db.Model):

     __tablename__ = "eng_cat_middles"

    eng_middle_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    engineer_cat_id = db.Column(db.Integer, db.ForeignKey('engineeringcategories.engineer_cat_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship("User", backref="eng_cat_middles")
    engineering_category = db.relationship("EngineeringCategory", backref="eng_cat_middles")


     def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Engineering Middle ID: {id}\n{eng_id} {user}>".format(id=self.eng_middle_id,
                                                                ed_id=self.engineer_cat_id,
                                                                user=self.user_id)


#########################################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///animals'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()





