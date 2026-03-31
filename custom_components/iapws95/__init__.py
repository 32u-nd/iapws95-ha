from homeassistant.core import HomeAssistant


async def async_setup_entry(hass: HomeAssistant, entry):
    hass.data.setdefault("iapws95", {})
    return True
