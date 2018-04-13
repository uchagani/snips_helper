import logging
import json

class SlotParser:
    def __init__(self, slot_data):
        self.__raw_value = slot_data['rawValue']
        self.__value = slot_data['value']['value']
        self.__name = slot_data['slotName']

    @property
    def raw_value(self):
        return self.__raw_value

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__name