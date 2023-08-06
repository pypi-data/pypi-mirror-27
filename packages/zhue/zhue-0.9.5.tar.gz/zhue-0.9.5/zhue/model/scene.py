# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import (BaseGroup)
from .group import (Group, MasterGroup)


class Scene(BaseGroup):
    def __init__(self, bridge, hue_id, json):
        super(Scene, self).__init__(bridge, 'scenes', hue_id, json)

    @property
    def owner(self):
        return self._bridge.user(username=self._json['owner'])

    @property
    def version(self):
        return self._json['version']

    @property
    def picture(self):
        return self._json['picture']

    @property
    def locked(self):
        return self._json['locked']

    @property
    def last_updated(self):
        return self._json['last_updated']

    @property
    def appdata(self):
        return self._json['appdata']

    @property
    def recycle(self):
        return self._json['recycle']

    def recall(self, target_group=None):
        if target_group is None:
            target_grp = MasterGroup(self._bridge)
        else:
            target_grp = target_group
        assert isinstance(target_grp, Group), \
            'Provided object is not a group'
        return target_grp.set_scene(self)
