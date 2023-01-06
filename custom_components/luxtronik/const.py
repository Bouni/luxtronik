"""Constants for the Luxtronik integration."""

from homeassistant.const import (
    UnitOfTemperature,
    UnitOfTime, 
    UnitOfPressure,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfFrequency,
    PERCENTAGE
)
from homeassistant.components.sensor import SensorDeviceClass

ATTR_PARAMETER = "parameter"
ATTR_VALUE = "value"

CONF_STATE_CLASS = "state_class"
CONF_INVERT_STATE = "invert"
CONF_SAFE = "safe"
CONF_GROUP = "group"
CONF_PARAMETERS = "parameters"
CONF_CALCULATIONS = "calculations"
CONF_VISIBILITIES = "visibilities"

CONF_CELSIUS = "celsius"
CONF_SECONDS = "seconds"
CONF_TIMESTAMP = "timestamp"
CONF_KELVIN = "kelvin"
CONF_BAR = "bar"
CONF_PERCENT = "percent"
CONF_ENERGY = "energy"
CONF_VOLTAGE = "voltage"
CONF_HOURS = "hours"
CONF_FLOW = "flow"
CONF_WATT = "W"
CONF_FREQUENCY = "Hz"

CONF_LOCK_TIMEOUT = "lock_timeout"
CONF_UPDATE_IMMEDIATELY_AFTER_WRITE = "update_immediately_after_write"


ICONS = {
    "celsius": "mdi:thermometer",
    "seconds": "mdi:timer-sand",
    "pulses": "mdi:pulse",
    "ipaddress": "mdi:ip-network-outline",
    "timestamp": "mdi:calendar-range",
    "errorcode": "mdi:alert-circle-outline",
    "kelvin": "mdi:thermometer",
    "bar": "mdi:arrow-collapse-all",
    "percent": "mdi:percent",
    "rpm": "mdi:rotate-right",
    "energy": "mdi:flash-circle",
    "voltage": "mdi:flash-outline",
    "hours": "mdi:clock-outline",
    "flow": "mdi:chart-bell-curve",
    "level": "mdi:format-list-numbered",
    "count": "mdi:counter",
    "version": "mdi:information-outline",
    "frequency": "mdi:cosine-wave",
}

DEVICE_CLASSES = {
    CONF_CELSIUS: SensorDeviceClass.TEMPERATURE,
    CONF_KELVIN: SensorDeviceClass.TEMPERATURE,
    CONF_BAR: SensorDeviceClass.PRESSURE,
    CONF_SECONDS: SensorDeviceClass.DURATION,
    CONF_HOURS: SensorDeviceClass.DURATION,
    CONF_TIMESTAMP: SensorDeviceClass.TIMESTAMP,
    CONF_ENERGY: SensorDeviceClass.ENERGY,
    CONF_WATT: SensorDeviceClass.POWER,
    CONF_FREQUENCY: SensorDeviceClass.FREQUENCY,
}

UNITS = {
    CONF_CELSIUS: UnitOfTemperature.CELSIUS,
    CONF_SECONDS: UnitOfTime.SECONDS,
    CONF_KELVIN: UnitOfTemperature.KELVIN,
    CONF_BAR: UnitOfPressure.BAR,
    CONF_PERCENT: PERCENTAGE,
    CONF_ENERGY: UnitOfEnergy.KILO_WATT_HOUR,
    CONF_VOLTAGE: UnitOfElectricPotential.VOLT,
    CONF_HOURS: UnitOfTime.HOURS,
    CONF_FLOW: "l/h",
    CONF_WATT: UnitOfPower.WATT,
    CONF_FREQUENCY: UnitOfFrequency.HERTZ
}
