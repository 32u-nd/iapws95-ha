from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN
from .iapws_region1 import compute_region1

OUTPUT_PROPERTIES = [
    "density",
    "enthalpy",
    "entropy",
    "internal_energy",
    "cp",
    "cv",
    "speed_of_sound",
    "viscosity",
    "thermal_conductivity",
]


async def async_setup_entry(hass, entry, async_add_entities):
    sensors = []
    for prop in OUTPUT_PROPERTIES:
        sensors.append(IAPWSSensor(hass, entry, prop))
    async_add_entities(sensors)


class IAPWSSensor(SensorEntity):
    def __init__(self, hass, entry, prop):
        self.hass = hass
        self.entry = entry
        self._prop = prop
        self._attr_name = f"IAPWS95 {prop}"
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):
        t_entity = self.entry.options.get("temp_entity")
        p_entity = self.entry.options.get("pressure_entity")

        T = float(self.hass.states.get(t_entity).state)
        P = float(self.hass.states.get(p_entity).state)

        T_unit = self.entry.options.get("temp_unit", "C")
        P_unit = self.entry.options.get("pressure_unit", "bar")
        out_unit = self.entry.options.get("output_unit", "si")

        result = compute_region1(T, P, T_unit, P_unit, out_unit)
        self._state = result[self._prop]
