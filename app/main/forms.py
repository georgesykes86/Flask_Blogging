from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, Required
from wtforms import ValidationError
from ..models import Role, User

class EditProfileForm(FlaskForm):
    name = StringField('Full name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    username = StringField('Username', validators=[Required(), Length(1,64),
     Regexp('^[A-Za-z][A-Za-z0-9_.!@?]*$', 0, 'Usernames must have only letters, numbers or _ . ! @ ? ')])
    role = SelectField('Role', coerce=int)
    name = StringField('Full name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class PostForm(FlaskForm):
    content = TextAreaField('What\'s on your mind', validators=[Required()])
    submit = SubmitField('Post')
