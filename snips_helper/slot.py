import time
import logging

class Slot:
    def __init__(self, name, driver, slot_type, slot_required=False,
                 follow_up_quesion=None):
        self.logger = logging.getLogger('snips_helper')
        self.logger.debug("Creating slot: {}".format(name))
        self.__name = name
        self.__driver = driver
        self.__slot_type = slot_type
        self.__slot_required = slot_required
        self.__follow_up_quesion = follow_up_quesion

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    @property
    def type(self):
        return self.__slot_type

    @property
    def required(self):
        return self.__slot_required

    @property
    def follow_up_quesion(self):
        return self.__follow_up_quesion

    def export_value(self):
        export = self.name

        if self.type:
            export = "{}, {}".format(export, str(self.type).lower())

        if self.required:
            export =  "{}, {}".format(export, str(self.required).lower())

        if self.follow_up_quesion:
            export = "{}, {}".format(export, self.follow_up_quesion)

        return export

