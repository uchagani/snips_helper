import time

class Intent:
    def __init__(self, name, driver):
        self.__name = name
        self.__driver = driver

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def utterances(self):
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_export_utterance_button().click()
        training_data = self._get_modal_text_area().text.split("\n")
        self.__get_modal_close_button().click()
        self.__deactivate()
        return training_data

    def save(self):
        self.__activate()
        self.__get_save_button().click()
        time.sleep(1)
        self.__deactivate()

    def __activate(self):
        self.__get_intent().click()

    def __deactivate(self):
        self.__get_back_to_assistant_button().click()

    def __get_intent(self):
        selector1 = "//*[contains(@class, 'assistant-intent__title')]"
        selector2 = "[text()='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __get_back_to_assistant_button(self):
        return self.driver.find_element_by_link_text('Back to Assistant')

    def __get_save_button(self):
        return self.driver.find_element_by_class_name('save-intent-button')

    def __get_export_headers(self):
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_utterance_section(self):
        return self.__get_export_headers()[1]

    def __get_utterance_dot_button(self):
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name('dots-icon-button')

    def __get_export_utterance_button(self):
        selector = "//*[text()='Export Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_modal(self):
        return self.driver.find_element_by_class_name(
            'modal-dialog__dialog')

    def __get_modal_content(self):
        modal = self.__get_modal()
        return modal.find_element_by_class_name('modal-dialog__content')

    def _get_modal_text_area(self):
        modal = self.__get_modal_content()
        return modal.find_element_by_tag_name('textarea')

    def __get_modal_close_button(self):
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Close']")
