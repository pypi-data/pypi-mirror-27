from __future__ import unicode_literals
from __future__ import print_function
import re


uuid_mac_regex = re.compile(
    r'(([0-9a-f]{2}[:-]){6}([0-9a-f]{2})):(.+)'
)


class HueJsonObject(object):
    def __init__(self, json):
        self._json = json


class NamedHueJsonObject(HueJsonObject):
    @property
    def name(self):
        return self._json['name']


class HueBaseObject(HueJsonObject):
    def __init__(self, bridge, api_endpoint, json):
        super(HueBaseObject, self).__init__(json)
        self._bridge = bridge
        self.api_endpoint = api_endpoint
        self.API = '{}/{}'.format(
            self._bridge.API,
            self.api_endpoint
        )

    # Shortcut function
    def _request(self, *args, **kwargs):
        if 'url' not in kwargs:
            return self._bridge._request(url=self.API, *args, **kwargs)
        return self._bridge._request(*args, **kwargs)

    def update(self):
        '''
        Update our object's data
        '''
        self._json = self._request(
            method='GET',
            url=self.API
        )._json


class HueObject(HueBaseObject):
    def __init__(self, bridge, api_endpoint, hue_id, json):
        super(HueObject, self).__init__(bridge, api_endpoint, json)
        self.hue_id = hue_id
        self.API = '{}/{}/{}'.format(
            self._bridge.API,
            self.api_endpoint,
            self.hue_id
        )

    def delete(self):
        return self._request(
            method='DELETE',
            url=self.API
        )

    @property
    def address(self):
        '''
        Return the address of this "object", minus the scheme, hostname
        and port of the bridge
        '''
        return self.API.replace(
            'http://{}:{}'.format(
                self._bridge.hostname,
                self._bridge.port
            ), ''
        )

    # Shortcut function
    def _request(self, *args, **kwargs):
        if 'url' not in kwargs:
            return self._bridge._request(url=self.API, *args, **kwargs)
        return self._bridge._request(*args, **kwargs)

    def update(self):
        '''
        Update our object's data
        '''
        self._json = self._request(
            method='GET',
            url=self.API
        )._json


class HueLLDevice(HueObject):
    def _set_state(self, data):
        url = '{}/state'.format(self.API)
        res = self._request(
            method='PUT',
            url=url,
            data=data
        )
        self.update()
        return res

    @property
    def manufacturer(self):
        return self._json['manufacturername']

    @property
    def model(self):
        return self._json['modelid']

    @property
    def name(self):
        return self._json['name']

    @name.setter
    def name(self, value):
        self._request(
            method='PUT',
            data={'name': value}
        )
        self.update()

    @property
    def version(self):
        return self._json['swversion']

    @property
    def uuid(self):
        return self._json.get('uniqueid', None)

    def __decompose_uuid(self):
        if self.uuid:
            m = re.match(uuid_mac_regex, self.uuid)
            if m:
                return m.group(1), m.group(4)
        return None, None

    @property
    def mac_address(self):
        mac, _ = self.__decompose_uuid()
        return mac

    @property
    def device_id(self):
        _, dev_id = self.__decompose_uuid()
        return dev_id

    @property
    def type(self):
        return self._json['type']

    @property
    def state(self):
        return self._json['state']

    # @property
    # def config(self):
    #     return self._json['config']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.name)


class LightDevice(HueLLDevice):
    def __on_off(self, state):
        assert state in ['on', 'off'], 'Unknown state: {}'.format(state)
        return self._set_state(data={'on': state == 'on'})

    def on(self):
        return self.__on_off('on')

    def off(self):
        return self.__on_off('off')

    @property
    def is_on(self):
        return self.state.on

    def toggle(self):
        return self.off() if self.is_on else self.on()

    def delete(self):
        return self._request(method='DELETE')

    def alert(self, effect='select'):
        assert effect in ['select', 'lselect', 'none'], \
            'Unknown alert effect: {}'.format(effect)
        return self._set_state(data={'alert': effect})

    def alert_stop(self):
        return self.alert('none')

    @property
    def brightness(self):
        return self.state.brightness

    @brightness.setter
    def brightness(self, value):
        assert value in xrange(0, 256), 'Unsupported brigthness value'
        return self._set_state(data={'bri': value})

    @property
    def saturation(self):
        return self.state.saturation

    @saturation.setter
    def saturation(self, value):
        assert value in xrange(0, 256), 'Unsupported saturation value'
        return self._set_state(data={'sat': value})

    @property
    def hue(self):
        return self.state.hue

    @hue.setter
    def hue(self, value):
        assert value in xrange(0, 65536), 'Unsupported hue value'
        return self._set_state(data={'hue': value})

    @property
    def xy(self):
        return self.state.xy

    @xy.setter
    def xy(self, value):
        assert type(value) is list, 'Unsupported xy value'
        return self._set_state(data={'xy': value})

    @property
    def color_temperature(self):
        return self.state.color_temperature

    @color_temperature.setter
    def color_temperature(self, value):
        assert value in xrange(0, 65536), 'Unsupported color_temperature value'
        return self._set_state(data={'ct': value})


class LightDeviceState(HueJsonObject):
    @property
    def alert(self):
        return self._json['alert']

    @property
    def on(self):
        return self._json['on']

    @property
    def brightness(self):
        return self._json['bri']

    @property
    def colormode(self):
        return self._json['colormode']

    @property
    def color_temperature(self):
        return self._json['ct']

    @property
    def effect(self):
        return self._json['effect']

    @property
    def hue(self):
        return self._json['hue']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def saturation(self):
        return self._json['sat']

    @property
    def xy(self):
        return self._json['xy']


class BaseGroup(LightDevice):
    @property
    def lights(self):
        l = []
        for l_id in self._json['lights']:
            l.append(self._bridge.light(hue_id=l_id))
        return l
