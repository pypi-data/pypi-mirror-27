from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import (HueObject, HueLLDevice, HueJsonObject)


def factory(bridge, hue_id, json):
    if json['type'] == 'ZLLTemperature':
        return TemperatureSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLLightLevel':
        return LightLevelSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLPresence':
        return PresenceSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLSwitch':
        return SwitchSensor(bridge, hue_id, json)
    else:
        return Sensor(bridge, hue_id, json)


class Sensor(HueLLDevice):
    def __init__(self, bridge, hue_id, json):
        super(Sensor, self).__init__(bridge, 'sensors', hue_id, json)

    @property
    def config(self):
        return SensorConfig(self._json['config'])

    @property
    def state(self):
        return SensorState(self._json['state'])

    @property
    def battery(self):
        return self.config.battery

    @property
    def has_battery(self):
        return self.battery is not None


class SensorConfig(HueJsonObject):
    @property
    def battery(self):
        return self._json.get('battery', None)


class SensorState(HueJsonObject):
    @property
    def last_updated(self):
        return self._json['lastupdated']


class LightLevelSensor(Sensor):
    @property
    def config(self):
        return LightLevelSensorConfig(self._json['config'])

    @property
    def state(self):
        return LightLevelSensorState(self._json['state'])

    @property
    def light_level(self):
        return self.state.light_level


class LightLevelSensorConfig(SensorConfig):
    @property
    def alert(self):
        return self._json['alert']

    @property
    def ledindication(self):
        return self._json['ledindication']

    @property
    def pending(self):
        return self._json['pending']

    @property
    def on(self):
        return self._json['on']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def usertest(self):
        return self._json['usertest']


class LightLevelSensorState(SensorState):
    @property
    def light_level(self):
        return self._json['lightlevel']

    @property
    def dark(self):
        return self._json['dark']

    @property
    def daylight(self):
        return self._json['daylight']


class TemperatureSensor(Sensor):
    @property
    def config(self):
        return TemperatureSensorConfig(self._json['config'])

    @property
    def state(self):
        return TemperatureSensorState(self._json['state'])

    @property
    def temperature(self):
        return self.state.temperature


class TemperatureSensorConfig(LightLevelSensorConfig):
    pass


class TemperatureSensorState(SensorState):
    @property
    def temperature(self):
        return float(self._json['temperature'] / 100.0)


class PresenceSensor(Sensor):
    @property
    def config(self):
        return PresenceSensorConfig(self._json['config'])

    @property
    def state(self):
        return PresenceSensorState(self._json['state'])

    @property
    def presence(self):
        return self.state.presence

    @property
    def battery(self):
        return self.config.battery

    def enable(self):
        return self._bridge._request(
            method='PUT', url=self.API + '/config', data={"on": True})

    def disable(self):
        return self._bridge._request(
            method='PUT', url=self.API + '/config', data={"on": False})


class PresenceSensorConfig(SensorConfig):
    pass


class PresenceSensorState(SensorState):
    @property
    def presence(self):
        return self._json['presence']


class SwitchSensor(Sensor):
    @property
    def config(self):
        return SwitchSensorConfig(self._json['config'])

    @property
    def last_updated(self):
        return self._json.get('state', {}).get('lastupdated')

    @property
    def button_event(self):
        return self._json.get('state', {}).get('buttonevent')

    @property
    def friendly_button_event(self):
        button_event = int(self.button_event)
        button_names = {
            1: 'on',
            2: 'brightness_up',
            3: 'brightness_down',
            4: 'off'
        }
        button_click_types = {
            0: 'short_pressed',
            1: 'long',
            2: 'short_released',
            3: 'long_released'
        }
        name = int(button_event / 1000)
        click_type = button_event - (name * 1000)
        return (button_names.get(name),
                button_click_types.get(click_type))


class SwitchSensorConfig(SensorConfig):
    @property
    def on(self):
        return self._json['on']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def pending(self):
        return self._json['pending']

