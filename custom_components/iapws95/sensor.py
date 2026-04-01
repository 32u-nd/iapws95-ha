from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .iapws_region1 import compute_region1

OUTPUT_PROPERTIES = {
    "density": ("Dichte", "kg/m³", "mdi:water", 2),
    "enthalpy": ("Enthalpie", "kJ/kg", "mdi:fire", 2),
    "entropy": ("Entropie", "kJ/kg·K", "mdi:chart-bell-curve", 3),
    "internal_energy": ("Innere Energie", "kJ/kg", "mdi:lightning-bolt", 2),
    "cp": ("Wärmekapazität cp", "kJ/kg·K", "mdi:thermometer", 3),
    "cv": ("Wärmekapazität cv", "kJ/kg·K", "mdi:thermometer", 3),
    "speed_of_sound": ("Schallgeschwindigkeit", "m/s", "mdi:sine-wave", 1),
    "viscosity": ("Viskosität", "Pa·s", "mdi:water-opacity", 6),
    "thermal_conductivity": ("Wärmeleitfähigkeit", "W/m·K", "mdi:heat-wave", 3),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    sensors = [
        IAPWSSensor(hass, entry, prop, label, unit, icon, precision)
        for prop, (label, unit, icon, precision) in OUTPUT_PROPERTIES.items()
    ]
    async_add_entities(sensors, update_before_add=True)


class IAPWSSensor(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True

    def __init__(self, hass, entry, prop, label, unit, icon, precision):
        self.hass = hass
        self.entry = entry
        self._prop = prop
        self._attr_name = f"IAPWS95 {label}"
        self._attr_unique_id = f"{entry.entry_id}_{prop}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_suggested_display_precision = precision
        self._attr_native_value = None
        self._attr_available = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="IAPWS95 Wassereigenschaften",
            manufacturer="IAPWS",
            model="Region 1",
        )

    async def async_update(self) -> None:
        t_entity = self.entry.options.get("temp_entity")
        p_entity = self.entry.options.get("pressure_entity")

        t_state = self.hass.states.get(t_entity)
        p_state = self.hass.states.get(p_entity)

        if (
            t_state is None
            or p_state is None
            or t_state.state in ("unavailable", "unknown")
            or p_state.state in ("unavailable", "unknown")
        ):
            self._attr_available = False
            return

        try:
            T = float(t_state.state)
            P = float(p_state.state)

            T_unit = self.entry.options.get("temp_unit", "C")
            P_unit = self.entry.options.get("pressure_unit", "bar")
            out_unit = self.entry.options.get("output_unit", "si")

            result = compute_region1(T, P, T_unit, P_unit, out_unit)
            self._attr_native_value = result[self._prop]
            self._attr_available = True
        except Exception:
            self._attr_available = False
