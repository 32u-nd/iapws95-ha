import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from .const import (
    DOMAIN,
    SUPPORTED_TEMP_UNITS,
    SUPPORTED_PRESSURE_UNITS,
    SUPPORTED_OUTPUT_UNITS,
)


class IAPWSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("temp_entity"): EntitySelector(
                            EntitySelectorConfig(domain="sensor")
                        ),
                        vol.Required("pressure_entity"): EntitySelector(
                            EntitySelectorConfig(domain="sensor")
                        ),
                        vol.Optional("temp_unit", default="C"): SelectSelector(
                            SelectSelectorConfig(
                                options=SUPPORTED_TEMP_UNITS,
                                mode=SelectSelectorMode.DROPDOWN,
                            )
                        ),
                        vol.Optional("pressure_unit", default="bar"): SelectSelector(
                            SelectSelectorConfig(
                                options=SUPPORTED_PRESSURE_UNITS,
                                mode=SelectSelectorMode.DROPDOWN,
                            )
                        ),
                        vol.Optional("output_unit", default="si"): SelectSelector(
                            SelectSelectorConfig(
                                options=SUPPORTED_OUTPUT_UNITS,
                                mode=SelectSelectorMode.DROPDOWN,
                            )
                        ),
                    }
                ),
            )
        return self.async_create_entry(
            title="IAPWS95 Water Properties", data={}, options=user_input
        )

    async def async_step_options(self, user_input=None):
        return await self.async_step_user(user_input)
