from .intent import Intent
import time
import logging


class Bundle:
    def __init__(self, name, driver):
        self.logger = logging.getLogger('snips_helper')
        self.logger.debug("Creating bundle: {}".format(name))
        self.__name = name
        self.__driver = driver

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def __get_bundle(self):
        selector1 = "//*[contains(@class, 'bundle-header__title')]"
        selector2 = "[@title='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __activate(self):
        self.logger.debug("Selecting bundle: {}".format(self.name))
        self.__get_bundle().click()

    def get_intents(self):
        self.logger.debug("Getting intents for: {}".format(self.name))
        self.__activate()
        intent_elements = self.driver.find_elements_by_class_name(
            'assistant-intent__title')

        intents = []
        for intent in intent_elements:
            intents.append(Intent(intent.text, self.driver))

        return intents

    def create_intent(self, intent, slots, utterances):
        self.logger.debug("Creating new intent: {}".format(intent))

        for existing_intent in self.get_intents():
            if existing_intent.name == intent:
                self.logger.debug("intent exists: {}".format(intent))
                return None
        self.__get_create_intent_button().click()
        self.__set_intent_name().send_keys(intent)
        self.__get_utterance_dot_button().click()
        self.__get_import_utterance_button().click()
        self.__get_modal_text_area().send_keys('\n'.join(utterances))
        self.__get_modal_import_button().click()
        time.sleep(1)
        self.save_intent()
        return intent

    def save_intent(self):
        self.logger.debug("Saving intent")
        self.__get_save_button().click()
        time.sleep(1)
        self.__deactivate()

    def __deactivate(self):
        self.logger.debug("Deactivating intent")
        self.__get_back_to_assistant_button().click()

    def __get_back_to_assistant_button(self):
        self.logger.debug("Get back to assistant button")
        return self.driver.find_element_by_link_text('Back to Assistant')

    def __get_save_button(self):
        self.logger.debug("Get save button")
        return self.driver.find_element_by_class_name('save-intent-button')

    def __get_create_intent_button(self):
        self.logger.debug("Get create intent button")
        return self.driver.find_element_by_xpath("//*[text()='Create new Intent']")

    def __set_intent_name(self):
        self.logger.debug("Get name input button")
        return self.driver.find_element_by_name('intentName')

    def __get_import_headers(self):
        self.logger.debug("Get import headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_utterance_section(self):
        self.logger.debug("Get utterance section")
        return self.__get_import_headers()[1]

    def __get_utterance_dot_button(self):
        self.logger.debug("Get utterance dot button")
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name('dots-icon-button')

    def __get_import_utterance_button(self):
        self.logger.debug("Get import utterance button")
        selector = "//*[text()='Import Training Examples']"
        return self.driver.find_element_by_xpath(selector)

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

    def __get_modal_import_button(self):
        self.logger.debug("Get modal import button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Import']")
