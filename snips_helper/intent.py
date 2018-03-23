import time

class Intent:
    def __init__(self, name, driver):
        print("Creating intent: {}".format(name))
        self.__name = name
        self.__driver = driver

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def utterances(self):
        print("Getting utterances")
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_export_utterance_button().click()
        training_data = self._get_modal_text_area().text.split("\n")
        self.__get_modal_close_button().click()
        self.__deactivate()
        return training_data

    def save(self):
        print("Saving intent: {}".format(self.name))
        self.__activate()
        self.__get_save_button().click()
        time.sleep(1)
        self.__deactivate()

    def __activate(self):
        print("Activating intent: {}".format(self.name))
        self.__get_intent().click()

    def __deactivate(self):
        print("Deactivating intent: {}".format(self.name))
        self.__get_back_to_assistant_button().click()

    def __get_intent(self):
        print("Getting intent: {}".format(self.name))
        selector1 = "//*[contains(@class, 'assistant-intent__title')]"
        selector2 = "[text()='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __get_back_to_assistant_button(self):
        print("Get back to assistant button")
        return self.driver.find_element_by_link_text('Back to Assistant')

    def __get_save_button(self):
        print("Get save button")
        return self.driver.find_element_by_class_name('save-intent-button')

    def __get_export_headers(self):
        print("Get export headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_utterance_section(self):
        print("Get utterance section")
        return self.__get_export_headers()[1]

    def __get_utterance_dot_button(self):
        print("Get utterance dot button")
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name('dots-icon-button')

    def __get_export_utterance_button(self):
        print("Get export utterance button")
        selector = "//*[text()='Export Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_modal(self):
        print("Get modal")
        return self.driver.find_element_by_class_name(
            'modal-dialog__dialog')

    def __get_modal_content(self):
        print("Get modal content")
        modal = self.__get_modal()
        return modal.find_element_by_class_name('modal-dialog__content')

    def _get_modal_text_area(self):
        print("Get utterance text area")
        modal = self.__get_modal_content()
        return modal.find_element_by_tag_name('textarea')

    def __get_modal_close_button(self):
        print("Get modal close button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Close']")
