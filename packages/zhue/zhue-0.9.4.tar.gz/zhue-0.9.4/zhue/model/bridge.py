#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import re
import requests
from simplejson.decoder import JSONDecodeError

from .api_response import (HueApiResponse, HueErrorResponse)
from .config import BridgeConfig
from .device import HueDevice
from .group import (Group, MasterGroup)
from .light import Light
from .rule import Rule
from .scene import Scene
from .schedule import Schedule
from .sensor import (LightLevelSensor, SwitchSensor,
                     TemperatureSensor, PresenceSensor)
from .sensor import factory as sensorfactory


_LOGGER = logging.getLogger(__name__)


class HueError(Exception):
    pass


class Bridge(object):
    def __init__(self, hostname, username=None, port=80):
        self.hostname = hostname
        self.port = port
        self._username = username
        self.__contruct_api_url()

    def from_address(self, address):
        endpoint_regex = re.compile(r'/api/([^/]+)/([^/]+)/([^/]+)(?:/(.+))?')
        match = re.match(endpoint_regex, address)
        assert match, 'Invalid address'
        endpoint = match.group(2)
        hue_id = match.group(3)
        if endpoint == 'sensors':
            return self.sensor(hue_id=hue_id)
        elif endpoint == 'lamps':
            return self.light(hue_id=hue_id)
        elif endpoint == 'groups':
            return self.group(hue_id=hue_id)
        elif endpoint == 'schedules':
            return self.schedule(hue_id=hue_id)
        raise HueError('Unsupported enpoint')

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.__contruct_api_url()

    def __contruct_api_url(self):
        self.API = 'http://{}:{}/api'.format(
            self.hostname,
            self.port
        )
        if self.username:
            self.API += '/{}'.format(self.username)
        _LOGGER.info('Update API URL to: {}'.format(self.API))

    def _request(self, url, method='GET', data=None):
        res = requests.request(url=url, method=method, json=data)
        logging.debug('Request data: {}'.format(data))
        if not res.ok:
            res.raise_for_status()
        try:
            jr = res.json()
            _LOGGER.debug('JSON Response: {}'.format(jr))
            response = HueApiResponse.factory(jr)
            if type(response) is HueErrorResponse:
                raise HueError(response.description)
            return response
        except JSONDecodeError:
            _LOGGER.error(
                'Failed to decode JSON from response: {}'.format(res.text)
            )

    @staticmethod
    def from_url(url, username=None):
        from urlparse import urlparse
        res = urlparse(url)
        return Bridge(hostname=res.hostname, port=res.port, username=username)

    @staticmethod
    def discover(username=None, guess=True, fast=True):
        nupnp = Bridge.discover_nupnp(username=username)
        if not fast or not nupnp:
            upnp = Bridge.discover_upnp(username=username)
        else:
            _LOGGER.info('Skip UPNP discovery')
            upnp = []
        bridges = list(set(upnp + nupnp))
        return bridges[0] if guess and bridges else bridges

    @staticmethod
    def discover_nupnp(username=None):
        res = requests.get('https://www.meethue.com/api/nupnp')
        return [Bridge(x['internalipaddress'], username) for x in res.json()]

    @staticmethod
    def discover_upnp(username=None):
        from netdisco.ssdp import scan

        PHILIPS = 'Royal Philips Electronics'
        BRIDGE_MODELS = ['929000226503', 'BSB002']

        hue_bridges = []
        res = scan()

        for h in res:
            _LOGGER.info('Check {}'.format(h))
            device_info = h.description.get('device', None)
            if device_info:
                manufacturer = device_info.get('manufacturer', None)
                model = device_info.get('modelNumber', None)
                if manufacturer == PHILIPS and model in BRIDGE_MODELS:
                    url = h.description['URLBase']
                    if url not in hue_bridges:
                        hue_bridges.append(url)
            else:
                _LOGGER.error('Missing device info')
        return [Bridge.from_url(x, username) for x in hue_bridges]

    def delete_user(self, username):
        url = '{}/config/whitelist/{}'.format(self.API, username)
        return self._request(method='DELETE', url=url)

    def delete_light(self, hue_id):
        url = '{}/lights/{}'.format(self.API, hue_id)
        return self._request(method='DELETE', url=url)

    def get_full_state(self):
        return self._request(method='GET', url=self.API)

    def _property(self, prop_url):
        url = '{}/{}'.format(self.API, prop_url)
        res = self._request(url)
        return res._json

    @property
    def config(self):
        return BridgeConfig(self, self._property('config'))

    @property
    def users(self):
        return self.config.users

    @property
    def lights(self):
        l = []
        for i, v in self._property('lights').items():
            l.append(Light(self, i, v))
        return l

    @property
    def groups(self):
        l = []
        for i, v in self._property('groups').items():
            l.append(Group(self, i, v))
        return l

    @property
    def schedules(self):
        l = []
        for i, v in self._property('schedules').items():
            l.append(Schedule(self, i, v))
        return l

    @property
    def sensors(self):
        s = []
        for i, v in self._property('sensors').items():
            s.append(sensorfactory(self, i, v))
        return s

    @property
    def scenes(self):
        s = []
        for i, v in self._property('scenes').items():
            s.append(Scene(self, i, v))
        return s

    @property
    def devices(self):
        devs = []
        sensors_grouped = self.__regroup_sensors()
        for d in filter(None, sensors_grouped):
            devs.append(HueDevice.factory(sensors_grouped[d]))
        devs += self.lights
        return devs

    @property
    def rules(self):
        r = []
        for i, v in self._property('scenes').items():
            r.append(Rule(self, i, v))
        return r

    def __regroup_sensors(self):
        d = {}
        for s in self.sensors:
            mac_addr = None
            try:
                mac_addr = s.mac_address
            except:
                pass
            if mac_addr in d:
                d[mac_addr].append(s)
            else:
                d[mac_addr] = [s]
        return d

    def __get_sensors_by_type(self, sensor_type):
        return [x for x in self.sensors if isinstance(x, sensor_type)]

    @property
    def temperature_sensors(self):
        return self.__get_sensors_by_type(TemperatureSensor)

    @property
    def light_level_sensors(self):
        return self.__get_sensors_by_type(LightLevelSensor)

    @property
    def presence_sensors(self):
        return self.__get_sensors_by_type(PresenceSensor)

    @property
    def switches(self):
        return self.__get_sensors_by_type(SwitchSensor)

    def __get_hue_objects_by_type(self, device_type):
        if device_type == 'sensor':
            return self.sensors
        elif device_type == 'switch':
            return self.switches
        elif device_type == 'light':
            return self.lights
        elif device_type == 'group':
            return self.groups
        elif device_type == 'schedule':
            return self.schedules
        elif device_type == 'scene':
            return self.scenes
        elif device_type == 'user':
            return self.users
        elif device_type == 'device':
            return self.devices
        elif device_type == 'rule':
            return self.rules
        else:
            _LOGGER.error('Unknown device type')

    def __get_hue_object(self, device_type, name=None, hue_id=None,
                         exact=False):
        assert name or hue_id, 'Name or Hue ID must be provided'
        for d in self.__get_hue_objects_by_type(device_type):
            if hue_id and str(d.hue_id) == str(hue_id):
                return d
            if name:
                if exact:
                    if d.name == name:
                        return d
                else:
                    if re.match('.*{}.*'.format(name), d.name, re.IGNORECASE):
                        return d
        raise HueError('No matching item was found')

    def group(self, name=None, hue_id=None, exact=False):
        if hue_id == 0:
            return MasterGroup(self)
        return self.__get_hue_object('group', name, hue_id, exact)

    def light(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('light', name, hue_id, exact)

    def sensor(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('sensor', name, hue_id, exact)

    def switch(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('switch', name, hue_id, exact)

    def schedule(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('schedule', name, hue_id, exact)

    def scene(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('scene', name, hue_id, exact)

    def user(self, name=None, username=None, exact=False):
        return self.__get_hue_object('user', name, username, exact)

    def device(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('device', name, hue_id, exact)

    def rule(self, name=None, hue_id=None, exact=False):
        return self.__get_hue_object('rule', name, hue_id, exact)

    # Hue object discovery
    def __find_new(self, hueobjecttype):
        '''
        Starts a search for new Hue objects
        '''
        assert hueobjecttype in ['lights', 'sensors'], \
            'Unsupported object type {}'.format(hueobjecttype)
        url = '{}/{}'.format(self.API, hueobjecttype)
        return self._request(
            method='POST',
            url=url
        )

    def __get_new(self, hueobjecttype):
        '''
        Get a list of newly found Hue object
        '''
        assert hueobjecttype in ['lights', 'sensors'], \
            'Unsupported object type {}'.format(hueobjecttype)
        url = '{}/{}/new'.format(self.API, hueobjecttype)
        return self._request(url=url)

    def find_new_lights(self):
        return self.__find_new('lights')

    def new_lights(self):
        return self.__get_new('lights')

    def find_new_sensors(self):
        return self.__find_new('sensors')

    def new_sensors(self):
        return self.__get_new('sensors')

    # All on/off
    def all_off(self):
        return MasterGroup(self).off()

    def all_on(self):
        return MasterGroup(self).on()

    # Factory methods. Create new objects
    def create_user(self, devicetype='zhue.py#user'):
        url = 'http://{}:{}/api'.format(self.hostname, self.port)
        data = {'devicetype': devicetype}
        res = self._request(method='POST', url=url, data=data)
        self.username = res._json['username']
        return res

    def create_schedule(self, *args, **kwargs):
        return Schedule.new(self, *args, **kwargs)

    def create_rule(self, *args, **kwargs):
        return Rule.new(self, *args, **kwargs)

    # Software update
    def update_check(self):
        return
