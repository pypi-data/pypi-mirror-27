from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import HueBaseObject
from .user import User


class BridgeConfig(HueBaseObject):
    def __init__(self, bridge, json):
        super(BridgeConfig, self).__init__(bridge, 'config', json)

    # Versions
    @property
    def api_version(self):
        return self._json['apiversion']

    @property
    def version(self):
        return self._json['swversion']

    @property
    def bridge_id(self):
        return self._json['bridgeid']

    # Network stuff
    @property
    def dhcp(self):
        return self._json['dhcp']

    @property
    def gateway(self):
        return self._json['gateway']

    @property
    def mac(self):
        return self._json['mac']

    @property
    def netmask(self):
        return self._json['netmask']

    @property
    def zigbeechannel(self):
        return self._json['zigbeechannel']

    @property
    def factorynew(self):
        return self._json['factorynew']

    @property
    def timezone(self):
        return self._json['timezone']

    @property
    def localtime(self):
        return self._json['localtime']

    @property
    def utc(self):
        return self._json['UTC']

    @property
    def users(self):
        u = []
        for k, v in self._json['whitelist'].items():
            u.append(User(username=k, json=v))
        return u

    def update_check(self):
        res = self._request(data={"swupdate": {"checkforupdate":True}})
        self.update()
        return res
