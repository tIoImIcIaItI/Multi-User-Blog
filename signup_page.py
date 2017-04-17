import re

from handler import Handler


# TODO: JSON endpoint to check for username availability in real-time

class SignupPage(Handler):

    def validate_form(self):

        # Extract the form input values
        username = self.request.get('username_input', '')
        password = self.request.get('password', '')
        verify = self.request.get('verify', '')
        email = self.request.get('email', '')

        username_error = None
        password_error = None
        verify_error = None
        email_error = None

        # Validate username availability and length
        user = self.users.get_by_username(username)
        if user:
            username_error = '%s is not available' % username
        else:
            if not username or len(username) < 2 or len(username) > 48:
                username_error = \
                    'A username between 2 and 48 characters is required'

        # Validate email format
        # SOURCE: https://www.scottbrady91.com/Email-Verification/Python
        # -Email-Verification-Script
        match = re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{'
            '2,4})$', email)
        if match is None:
            email_error = \
                'A valid email address is required'

        # Validate password requirements
        if not password or len(password) < 6 or len(password) > 32:
            password_error = \
                'A password between 6 and 32 characters is required'

        # Validate passwords match
        if password != verify:
            verify_error = \
                'Passwords do not match'

        is_valid = \
            username_error is None and \
            password_error is None and \
            verify_error is None and \
            email_error is None

        return \
            is_valid, \
            username, username_error, \
            password, password_error, \
            verify, verify_error, \
            email, email_error

    def get(self):
        self.sign_out()

        self.render(
            'signup.html',
            suppressSignup=True)

    def post(self):

        # Validate the form

        (is_valid,
         username, username_error,
         password, password_error,
         verify, verify_error,
         email, email_error) = \
            self.validate_form()

        if not is_valid:
            self.render(
                "signup.html",
                suppressSignup=True,
                username_input=username,
                email=email,
                username_error=username_error,
                password_error=password_error,
                verify_error=verify_error,
                email_error=email_error)
            return

        # Create the new account

        (created_account, username, pwd_hash, salt) = \
            self.create_account(username, password, email)

        if not created_account:
            self.error(500)
            return

        # Sign in the new user

        self.sign_in(username, pwd_hash, salt)

        self.redirect('/welcome')
