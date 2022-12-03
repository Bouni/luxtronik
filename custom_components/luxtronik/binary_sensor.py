"""Support for Luxtronik heatpump binary states."""
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.const import CONF_FRIENDLY_NAME, CONF_ICON, CONF_ID, CONF_SENSORS
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify

from . import DOMAIN, ENTITY_ID_FORMAT
from .const import (
    CONF_CALCULATIONS,
    CONF_GROUP,
    CONF_INVERT_STATE,
    CONF_PARAMETERS,
    CONF_VISIBILITIES,
)

ICON_ON = "mdi:check-circle-outline"
ICON_OFF = "mdi:circle-outline"

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_CLASS = None

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SENSORS): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required(CONF_GROUP): vol.All(
                        cv.string,
                        vol.In([CONF_PARAMETERS, CONF_CALCULATIONS, CONF_VISIBILITIES]),
                    ),
                    vol.Required(CONF_ID): cv.string,
                    vol.Optional(CONF_FRIENDLY_NAME): cv.string,
                    vol.Optional(CONF_ICON): cv.string,
                    vol.Optional(CONF_INVERT_STATE, default=False): cv.boolean,
                }
            ],
        )
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Luxtronik binary sensor."""
    luxtronik = hass.data.get(DOMAIN)
    if not luxtronik:
        return False

    sensors = config.get(CONF_SENSORS)

    entities = []
    for sensor_cfg in sensors:
        sensor = luxtronik.get_sensor(sensor_cfg[CONF_GROUP], sensor_cfg[CONF_ID])
        if sensor:
            entities.append(
                LuxtronikBinarySensor(
                    luxtronik,
                    sensor,
                    sensor_cfg.get(CONF_FRIENDLY_NAME),
                    sensor_cfg.get(CONF_ICON),
                    sensor_cfg.get(CONF_INVERT_STATE),
                )
            )
        else:
            _LOGGER.warning(
                "Invalid Luxtronik ID %s in group %s",
                sensor_cfg[CONF_ID],
                sensor_cfg[CONF_GROUP],
            )

    add_entities(entities, True)


class LuxtronikBinarySensor(BinarySensorEntity):
    """Representation of a Luxtronik binary sensor."""

    def __init__(self, luxtronik, sensor, friendly_name, icon, invert_state):
        """Initialize a new Luxtronik binary sensor."""
        self._luxtronik = luxtronik
        self._sensor = sensor
        self._name = friendly_name
        self._icon = icon
        self._invert = invert_state
        self._attr_unique_id = ENTITY_ID_FORMAT.format(
            slugify(self._sensor.name if not self._name else self._name)
        )

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def name(self):
        """Return the name of the sensor."""
        if not self._name:
            return self._sensor.name
        return self._name

    @property
    def is_on(self):
        """Return true if binary sensor is on."""
        if self._invert:
            return not self._sensor.value
        return self._sensor.value

    @property
    def device_class(self):
        """Return the dvice class."""
        return DEFAULT_DEVICE_CLASS

    def update(self):
        """Get the latest status and use it to update our sensor state."""
        self._luxtronik.update()
