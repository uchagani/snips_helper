import time

class Intent:
    def __init__(self, name, driver, debug):
        if debug: print("Creating intent: {}".format(name))
        self.__name = name
        self.__driver = driver
        self.__debug = debug

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def utterances(self):
        if self.__debug: print("Getting utterances")
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_export_utterance_button().click()
        training_data = self.__get_modal_text_area().text.split("\n")
        self.__get_modal_close_button().click()
        self.__deactivate()
        return training_data

    def import_utterances(self, utterances):
        if self.__debug: print("Importing utterances")
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_import_utterance_button().click()
        self.__get_modal_text_area().send_keys(utterances)
        self.__get_modal_import_button().click()
        time.sleep(1)
        self.save()
        return

    def delete_utterances(self):
        if self.__debug: print("Deleting utterances")
        self.__activate()
        while self.__get_utterance_delete_button():
            self.__get_utterance_delete_button().click()
        self.save()
        return

    def save(self):
        if self.__debug: print("Saving intent: {}".format(self.name))
        if not self.__get_save_button():
            self.__activate()
        self.__get_save_button().click()
        time.sleep(1)
        self.__deactivate()

    def __activate(self):
        if self.__debug: print("Activating intent: {}".format(self.name))
        self.__get_intent().click()

    def __deactivate(self):
        if self.__debug: print("Deactivating intent: {}".format(self.name))
        self.__get_back_to_assistant_button().click()

    def __get_intent(self):
        if self.__debug: print("Getting intent: {}".format(self.name))
        selector1 = "//*[contains(@class, 'assistant-intent__title')]"
        selector2 = "[text()='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __get_back_to_assistant_button(self):
        if self.__debug: print("Get back to assistant button")
        return self.driver.find_element_by_link_text('Back to Assistant')

    def __get_save_button(self):
        if self.__debug: print("Get save button")
        return self.driver.find_element_by_class_name('save-intent-button')

    def __get_export_headers(self):
        if self.__debug: print("Get export headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_import_headers(self):
        if self.__debug: print("Get import headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_utterance_section(self):
        if self.__debug: print("Get utterance section")
        return self.__get_export_headers()[1]

    def __get_utterance_delete_button(self):
        if self.__debug: print("Get utterance delete button")
        selector = 'button--unstyled'
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name(selector)

    def __get_utterance_dot_button(self):
        if self.__debug: print("Get utterance dot button")
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name('dots-icon-button')

    def __get_export_utterance_button(self):
        if self.__debug: print("Get export utterance button")
        selector = "//*[text()='Export Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_import_utterance_button(self):
        if self.__debug: print("Get import utterance button")
        selector = "//*[text()='Import Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_modal(self):
        if self.__debug: print("Get modal")
        return self.driver.find_element_by_class_name(
            'modal-dialog__dialog')

    def __get_modal_content(self):
        if self.__debug: print("Get modal content")
        modal = self.__get_modal()
        return modal.find_element_by_class_name('modal-dialog__content')

    def __get_modal_text_area(self):
        if self.__debug: print("Get utterance text area")
        modal = self.__get_modal_content()
        return modal.find_element_by_tag_name('textarea')

    def __get_modal_close_button(self):
        if self.__debug: print("Get modal close button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Close']")

    def __get_modal_import_button(self):
        if self.__debug: print("Get modal import button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Import']")
