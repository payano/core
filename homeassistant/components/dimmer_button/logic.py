from enum import Enum
from threading import Thread, Lock
import time
import homeassistant.core as ha
import yaml


class State(Enum):
    OFF           = 1
    ON            = 2
class CallbackState(Enum):
    LONG_PRESSED  = 1
    SHORT_PRESSED = 2

class StateMachine:
    def __init__(self):
        self._state = State.OFF
        self._lock = Lock()

    def get_state(self):
        ret = self._state
        return ret

    def update_state(self, new_state):
        if(self._state == new_state):
            return
        print("update_state")
        self._lock.acquire()
        self._state = new_state
        self._lock.release()

class Button:
    def __init__(self, index, sleep_time, event_callback):
        self.sm = StateMachine()
        self.delay_running = False        
        self.event_callback = event_callback
        self.index = index
        self.sleep_time = sleep_time

    def delay_on(self, data):
        if(self.delay_running == True):
            return
        self.delay_running = True
        time.sleep(self.sleep_time)
        returnValue = {}
        returnValue["id"] = self.index
        if(self.sm.get_state() == State.OFF):
            print("loop")
            returnValue["event"] = CallbackState.SHORT_PRESSED
            self.event_callback(returnValue)

        while self.sm.get_state() == State.ON:
            returnValue["event"] = CallbackState.LONG_PRESSED
            self.event_callback(returnValue)
            time.sleep(self.sleep_time)
        self.delay_running = False

    def input(self, data):
        print("Button")
        if "press" in data:
            self.sm.update_state(State.ON)
            self.delay_on(data)
        elif "release" in data:
            self.sm.update_state(State.OFF)

class Switch:
    def __init__(self, sleep_time, no_of_buttons, entity, callback):
        self.no_of_buttons = no_of_buttons
        self.callback = callback
        self.entity = entity
        self.buttons = []

        for index in range(no_of_buttons):
            self.buttons.append(Button(index+1, sleep_time, self.__callback__))

    def __callback__(self, value):
        value["entity"] = self.entity
        self.callback(value)

    def input(self, data):
        print("swt")
        print(data)
        values = data["event"].split("_")
        print(len(values))
        if(len(values) != 2):
            return

        index = int(values[1]) - 1
        data = values[0]
        print("switch")
        if(index >= self.no_of_buttons and index < 0):
            print("ERROR! ")
            return
        self.buttons[index].input(data)

# this will be HASS specifc stuff...
class SwitchHandler:
    def __init__(self, hass, config, callback):
        print(config)
        self.hass = hass
        self.config = config
        self.switch = {}
        self.entities = []
        sleep_time = config["sleep_time"]
        self.entitymap = {}

        for switch in config["switches"]:
            sw_conf = switch["switch"]
            entity = sw_conf["entity"]
            self.entities.append(entity)
            self.entitymap[entity] = {}

            no_of_buttons = sw_conf["no_of_buttons"]
            for button in sw_conf["buttons"]:
                buttonid = button["button"]
                target = button["target"]
                pressed = button["pressed"]
                released = button["released"]
                shortpressed = button["shortpressed"]
                longpressed = button["longpressed"]

                self.entitymap[entity][buttonid] = {}

                self.entitymap[entity][buttonid]["target"] = target
                self.entitymap[entity][buttonid]["pressed"] = pressed
                self.entitymap[entity][buttonid]["released"] = released
                self.entitymap[entity][buttonid]["shortpressed"] = shortpressed
                self.entitymap[entity][buttonid]["longpressed"] = longpressed

            self.switch[entity] = Switch(sleep_time, no_of_buttons, entity, self.__cb_method)

    def __cb_method(self, event):
        item = self.entitymap[event["entity"]][event["id"]] 
        retVal = {}
        retVal["target"] = item["target"]
        if event["event"] == CallbackState.LONG_PRESSED:
            retVal["action"] = item["longpressed"]
        else:
            retVal["action"] = item["shortpressed"]
        
        #lamp = self.hass.states.get("light.vet_ej")
        #service_data = {"entity_id": entity_id, "rgb_color": rgb_color, "brightness": 255}
        #service_data = {"entity_id": "light.vet_ej"}
        print(item)
        service_data = {"entity_id": "light.vet_ej", "brightness_step_pct" : "10"}
        self.hass.services.call("light", "turn_on", service_data, False)

    def input(self, data):
        entity = data["entity"]
        event = data["event"]
        self.switch[entity].input(data)

    def getEntities(self):
        return self.entities

    @ha.callback
    def incoming_event(self, value):
        indata = {}
        entity_id = value.data["entity_id"]
        new_state = value.data["new_state"].state
        indata["entity"] = entity_id
        indata["event"] = new_state
        print(indata)
        self.thread = Thread(target=self.input, args=(indata,))
        self.thread.start()
        


def callback(self, n):
    print("do specific hass implementation here:")
    lamp = self.hass.states.get("light.vet_ej")
    print(lamp)
    print(n)

def update_input(s, data):
    thread = Thread(target=s.input, args=(data,))
    thread.start()

if __name__ == '__main__':
    config = None
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


    dimmer_config = config["dimmer_button"]
    switchHandler = SwitchHandler(dimmer_config, callback)

    indata = {}
    indata["entity"] = "mybutton1"
    indata["event"] = "press_2"
    #switchHandler.input(indata)
    update_input(switchHandler, indata)
    time.sleep(0.4)
    indata["event"] = "release_1"
    update_input(switchHandler, indata)
    time.sleep(0.4)
    indata["event"] = "release_2"
    update_input(switchHandler, indata)

'''
    config = None
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    dimmer_config = config["dimmer_button"]
    #print(dimmer_config)

    sleep_time = dimmer_config["sleep_time"]

    for switch in dimmer_config["switches"]:
        sw_conf = switch["switch"]
        no_of_buttons = sw_conf["no_of_buttons"]
        #print(no_of_buttons)
        button = sw_conf["entity"]
        print(sw_conf["buttons"])


    index = 1
    sw = Switch(index, 0.5, 4, callback)
    data = "1_on"
    update_input(sw, data)
    time.sleep(0.1)
    data = "2_on"
    update_input(sw, data)
    time.sleep(0.1)
    data = "3_on"
    update_input(sw, data)
    time.sleep(0.1)
    data = "4_on"
    update_input(sw, data)
    time.sleep(0.1)

    time.sleep(0.1)
    data = "4_off"
    update_input(sw, data)
    time.sleep(0.1)
    data = "3_off"
    update_input(sw, data)
    time.sleep(0.1)
    data = "2_off"
    update_input(sw, data)
    time.sleep(0.1)
    data = "1_off"
    update_input(sw, data)
    time.sleep(0.1)

    s = Button(0.5, callback)
    data = "on"
    update_input(s, data)
    time.sleep(0.1)
    data = "off"
    update_input(s, data)
    time.sleep(1)
    data = "off"
    update_input(s, data)
    time.sleep(1)
    data = "on"
    update_input(s, data)
    time.sleep(3)
    data = "off"
    update_input(s, data)
    s = None
    '''
