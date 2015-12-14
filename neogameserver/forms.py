from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import validators

from .models import User


class LoginForm(Form):
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.optional()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.objects(username=self.username.data)[0]
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # Do the passwords match
        if not User.check_password(user.password, self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class RegisterForm(Form):
    username = TextField(u"Username", validators=[validators.required()])
    password = PasswordField(u"Password", validators=[validators.required()])
    confirm = PasswordField(u"Confirm Password",
                            validators=[validators.required(),
                                        validators.EqualTo('password',
                                                           message="Passwords\
                                                           must match"
                                                           )
                                        ]
                            )
    email = TextField(u"Email", validators=[validators.required()])
