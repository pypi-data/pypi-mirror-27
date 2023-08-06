from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import (BaseGroup, LightDeviceState)


class Group(BaseGroup):
    def __init__(self, bridge, hue_id, json):
        super(Group, self).__init__(bridge, 'groups', hue_id, json)

    @property
    def name(self):
        if self._json:
            return super(Group, self).name
        elif self.hue_id == 0:
            return '# Master group'

    @property
    def state(self):
        return GroupState(
            dict(self._json['state'].items() + self._json['action'].items())
        )

    @property
    def all_on(self):
        return self.state.all_on

    @property
    def any_on(self):
        return self.state.any_on

    def _set_state(self, data):
        # Groups have a different endpoint for the "state" (/action)
        url = '{}/action'.format(self.API)
        res = self._request(
            method='PUT',
            url=url,
            data=data
        )
        self.update()
        return res

    def set_scene(self, scene):
        return self._set_state({'scene': scene.hue_id})


class GroupState(LightDeviceState):
    @property
    def all_on(self):
        return self._json['all_on']

    @property
    def any_on(self):
        return self._json['any_on']


class MasterGroup(Group):
    def __init__(self, bridge):
        super(MasterGroup, self).__init__(bridge=bridge, hue_id=0, json=None)

    @property
    def lights(self):
        return self._bridge.ligths
