"""
accounts.py

Mockup class that represent the casket's accounts.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"


import casket

class account:
    name = ''
    email = ''
    attributes = {}

    def __repr__(self):
        return "%s account(%s)" % (self.name, self.email)

    def __init__(self, name = 'default account', email = "user@example.com"):
        self.name = name
        self.email = email

    def set_password_safe(self, password):
        if not casket.password_validator.check_exist(password):
            if casket.password_validator.check_string(password):
                self.password = password
            else:
                raise not_valid_password_error
        else:
            if casket.settings.equal_password_allowed:
                self.password = password
            else:
                raise not_valid_password_error

    def set_password_any(self, password):
        self.password = password
