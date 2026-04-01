from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, OUTPUT_IMPERIAL
from .iapws_region1 import compute_region1

# (label, unit_si, unit_imperial, icon, precision_si, precision_imperial)
OUTPUT_PROPERTIES = {
    "density": ("Dichte", "kg/m³", "lb/ft³", "mdi:water", 2, 4),
    "enthalpy": ("Enthalpie", "kJ/kg", "BTU/lbm", "mdi:fire", 2, 2),
    "entropy": ("Entropie", "kJ/kg·K", "BTU/lbm·°F", "mdi:chart-bell-curve", 4, 4),
    "internal_energy": (
        "Innere Energie",
        "kJ/kg",
        "BTU/lbm",
        "mdi:lightning-bolt",
        2,
        2,
    ),
    "cp": ("Wärmekapazität cp", "kJ/kg·K", "BTU/lbm·°F", "mdi:thermometer", 4, 4),
    "cv": ("Wärmekapazität cv", "kJ/kg·K", "BTU/lbm·°F", "mdi:thermometer", 4, 4),
    "speed_of_sound": ("Schallgeschwindigkeit", "m/s", "ft/s", "mdi:sine-wave", 1, 1),
    "viscosity": ("Viskosität", "µPa·s", "lb/ft·s", "mdi:water-opacity", 1, 6),
    "thermal_conductivity": (
        "Wärmeleitfähigkeit",
        "W/m·K",
        "BTU/h·ft·°F",
        "mdi:heat-wave",
        4,
        4,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    sensors = [
        IAPWSSensor(hass, entry, prop, *meta)
        for prop, meta in OUTPUT_PROPERTIES.items()
    ]
    async_add_entities(sensors, update_before_add=True)


class IAPWSSensor(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True

    def __init__(
        self,
        hass,
        entry,
        prop,
        label,
        unit_si,
        unit_imperial,
        icon,
        precision_si,
        precision_imperial,
    ):
        self.hass = hass
        self.entry = entry
        self._prop = prop
        self._unit_si = unit_si
        self._unit_imperial = unit_imperial
        self._precision_si = precision_si
        self._precision_imperial = precision_imperial
        self._attr_name = f"IAPWS95 {label}"
        self._attr_unique_id = f"{entry.entry_id}_{prop}"
        self._attr_icon = icon
        self._attr_native_value = None
        self._attr_available = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="IAPWS95 Wassereigenschaften",
            manufacturer="IAPWS",
            model="Region 1",
        )
        self._update_unit()

    def _update_unit(self):
        imperial = self.entry.options.get("output_unit") == OUTPUT_IMPERIAL
        self._attr_native_unit_of_measurement = (
            self._unit_imperial if imperial else self._unit_si
        )
        self._attr_suggested_display_precision = (
            self._precision_imperial if imperial else self._precision_si
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

            value = result[self._prop]
            if self._prop == "viscosity" and out_unit != OUTPUT_IMPERIAL:
                value = value * 1e6  # Pa·s → µPa·s

            self._update_unit()
            self._attr_native_value = round(value, 6)
            self._attr_available = True
        except Exception:
            self._attr_available = False
