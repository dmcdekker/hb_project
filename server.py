"""Shero"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Language, LanguageMiddle 
from model import Education, EducationMiddle, EngineeringType

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHERO_app"

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
    city = request.form["city"]
    state = request.form["state"]
    user_name = request.form["user_name"]

    new_user = User(fname=fname, lname=lname, email=email, password=password,
                    city=city, state=state, user_name=user_name)


    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.user_id
    session['fname'] = new_user.fname

    return redirect('/add-profile')    


@app.route('/add-profile', methods=['GET'])
def profile_form():
    """Show form for user signup"""

    engineer_type = EngineeringType.query.all()

    languages = Language.query.all()

    return render_template('add-profile.html', engineer_type=engineer_type, languages=languages)


@app.route('/add-profile', methods=['POST'])
def profile_setup():
    """Process profile setup"""

    user_id = session.get('user_id')
    
    user = User.query.filter_by(user_id=user_id).first()


    if user_id:
        # update column values instead of creating new user
        user.twitter = request.form['twitter']
        user.linkedin = request.form['linkedin']
        user.website_url = request.form['website_url']
        user.description = request.form['description']
        user.engineer_type = request.form['engineer_type']     

        get_active = request.form['is_active']
        if get_active == 'True':
            user.is_active = True
        elif get_active == 'False':
            user.is_active = False

        get_is_mentor = request.form['is_mentor']
        if get_is_mentor == 'True':
            user.is_mentor = True
        elif get_is_mentor == 'False':
            user.is_mentor = False


        # Get form variables for education
        school_name = request.form['school_name']
        city = request.form['city']
        school_state = request.form['school_state']
        degree_level = request.form['degree_level']
        major = request.form['major']
        year = request.form['year']

        # Get form variables for languages
        languages = request.form.getlist('get_langs')
        for lang in languages:
            lang_id = LanguageMiddle(language_id=lang, user=user)
            db.session.add(lang_id)
            db.session.commit()

        # create new education object
        education = Education(school_name=school_name, city=city, school_state=school_state, degree_level=degree_level,
                              major=major, year=year)
        
        # create new education id object s
        ed_id = EducationMiddle(education=education, user=user)
      
        # create new mentee id and relationship object
        #mentee = Mentee(user=user)
        #relationship = Relationship(mentee=mentee)

        db.session.add_all([user, education, ed_id])
        db.session.commit()

    else:
        flash("No user logged in")   

    flash("Congrats, {}! You've successfully added your profile!".format(session['fname']))
    return redirect("/")


@app.route("/profiles")
def user_list():
    """Show list of all profiles"""

    users = User.query.all()

    engineer_types = EngineeringType.query.all()

    return render_template("profiles.html", users=users, engineer_types=engineer_types)


@app.route("/profiles/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)

    schools = Education.query.join(EducationMiddle).filter_by(user_id=user.user_id).all()

    languages = Language.query.join(LanguageMiddle).filter_by(user_id=user.user_id).all()

    return render_template("user_profile.html", user=user, schools=schools, languages=languages)



@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/profiles/{}".format(user.user_id))


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You are now logged Out")

    return redirect("/")


if __name__ == "__main__":

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    # disable intercept redirects
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    connect_to_db(app)

    app.run(host="0.0.0.0")

