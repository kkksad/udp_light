import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    LightEntity,
    SUPPORT_BRIGHTNESS,
)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the UDP light platform."""
    if discovery_info is None:
        return

    light = UDPLight(discovery_info["ip_address"], discovery_info["port"])
    add_entities([light])

class UDPLight(LightEntity):
    """Representation of a UDP controlled light."""

    def __init__(self, ip_address, port):
        """Initialize the UDP light."""
        self._ip_address = ip_address
        self._port = port
        self._state = False
        self._brightness = 0

    @property
    def name(self):
        """Return the name of the light."""
        return "UDP Light"

    @property
    def unique_id(self):
        """Return a unique ID to use for this light."""
        return f"udp_light_{self._ip_address}_{self._port}"

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self._state

    @property
    def brightness(self):
        """Return the brightness of the light between 0..255."""
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    def turn_on(self, **kwargs):
        """Turn the light on."""
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness is not None:
            self._brightness = brightness
        self._state = True
        self.send_command(self._state, self._brightness)

    def turn_off(self, **kwargs):
        """Turn the light off."""
        self._state = False
        self.send_command(self._state, self._brightness)

    def update(self):
        """Get the latest state of the light."""
        pass

    def send_command(self, state, brightness):
        """Send command to the UDP light."""
        # Implement your UDP communication here
        pass
