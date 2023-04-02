"""The dimmer_button integration."""
from __future__ import annotations
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
import homeassistant.core as ha
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    CONF_UNIT_SYSTEM,
    EVENT_CALL_SERVICE,
    EVENT_CORE_CONFIG_UPDATE,
    EVENT_HOMEASSISTANT_CLOSE,
    EVENT_HOMEASSISTANT_FINAL_WRITE,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STARTED,
    EVENT_HOMEASSISTANT_STOP,
    EVENT_SERVICE_REGISTERED,
    EVENT_SERVICE_REMOVED,
    EVENT_STATE_CHANGED,
    MATCH_ALL,
    __version__,
)

from homeassistant.helpers.event import (
    TrackStates,
    TrackTemplate,
    TrackTemplateResult,
    async_call_later,
    async_track_entity_registry_updated_event,
    async_track_point_in_time,
    async_track_point_in_utc_time,
    async_track_same_state,
    async_track_state_added_domain,
    async_track_state_change,
    async_track_state_change_event,
    async_track_state_change_filtered,
    async_track_state_removed_domain,
    async_track_sunrise,
    async_track_sunset,
    async_track_template,
    async_track_template_result,
    async_track_time_change,
    async_track_time_interval,
    async_track_utc_time_change,
    track_point_in_utc_time,
)

import logging
_LOGGER = logging.getLogger(__name__)

from .logic import SwitchHandler

DOMAIN = "dimmer_button"

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
#PLATFORMS: list[Platform] = [Platform.LIGHT]
PLATFORMS: list[Platform] = None

def yolo():
    _LOGGER.error("YOOOOOOLOOOOO")

async def async_say_hello(hass, target):
    _LOGGER.error("RUNEEEEMEMEMEEMEMEg")
    yolo()

async def async_setup(hass, config):
    #hass.states.async_set("dimmer_button.world", "Paulus")
    
    #_LOGGER.error(config["dimmer_button"])
    dimmer_config = config["dimmer_button"]

    entities = []
    
    switchHandler = SwitchHandler(hass, dimmer_config, handle_sw_event)
    entities = switchHandler.getEntities()
    hass.data.setdefault(DOMAIN, {})["switchhandler"] = switchHandler
    hass.async_create_task(async_say_hello(hass, dimmer_config))
    print(dimmer_config)
    #print(len(dimmer_config["switches"]))
    #entities = []
   
    #_LOGGER.error("HAHA")
    #entities.append("sensor.strombrytare_vardagsrum_action")
    print(entities)

    #hass.bus.async_listen(EVENT_STATE_CHANGED, handl2e_event)
    async_track_state_change_event(hass, entities, switchHandler.incoming_event)
    #hass.bus.listen(EVENT_STATE_CHANGED, handle_event)
    #hass.bus.listen("example_component_my_cool_event", handle_event)
    #_LOGGER.error("HAHA2")
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
    #_LOGGER.error(value)
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
    switchandler = hass.data[DOMAIN]["switchhandler"]
    print(swithandler)
    _LOGGER.error("SICK!")
    _LOGGER.error(value)

