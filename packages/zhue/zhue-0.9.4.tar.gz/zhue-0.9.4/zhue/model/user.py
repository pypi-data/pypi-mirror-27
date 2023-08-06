from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import NamedHueJsonObject


class User(NamedHueJsonObject):
    def __init__(self, username, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username

    @property
    def hue_id(self):
        return self.username

    @property
    def last_used(self):
        return self._json['last use date']

    @property
    def creation_date(self):
        return self._json['create date']

    @property
    def ctime(self):
        '''
        ctime is a shortcut for creation_date
        '''
        return self.creation_date

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.name)
