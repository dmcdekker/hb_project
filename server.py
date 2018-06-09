from pprint import pformat
import os
import requests
import json

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, configure_uploads, IMAGES

from model import connect_to_db, db, User, Language, LanguageMiddle
from model import Education, EducationMiddle, EngineeringType

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHERO_app"

app.jinja_env.undefined = StrictUndefined

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = 'https://www.eventbriteapi.com/v3/'


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

    new_user = User(fname=fname, lname=lname, email=email, password=password,
                    city=city, state=state)


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

    return render_template('add_profile.html', engineer_type=engineer_type, languages=languages)


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
        if get_active:
            user.is_active = True
        elif not get_active:
            user.is_active = False

        get_is_mentor = request.form['is_mentor']
        if get_is_mentor:
            user.is_mentor = True
        elif not get_is_mentor:
            user.is_mentor = False

        # Get form variables for education
        school_name = request.form['school_name']
        school_city = request.form['school_city']
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
        education = Education(school_name=school_name, school_city=school_city, school_state=school_state, degree_level=degree_level,
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
        return redirect('/login')

    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    user_id = session.get('user_id')
    path = str(user_id) + ".jpg"
    if request.method == 'POST' and 'photo' in request.files:
        request.files['photo'].filename = path
        filename = photos.save(request.files['photo'])
        user = User.query.get(user_id)
        user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
        db.session.commit()
        
    flash("Congrats, {}! You've successfully created your profile!".format(session['fname']))    
    return redirect("/profiles/{}".format(user.user_id))
    

@app.route('/edit-social.json', methods=['POST'])
def edit_social():
    """User can edit social media"""

    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        twitter = request.form.get('twitter')
        linkedin = request.form.get('linkedin')
        website_url = request.form.get('website_url')

        if twitter != '':
            user.twitter = twitter
        
        if linkedin != '':    
            user.linkedin = linkedin

        if website_url != '':    
            user.website_url = website_url

        db.session.commit()

        return jsonify(twitter, linkedin, website_url)

    else:
        flash("You can't edit other user's profiles")
        return redirect('/user_profile')        


@app.route('/edit-education.json', methods=['POST'])
def edit_education():
    """User can edit social education details"""

    user_id = session.get('user_id')

    if user_id:

        user = Education.query.get(user_id)

        school = request.form.get('school_name')
        year = request.form.get('year')
        school_city = request.form.get('school_city')
        school_state = request.form.get('school_state')
        degree = request.form.get('degree_level')
        major = request.form.get('major')

        if school != '':
            user.school_name = school
        
        if year != '':    
            user.year = year

        if school_city != '':    
            user.school_city = school_city

        if school_state != '':    
            user.school_state = school_state
        
        if degree != '':    
            user.degree_level = degree

        if major != '':    
            user.major = major           

        db.session.commit()

        return jsonify(school, year, school_city, school_state, degree, major )


@app.route('/edit-languages.json', methods=['POST'])
def edit_languages():
    """User can edit languages"""

    user_id = session.get('user_id')

    if user_id:

        user = User.query.get(user_id)

        languages = json.loads(request.form.get('language_name'))

        lang_json = ''
        
        for language_id in languages:
            if language_id == '':
                continue
            lang = Language.query.get(int(language_id))
            lang_json += lang.language_name
            db.session.add(LanguageMiddle(language=lang, user=user)) 
            db.session.commit()   

        return jsonify(lang_json)


@app.route('/edit-description.json', methods=['POST'])
def edit_description():
    """User can edit description"""

    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        description = request.form.get('description')
       
        if description != '':
            user.description = description

        db.session.commit()

        return jsonify(description)


@app.route('/edit-is_mentor.json', methods=['POST'])
def edit_mentor():
    """User can edit whether is mentor or mentee"""

    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        get_is_mentor = request.form['is_mentor']
        if get_is_mentor == 'True':
            user.is_mentor = True
        elif get_is_mentor == 'False':
            user.is_mentor = False
        
        db.session.commit()
        user2 = User.query.get(user_id)

        return jsonify(user.is_mentor)


@app.route('/edit-is_active.json', methods=['POST'])
def edit_active():
    """User can edit whether profile is active or not"""

    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        get_is_active = request.form['is_active']

        if get_is_active == 'True':
            user.is_active = True
        elif get_is_active == 'False':
            user.is_active = False
        
        db.session.commit()
        
        return jsonify(user.is_active)



@app.route('/profiles')
def user_list():
    """Show list of all profiles"""

    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in or register to view profiles")
        return redirect('/')

    users = User.query.all()

    engineer_types = EngineeringType.query.all()

    return render_template("profiles.html", users=users, engineer_types=engineer_types)



@app.route("/profiles/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)

    schools = Education.query.join(EducationMiddle).filter_by(user_id=user.user_id).all()

    user_languages = Language.query.join(LanguageMiddle).filter_by(user_id=user.user_id).all()

    all_languages = Language.query.all()

    return render_template("user_profile.html", user=user, schools=schools, user_languages=user_languages, all_languages=all_languages)

        
@app.route('/events')
def show_events():
    """Show events from Eventbite"""

    query = 'women+technology'
    location = 'san francisco'
    distance = '75mi'
    sort = 'date'
    category_id ='101,102'
    payload = {'q': query,
                'location.address': location,
                'location.within': distance,
                'categories': category_id,
                'sort_by': sort,}

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + 'events/search/',
                            params=payload,
                            headers=headers)

    data = response.json()

    if response.ok:
            events = data['events']

    else:
        flash("Nothing found: {}".format(data['error_description']))
        events = []        


    return render_template("events.html", data=pformat(data),
                               results=events)


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

    flash("You are now logged in")
    return redirect("/profiles/{}".format(user.user_id))


@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash('You are now logged out')

    return redirect('/')



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
