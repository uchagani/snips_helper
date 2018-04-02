import time
import logging

class Intent:
    def __init__(self, name, driver):
        self.logger = logging.getLogger('snips_helper')
        self.logger.debug("Creating intent: {}".format(name))
        self.__name = name
        self.__driver = driver

    @property
    def name(self):
        return self.__name

    @property
    def driver(self):
        return self.__driver

    def utterances(self):
        self.logger.debug("Getting utterances")
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_export_utterance_button().click()
        training_data = self.__get_modal_text_area().text.split("\n")
        self.__get_modal_close_button().click()
        self.__deactivate()
        return training_data

    def slots(self):
        self.logger.debug("Getting slots")
        self.__activate()
        self.__get_slots_dot_button().click()
        self.__get_export_slots_button().click()
        slots = self.__get_modal_text_area().text.split("\n")
        self.__get_modal_close_button().click()
        self.__deactivate()
        if slots == ['']: slots = []
        return slots

    def export_slot_values(self, slot):
        self.logger.debug("Getting slot: {}".format(slot))
        self.__activate()
        if self.__get_slot_editor_button(slot):
            self.__get_slot_editor_button(slot).click()
        else:
            self.logger.debug("No slots found {}".format(self.__get_slot_editor_button(slot)))
            self.__deactivate()
            return None
        self.__get_slot_modal_export_button().click()
        slot_values = self.__get_modal_text_area().text.split("\n")
        self.__get_slot_modal_dialog_close_button().click()
        self.__get_slot_modal_close_button().click()
        self.__deactivate()
        return slot_values

    def import_slot_values(self, slot, slot_values):
        self.logger.debug("Getting slot: {}".format(slot))
        existing_slots = [x + '\n' for x in self.export_slot_values(slot)]
        slots = (existing_slots +
                 list(set(slot_values) - set(existing_slots)))
        self.__activate()
        if self.__get_slot_editor_button(slot):
            self.__get_slot_editor_button(slot).click()
        else:
            self.logger.debug("No slots found {}".format(
                self.__get_slot_editor_button(slot)))
            self.__deactivate()
            return None
        self.__get_slot_modal_import_button().click()
        self.__get_modal_text_area().send_keys(slots)
        self.__get_modal_import_button().click()
        self.__get_slot_modal_close_button().click()
        self.__deactivate()
        return slots

    def import_utterances(self, utterances):
        self.logger.debug("Importing utterances")
        existing_utterances = [x + '\n' for x in self.utterances()]
        imported_utterances = (existing_utterances +
                               list(set(utterance) - set(existing_utterances)))
        self.__activate()
        self.__get_utterance_dot_button().click()
        self.__get_import_utterance_button().click()
        self.__get_modal_text_area().send_keys(utterances)
        self.__get_modal_import_button().click()
        time.sleep(1)
        self.save()
        self.__deactivate()
        return imported_utterances

    def delete_utterances(self):
        self.logger.debug("Deleting utterances")
        self.__activate()
        while self.__get_utterance_delete_button():
            self.__get_utterance_delete_button().click()
        self.save()
        return

    def save(self):
        self.logger.debug("Saving intent: {}".format(self.name))
        if not self.__get_save_button():
            self.__activate()
        self.__get_save_button().click()
        time.sleep(1)
        self.__deactivate()

    def __activate(self):
        self.logger.debug("Activating intent: {}".format(self.name))
        self.__get_intent().click()

    def __deactivate(self):
        self.logger.debug("Deactivating intent: {}".format(self.name))
        self.__get_back_to_assistant_button().click()

    def __get_intent(self):
        self.logger.debug("Getting intent: {}".format(self.name))
        selector1 = "//*[contains(@class, 'assistant-intent__title')]"
        selector2 = "[text()='{}']".format(self.name)
        selector = selector1 + selector2
        return self.driver.find_element_by_xpath(selector)

    def __get_back_to_assistant_button(self):
        self.logger.debug("Get back to assistant button")
        return self.driver.find_element_by_link_text('Back to Assistant')

    def __get_save_button(self):
        self.logger.debug("Get save button")
        return self.driver.find_element_by_class_name('save-intent-button')

    def __get_export_headers(self):
        self.logger.debug("Get export headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_import_headers(self):
        self.logger.debug("Get import headers")
        return self.driver.find_elements_by_class_name(
            'intent-editor-section-header')

    def __get_utterance_section(self):
        self.logger.debug("Get utterance section")
        return self.__get_export_headers()[1]

    def __get_utterance_delete_button(self):
        self.logger.debug("Get utterance delete button")
        selector = 'button--unstyled'
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name(selector)

    def __get_utterance_dot_button(self):
        self.logger.debug("Get utterance dot button")
        utterance_section = self.__get_utterance_section()
        return utterance_section.find_element_by_class_name('dots-icon-button')

    def __get_export_utterance_button(self):
        self.logger.debug("Get export utterance button")
        selector = "//*[text()='Export Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_import_utterance_button(self):
        self.logger.debug("Get import utterance button")
        selector = "//*[text()='Import Training Examples']"
        return self.driver.find_element_by_xpath(selector)

    def __get_slots_section(self):
        self.logger.debug("Get slots section")
        return self.__get_export_headers()[0]

    def __get_slots_dot_button(self):
        self.logger.debug("Get slots dot button")
        slot_section = self.__get_slots_section()
        return slot_section.find_element_by_class_name('dots-icon-button')

    def __get_export_slots_button(self):
        self.logger.debug("Get export slots button")
        selector = "//*[text()='Export Slots']"
        return self.driver.find_element_by_xpath(selector)

    def __get_import_slots_button(self):
        self.logger.debug("Get import slots button")
        selector = "//*[text()='Import Slots']"
        return self.driver.find_element_by_xpath(selector)

    def __get_slots_island(self):
        self.logger.debug("Get slot island")
        return self.driver.find_elements_by_class_name('island--with-row')[0]

    def __get_slot_editors(self):
        self.logger.debug("Get slots editors")
        slots_island = self.__get_slots_island()
        return slots_island.find_elements_by_class_name('slot-editor')

    def __get_slot_editor_row(self, slot):
        self.logger.debug("Get slot editor row")
        for editor in self.__get_slot_editors():
            slot_name = editor.find_element_by_class_name(
                'slot-editor__name').get_attribute('value')
            if slot == slot_name:
                return editor

    def __get_slot_editor_button(self, slot):
        self.logger.debug("Get slot editor button")
        editor_row = self.__get_slot_editor_row(slot)
        if not editor_row:
            return None
        if editor_row.find_element_by_class_name(
                'item-option__subtitle').text == 'builtin':
            return None
        editor_button = editor_row.find_element_by_class_name(
                'slot-editor--action-button')
        self.driver.execute_script(
            "arguments[0].setAttribute('style','visibility:visible;');",
            editor_button)
        return editor_button

    def __get_slot_modal(self):
        self.logger.debug("Get slot modal")
        return self.driver.find_element_by_class_name(
            'fullscreen-modal')

    def __get_slot_modal_content(self):
        self.logger.debug("Get slot modal content")
        modal = self.__get_slot_modal()
        return modal.find_element_by_class_name('fullscreen-modal__content')

    def __get_slot_modal_export_button(self):
        self.logger.debug("Get slot modal export button")
        modal_content = self.__get_slot_modal_content()
        export_button = modal_content.find_element_by_xpath("//*[text()=' Export']")
        self.driver.execute_script(
                "return arguments[0].scrollIntoView();", export_button)
        return export_button

    def __get_slot_modal_import_button(self):
        self.logger.debug("Get slot modal import button")
        modal_content = self.__get_slot_modal_content()
        import_button = modal_content.find_element_by_xpath("//*[text()=' Import']")
        self.driver.execute_script(
                "return arguments[0].scrollIntoView();", import_button)
        return import_button

    def __get_slot_modal_dialog_close_button(self):
        modal = self.__get_modal()
        return modal.find_element_by_class_name("modal-dialog__closeundefined")

    def __get_slot_modal_close_button(self):
        modal = self.__get_slot_modal()
        close_button = modal.find_element_by_xpath("//*[text()='Close']")
        self.driver.execute_script(
                "return arguments[0].scrollIntoView();", close_button)
        return close_button

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

    def __get_modal_close_button(self):
        self.logger.debug("Get modal close button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Close']")

    def __get_modal_import_button(self):
        self.logger.debug("Get modal import button")
        modal = self.__get_modal()
        return modal.find_element_by_xpath("//*[text()='Import']")
