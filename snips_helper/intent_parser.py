import logging
import json
from .slot_parser import SlotParser

class IntentParser:

    def __init__(self, data):
        self.logger = logging.getLogger('snips_helper')
        self.__raw_data = data
        self.__parsed_data = self.parse_data(self.__raw_data)

    def parse_data(self, data):
        parsed_data = json.loads(data)
        self.__session_id = parsed_data['sessionId']
        self.__custom_data = parsed_data['customData']
        self.__site_id = parsed_data['siteId']
        self.__input_text = parsed_data['input']
        self.__name = parsed_data['intent']['intentName']
        self.__probability = parsed_data['intent']['probability']

        slots = parsed_data['slots']
        parsed_slots = []
        for slot in slots:
            parsed_slots.append(SlotParser(slot))

        self.__slots = parsed_slots

        return parsed_data


    @property
    def name(self):
        return self.__name

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def parsed_data(self):
        return self.__parsed_data

    @property
    def session_id(self):
        return self.__session_id

    @property
    def custom_data(self):
        return self.__custom_data

    @property
    def site_id(self):
        return self.__site_id

    @property
    def input_text(self):
        return self.__input_text

    @property
    def probability(self):
        return self.__probability

    @property
    def slots(self):
        return self.__slots


