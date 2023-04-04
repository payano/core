"""The dimmer_button integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
import homeassistant.core as ha
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

from .logic import SwitchHandler

DOMAIN = "dimmer_button"

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
# PLATFORMS: list[Platform] = [Platform.LIGHT]
PLATFORMS: list[Platform] = None


def yolo():
    _LOGGER.error("YOOOOOOLOOOOO")


async def async_say_hello(hass, target):
    _LOGGER.error("RUNEEEEMEMEMEEMEMEg")
    yolo()


async def async_setup(hass, config):
    # hass.states.async_set("dimmer_button.world", "Paulus")

    # _LOGGER.error(config["dimmer_button"])
    dimmer_config = config["dimmer_button"]

    entities = []

    switchHandler = SwitchHandler(hass, dimmer_config, handle_sw_event)
    entities = switchHandler.getEntities()
    hass.data.setdefault(DOMAIN, {})["switchhandler"] = switchHandler
    hass.async_create_task(async_say_hello(hass, dimmer_config))
    print(dimmer_config)
    # print(len(dimmer_config["switches"]))
    # entities = []

    # _LOGGER.error("HAHA")
    # entities.append("sensor.strombrytare_vardagsrum_action")
    print(entities)

    # hass.bus.async_listen(EVENT_STATE_CHANGED, handl2e_event)
    async_track_state_change_event(hass, entities, switchHandler.incoming_event)
    # hass.bus.listen(EVENT_STATE_CHANGED, handle_event)
    # hass.bus.listen("example_component_my_cool_event", handle_event)
    # _LOGGER.error("HAHA2")
    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up dimmer_button from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


@ha.callback
def handle_event(value):
    # _LOGGER.error(value)
    input = {}
    entity_id = value.data["entity_id"]
    new_state = value.data["new_state"].state
    input["entity"] = entity_id
    input["event"] = new_state
    switchHandler = hass.data[DOMAIN]["switchhandler"]
    switchHandler.input(input)
    _LOGGER.error(entity_id)
    _LOGGER.error(new_state)


@ha.callback
def handle_sw_event(value):
    hass.data[DOMAIN]["switchhandler"]
    print(swithandler)
    _LOGGER.error("SICK!")
    _LOGGER.error(value)
