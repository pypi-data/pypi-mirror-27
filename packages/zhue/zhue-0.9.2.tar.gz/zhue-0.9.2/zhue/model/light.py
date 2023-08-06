from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import (LightDevice, LightDeviceState)


class Light(LightDevice):
    def __init__(self, bridge, hue_id, json):
        super(Light, self).__init__(bridge, 'lights', hue_id, json)

    @property
    def state(self):
        return LightDeviceState(self._json['state'])

    def delete(self):
        return self._bridge.delete_light(self.hue_id)

    def __str__(self):
        return '<Light: {}{}>'.format(self.name, ' (*)' if self.is_on else '')
