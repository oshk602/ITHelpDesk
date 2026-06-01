from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    submit = SubmitField('Register')

class LoginForm(FlaskForm):

    identifier = StringField(
        'Email or Username',
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Login')

    def validate_identifier(self, field):
        # Accept either a valid email or a username.
        value = (field.data or '').strip()

        # Email validator
        try:
            Email()(self, field)
            return
        except Exception:
            pass

        # Username validator (must match what registration accepts)
        if len(value) < 3 or len(value) > 20:
            raise ValueError('Username must be between 3 and 20 characters.')

