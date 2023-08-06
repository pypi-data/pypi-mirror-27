zhue
============

This library eases the interaction with Philips Hue devices

.. code-block::

    from zhue import Bridge

    # upnp/nupnp discovery
    b = Bridge.discover()

    # register a new user on the Hue bridge
    b.create_user()

    # or use a predefined username
    b.username = 'MY_USERNAME'

    # query lights
    b.lights

    # turn light on and off
    b.light('outdoor').on()
    b.light('outdoor').off()

    # query groups
    b.groups

    # turn all lights belonging to a group on
    b.group('living').on()

    # query sensors
    b.sensors

    # get temperature readings
    [x.temperature for x in b.temperature_sensors]

    # get light level readings
    [x.light_level for x in b.light_level_sensors]

    # get battery levels
    [x.config.battery for x in b.sensors if hasattr(x.config, 'battery')]
