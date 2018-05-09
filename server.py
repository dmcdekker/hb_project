"""Shero"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Keyword, Education, Engineer, EducationMiddle, EngineerMiddle, Keyword, KeyMiddle, Relationship, Mentee

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHERO_app"

# if an undefined variable is used in Jinja2; raise an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""
    return render_template('homepage.html')


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables for user
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form["email"]
    password = request.form["password"]
    location = request.form["location"]
    state = request.form["state"]
    twitter = request.form["twitter"]
    linkedin = request.form["linkedin"]
    website_url = request.form["website_url"]
    description = request.form["description"]

    # Get form variables for education
    school_name = request.form['school_name']
    city = request.form['city']
    school_state = request.form['school_state']
    degree_level = request.form['degree_level']
    major = request.form['major']
    year = request.form['year']

    # Get form variables for engineering type
    engineer_type = request.form['engineer_type']

    # Get form variables for keywords
    keyword = request.form['keyword']

    
    # create new user object
    new_user = User(fname=fname, lname=lname, email=email, password=password,
                  location=location, state=state, twitter=twitter, linkedin=linkedin, 
                  website_url=website_url, description=description)

    # create new education object
    education = Education(school_name=school_name, city=city, school_state=school_state, degree_level=degree_level,
                          major=major, year=year)
    
    # create new education id object
    ed_id = EducationMiddle(education=education, user=new_user)

    # create new engineering type
    engineer = Engineer(engineer_type=engineer_type)

    # create new engineer id object
    eng_id = EngineerMiddle(engineer=engineer, user=new_user)

    # create new keyword object
    keyword = Keyword(keyword=keyword)

    # create new keyword id object
    keyword_id = KeyMiddle(keyword=keyword, user=new_user)

    # create new mentee id and relationship object
    mentee = Mentee(user=new_user)
    relationship = Relationship(mentee=mentee)

    db.session.add_all([new_user, education, ed_id, engineer, eng_id, keyword, 
                    mentee, relationship, keyword_id])
    db.session.commit()

    flash("Congrats, {}! You've successfully added your profile!".format(fname))
    return redirect("/")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # disable intercept redirects
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

