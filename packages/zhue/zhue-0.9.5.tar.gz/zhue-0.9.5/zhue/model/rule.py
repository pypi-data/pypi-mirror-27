from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import HueLLDevice


class Rule(HueLLDevice):
    def __init__(self, bridge, hue_id, json):
        super(Rule, self).__init__(bridge, 'rules', hue_id, json)

    @staticmethod
    def new(bridge, *args, **kwargs):
        raise NotImplementedError()

    @property
    def owner(self):
        return self._bridge.user(username=self._json['owner'])

    @property
    def lights(self):
        l = []
        for l_id in self._json['lights']:
            l.append(self._bridge.light(hue_id=l_id))
        return l

    @property
    def locked(self):
        return self._json['locked']

    @property
    def picture(self):
        return self._json['picture']

    @property
    def recycle(self):
        return self._json['recycle']

    @property
    def version(self):
        return self._json['version']

    @property
    def status(self):
        return self._json['status']

    @property
    def created(self):
        return self._json['created']

    @property
    def lasttriggered(self):
        return self._json['lasttriggered']

    @property
    def timestriggered(self):
        return self._json['timestriggered']

    @property
    def conditions(self):
        return self._json['conditions']

    @property
    def actions(self):
        return self._json['actions']
