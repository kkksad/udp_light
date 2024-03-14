import socket
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP,
    LightEntity,
)

CONF_IP_ADDRESS = "ip_address"
CONF_PORT = "port"

DEFAULT_PORT = 1234

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the UDP light platform."""
    ip_address = config.get(CONF_IP_ADDRESS)
    port = config.get(CONF_PORT)

    add_entities([UDPLight(ip_address, port)], True)

class UDPLight(LightEntity):
    """Representation of a UDP controlled light."""

    def __init__(self, ip_address, port):
        """Initialize the UDP light."""
        self._ip_address = ip_address
        self._port = port
        self._state = False
        self._brightness = 255

    @property
    def name(self):
        """Return the name of the light."""
        return "UDP Light"

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP

    def turn_on(self, **kwargs):
        """Turn the light on."""
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness is not None:
            self._brightness = brightness
            set_bright(self._ip_address, self._port, self._brightness)

        color_temp = kwargs.get(ATTR_COLOR_TEMP)
        if color_temp is not None:
            self._state = True
            set_color(self._ip_address, self._port, color_temp)

    def turn_off(self, **kwargs):
        """Turn the light off."""
        self._state = False

    def update(self):
        """Get the latest data from the UDP light and updates the states."""
        pass
