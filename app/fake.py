from .models import User
from faker import Faker
from . import db
from sqlalchemy.exc import IntegrityError

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        user = User(email = fake.email(),
                 password = 'password',
                 username = fake.user_name(),
                 location = fake.city(),
                 about_me = fake.text(),
                 member_since = fake.past_date())
        db.session.add(user)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
