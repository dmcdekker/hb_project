
from model import User, Language, LanguageMiddle, Education, EducationMiddle, EngineeringType, connect_to_db, db
from server import app
from faker import Faker
from random import randint, choice

def seed_data():
    """Create example data for the test database."""

    engineering_types = ['Full Stack', 'Front End', 'Back End', 'Web', 'Mobile', 'Game', 'DevOps', 'CRM', 'Test', 'Embedded', 'Security', 'Infrastucture', 'Architect', 'Platform', 'Other']
    for name in engineering_types:
        add_type = EngineeringType(engineer_type=name)
        db.session.add(add_type)


    lang_list = open("lang_list.txt")    
    for name in lang_list:
        add_lang = Language(language_name=name)
        db.session.add(add_lang)


    user_1 = User(fname='Denise', lname='Dekker', email='dd@me.com', password='xxxxxx',
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

        user = User(fname=fake.first_name_female(), lname=fake.last_name(), email=fake.email(), password='test1',
                      city=fake.city(), state=fake.state_abbr(), twitter=fake.user_name(), linkedin=fake.user_name(), 
                      website_url=fake.url(), description=fake.paragraph(), 
                      engineer_type=randint(1, 15), is_active=True, is_mentor=choice([True, False]), photo='https://placeimg.com/640/480/any')

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

if __name__ == "__main__":
    # As a convenience, if we run this module interis_actively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB"

    fake = Faker()
    seed_data()
    fake_profiles(fake)
    
