#for sign up of users
from flask.ext.login import AnonymousUserMixin

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = "Guest"

