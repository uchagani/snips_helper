from .intent import Intent


class Bundle:
    def __init__(self, name, driver):
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
        self.__get_bundle().click()

    def get_intents(self):
        self.__activate()
        intent_elements = self.driver.find_elements_by_class_name(
            'assistant-intent__title')

        intents = []
        for intent in intent_elements:
            intents.append(Intent(intent.text, self.driver))

        return intents
