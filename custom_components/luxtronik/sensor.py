"""Support for Luxtronik heatpump sensors."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, STATE_CLASSES_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_FRIENDLY_NAME,
    CONF_ICON,
    CONF_ID,
    CONF_SENSORS,
)
from homeassistant.util import slugify

from . import DOMAIN, ENTITY_ID_FORMAT
from .const import (
    CONF_CALCULATIONS,
    CONF_GROUP,
    CONF_PARAMETERS,
    CONF_VISIBILITIES,
    CONF_STATE_CLASS,
    DEVICE_CLASSES,
    ICONS,
    UNITS,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_CLASS = None
DEFAULT_STATE_CLASS = None

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SENSORS): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required(CONF_GROUP): vol.All(
                        cv.string,
                        vol.Any(CONF_PARAMETERS, CONF_CALCULATIONS, CONF_VISIBILITIES),
                    ),
                    vol.Required(CONF_ID): cv.string,
                    vol.Optional(CONF_FRIENDLY_NAME): cv.string,
                    vol.Optional(CONF_ICON): cv.string,
                    vol.Optional(CONF_STATE_CLASS): STATE_CLASSES_SCHEMA,
                }
            ],
        )
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Luxtronik sensor."""
    luxtronik = hass.data.get(DOMAIN)
    if not luxtronik:
        return False

    sensors = config.get(CONF_SENSORS)

    entities = []
    for sensor_cfg in sensors:
        sensor = luxtronik.get_sensor(sensor_cfg[CONF_GROUP], sensor_cfg[CONF_ID])
        if sensor:
            entities.append(
                LuxtronikSensor(
                    luxtronik,
                    sensor,
                    sensor_cfg.get(CONF_FRIENDLY_NAME),
                    sensor_cfg.get(CONF_ICON),
                    sensor_cfg.get(CONF_STATE_CLASS),
                )
            )
        else:
            _LOGGER.warning(
                "Invalid Luxtronik ID %s in group %s",
                sensor_cfg[CONF_ID],
                sensor_cfg[CONF_GROUP],
            )

    add_entities(entities, True)


class LuxtronikSensor(SensorEntity):
    """Representation of a Luxtronik sensor."""

    def __init__(self, luxtronik, sensor, friendly_name, icon, state_class):
        """Initialize a new Luxtronik sensor."""
        self._luxtronik = luxtronik
        self._sensor = sensor
        self._name = friendly_name
        self._icon = icon
        self._state_class = state_class
        self._attr_unique_id = ENTITY_ID_FORMAT.format(
            slugify(self._sensor.name if not self._name else self._name)
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        if not self._name:
            return self._sensor.name
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if not self._icon:
            return ICONS.get(self._sensor.measurement_type)
        return self._icon

    @property
    def state(self):
        """Return the sensor state."""
        return self._sensor.value

    @property
    def state_class(self):
        """Return the state class of this sensor."""
        if not self._state_class:
            return DEFAULT_STATE_CLASS
        return self._state_class

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return DEVICE_CLASSES.get(self._sensor.measurement_type, DEFAULT_DEVICE_CLASS)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return UNITS.get(self._sensor.measurement_type)

    def update(self):
        """Get the latest status and use it to update our sensor state."""
        self._luxtronik.update()
