#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import
import argparse
import logging
import time

from zhue.model.bridge import Bridge
from yaml import load as yaml_load
import requests


_LOGGER = logging.getLogger(__name__)


def parse_args():
    ON_OFF_CHOICE = ['on', 'off']
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        help='Username', required=True)
    parser.add_argument('-b', '--bridge',
                        help='Hostname or IP of the Hue bridge',
                        default=None, required=False)
    subparsers = parser.add_subparsers(dest='action', help='Action')
    light_parser = subparsers.add_parser('light')
    light_parser.add_argument('NAME')
    light_parser.add_argument('STATE', choices=ON_OFF_CHOICE)
    subparsers.add_parser('sensors')
    sensor_parser = subparsers.add_parser('sensor')
    sensor_parser.add_argument('NAME')
    sensor_parser.add_argument('STATE', choices=ON_OFF_CHOICE, nargs='?')
    switch_parser = subparsers.add_parser('switch')
    switch_parser.add_argument('NAME')
    switch_parser.add_argument('-w', '--wait', action='store_true',
                               default=False)
    switch_parser.add_argument('-S', '--secrets-file',
                               required=False, type=argparse.FileType('r'),
                               help='Home Assistant secrets file')
    switch_parser.add_argument('-H', '--home-assistant',
                               required=False,
                               help='Home Assistant URL')
    switch_parser.add_argument('-P', '--home-assistant-password',
                               required=False,
                               help='Home Assistant Password')
    temperature_parser = subparsers.add_parser('temperature')
    temperature_parser.add_argument('NAME')
    light_level_parser = subparsers.add_parser('light-level')
    light_level_parser.add_argument('NAME')
    motion_parser = subparsers.add_parser('motion')
    motion_parser.add_argument('NAME')
    battery_parser = subparsers.add_parser('battery')
    battery_parser.add_argument('NAME')
    return parser.parse_args()


def hass_event(url, api_key, switches, event_name='hue_dimmer_switch_pressed'):
    last_updated = {}
    while True:
        for switch in switches:
            last_updated[switch.name] = switch.last_updated
            switch.update()
            if switch.last_updated != last_updated[switch.name]:
                button, click_type = switch.friendly_button_event
                button, click_type = switch.friendly_button_event
                print('Name:', switch.name, '\nButton:', button,
                      '\nEvent:', click_type, '\n')
                if url:
                    try:
                        res = requests.post(
                            '{}/api/events/{}'.format(url, event_name),
                            headers={'X-HA-Access': api_key},
                            json={'switch_name': switch.name,
                                  'button_name': button,
                                  'click_type': click_type}
                        )
                        res.raise_for_status()
                        print(res.json(), '\n')
                    except Exception as exc:
                        _LOGGER.error('Failed to post HASS event: %s', exc)
                last_updated[switch.name] = switch.last_updated
            time.sleep(1)


def main():
    args = parse_args()
    if args.bridge:
        bridge = Bridge(args.bridge, username=args.username)
    else:
        bridges = Bridge.discover_nupnp(username=args.username)
        bridge = bridges[0]
    if args.action == 'lights':
        print(bridge.lights)
    elif args.action == 'light':
        light = bridge.light(args.NAME)
        if args.STATE == 'on':
            light.on()
        else:
            light.off()
    elif args.action == 'sensor':
        sensor = bridge.sensor(args.NAME)
        if args.STATE == 'on':
            print(sensor.enable())
        elif args.STATE == 'off':
            print(sensor.disable())
        else:
            print(sensor._json)
    elif args.action == 'sensors':
        print(bridge.sensors)
    elif args.action == 'switch':
        if args.NAME.lower() == 'all':
            switches = bridge.switches
        else:
            switches = [bridge.switch(args.NAME)]
        if args.wait:
            if args.secrets_file:
                secrets_file = yaml_load(args.secrets_file)
                hass_url = secrets_file.get('base_url')
                hass_key = secrets_file.get('http_password')
            else:
                hass_url = args.home_assistant
                hass_key = args.home_assistant_password
            hass_event(hass_url, hass_key, switches)
        else:
            for switch in switches:
                button, click_type = switch.friendly_button_event
                print('Name:', switch.name, '\nButton:', button,
                      '\nEvent:', click_type)
    elif args.action == 'battery':
        device = bridge.device(args.NAME)
        print(device.battery)
    elif args.action == 'temperature':
        device = bridge.device(args.NAME)
        print(device.temperature)
    elif args.action == 'light-level':
        device = bridge.device(args.NAME)
        print(device.light_level)
    elif args.action == 'motion':
        device = bridge.device(args.NAME)
        print(device.presence)


if __name__ == '__main__':
    main()
