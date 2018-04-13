import time
import logging


class SlotType:
    def __init__(self, name, driver):
        self.logger = logging.getLogger('snips_helper')
        self.logger.debug("Creating slot type: {}".format(name))
        self.__name = name
        self.__driver = driver

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def edit(self, slot_values):
        self.logger.debug("Modifying slot values")
        self.__activate()
        return

    def manual_values(self):
        self.__get_export_button().click()
        manual_values = self.__get_modal_text_area().text.split("\n")
        return self.__format_manual_values_dict(manual_values)

    def __activate(self):
        self.logger.debug("Activating slot values window")
        self.__get_slot_type().click()

    def __get_slot_type(self):
        selector1 = "//*[contains(@class, 'item-option__title')]"
        selector2 = "[@title='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __get_export_button(self):
        modal = self.__get_modal()
        self.driver.find_element_by_xpath("//*[text()='Export']")

    def __get_modal(self):
        self.logger.debug("Get modal")
        return self.driver.find_element_by_class_name(
            'modal-dialog__dialog')

    def __get_modal_content(self):
        self.logger.debug("Get modal content")
        modal = self.__get_modal()
        return modal.find_element_by_class_name('modal-dialog__content')

    def __get_modal_text_area(self):
        self.logger.debug("Get text area")
        modal = self.__get_modal_content()
        return modal.find_element_by_tag_name('textarea')

    def __format_manual_values_dict(self, manual_values):
        return manual_values