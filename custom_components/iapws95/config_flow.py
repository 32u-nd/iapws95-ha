import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
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
    DEFAULT_TEMP_UNIT,
    DEFAULT_PRESSURE_UNIT,
    OUTPUT_SI,
)


def _build_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                "temp_entity",
                **(
                    {"default": defaults["temp_entity"]}
                    if "temp_entity" in defaults
                    else {}
                ),
            ): EntitySelector(EntitySelectorConfig(domain="sensor")),
            vol.Optional(
                "temp_unit",
                default=defaults.get("temp_unit", DEFAULT_TEMP_UNIT),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=SUPPORTED_TEMP_UNITS,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                "pressure_entity",
                **(
                    {"default": defaults["pressure_entity"]}
                    if "pressure_entity" in defaults
                    else {}
                ),
            ): EntitySelector(EntitySelectorConfig(domain="sensor")),
            vol.Optional(
                "pressure_unit",
                default=defaults.get("pressure_unit", DEFAULT_PRESSURE_UNIT),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=SUPPORTED_PRESSURE_UNITS,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                "output_unit",
                default=defaults.get("output_unit", OUTPUT_SI),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=SUPPORTED_OUTPUT_UNITS,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


class IAPWSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return IAPWSOptionsFlow()

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=_build_schema({}),
            )
        return self.async_create_entry(
            title="IAPWS95 Water Properties",
            data={},
            options=user_input,
        )


class IAPWSOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=_build_schema(dict(self.config_entry.options)),
            )
        return self.async_create_entry(title="", data=user_input)
