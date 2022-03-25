"""Support for Luxtronik heatpump controllers."""
import threading
from datetime import timedelta
from typing import Optional
import logging

from luxtronik import LOGGER as LuxLogger, Luxtronik as Lux
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

from .const import (
    ATTR_PARAMETER,
    ATTR_VALUE,
    CONF_CALCULATIONS,
    CONF_PARAMETERS,
    CONF_SAFE,
    CONF_VISIBILITIES,
    CONF_UPDATE_IMMEDIATELY_AFTER_WRITE,
    CONF_LOCK_TIMEOUT,
)

LuxLogger.setLevel(level="WARNING")


_LOGGER = logging.getLogger(__name__)

LUXTRONIK_PLATFORMS = ["binary_sensor", "sensor"]
DOMAIN = "luxtronik"

ENTITY_ID_FORMAT = DOMAIN + ".{}"

SERVICE_WRITE = "write"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_PORT, default=8889): cv.port,
                vol.Optional(CONF_SAFE, default=True): cv.boolean,
                vol.Optional(CONF_LOCK_TIMEOUT, default=30): cv.positive_int,
                vol.Optional(
                    CONF_UPDATE_IMMEDIATELY_AFTER_WRITE, default=False
                ): cv.boolean,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

SERVICE_WRITE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_PARAMETER): cv.string,
        vol.Required(ATTR_VALUE): vol.Any(cv.Number, cv.string),
    }
)


def setup(hass, config):
    """Set up the Luxtronik component."""
    conf = config[DOMAIN]

    host = conf[CONF_HOST]
    port = conf[CONF_PORT]
    safe = conf[CONF_SAFE]
    lock_timeout = conf[CONF_LOCK_TIMEOUT]
    update_immediately_after_write = conf[CONF_UPDATE_IMMEDIATELY_AFTER_WRITE]

    luxtronik = LuxtronikDevice(host, port, safe, lock_timeout)

    hass.data[DOMAIN] = luxtronik

    def write_parameter(service):
        """Write a parameter to the Luxtronik heatpump."""
        parameter = service.data.get(ATTR_PARAMETER)
        value = service.data.get(ATTR_VALUE)
        luxtronik.write(parameter, value, update_immediately_after_write)

    hass.services.register(
        DOMAIN, SERVICE_WRITE, write_parameter, schema=SERVICE_WRITE_SCHEMA
    )

    return True


class LuxtronikDevice:
    """Handle all communication with Luxtronik."""

    def __init__(self, host, port, safe, lock_timeout_sec):
        """Initialize the Luxtronik connection."""
        self.lock = threading.Lock()

        self._host = host
        self._port = port
        self._lock_timeout_sec = lock_timeout_sec
        self._luxtronik = Lux(host, port, safe)
        self.update()

    def get_sensor(self, group, sensor_id):
        """Get sensor by configured sensor ID."""
        sensor = None
        if group == CONF_PARAMETERS:
            sensor = self._luxtronik.parameters.get(sensor_id)
        if group == CONF_CALCULATIONS:
            sensor = self._luxtronik.calculations.get(sensor_id)
        if group == CONF_VISIBILITIES:
            sensor = self._luxtronik.visibilities.get(sensor_id)
        return sensor

    def write(self, parameter, value, update_immediately_after_write):
        """Write a parameter to the Luxtronik heatpump."""
        try:
            if self.lock.acquire(blocking=True, timeout=self._lock_timeout_sec):
                self._luxtronik.parameters.set(parameter, value)
                self._luxtronik.write()
                if update_immediately_after_write:
                    self._luxtronik.read()
            else:
                _LOGGER.warning(
                    "Couldn't write luxtronik parameter %s with value %s because of lock timeout %s",
                    parameter,
                    value,
                    self._lock_timeout_sec,
                )
        finally:
            self.lock.release()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the data from Luxtronik."""
        try:
            if self.lock.acquire(blocking=True, timeout=self._lock_timeout_sec):
                self._luxtronik.read()
            else:
                _LOGGER.warning(
                    "Couldn't read luxtronik data because of lock timeout %s",
                    self._lock_timeout_sec,
                )
        finally:
            self.lock.release()
