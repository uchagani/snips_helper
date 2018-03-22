from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

class ConsoleHelper:
    
    LOGIN_URL = 'https://console.snips.ai/login'
    IMPLICIT_DELAY = 30

    def __init__(self, chrome_driver_path='/usr/bin/chromedriver', download_dir=None):
        if download_dir is None:
            download_dir = os.getcwd()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=chrome_driver_path)
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = self.driver.execute("send_command", params)
        self.driver.implicitly_wait(self.IMPLICIT_DELAY)

    def login(self, email, password, assistant=None):
        self.driver.get(self.LOGIN_URL)
        self.handle_cookie_message()
        email_field = self.driver.find_element_by_name('email')
        password_field = self.driver.find_element_by_name('password')
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.submit()

        if assistant is not None:
            self.change_assistant(assistant)
    
    def change_assistant(self, assistant):
        assistant_selector = self.driver.find_element_by_class_name("header-assistants-select")
        assistant_selector.click()
        assistant_options = self.driver.find_element_by_class_name("Select-menu-outer")
        assistant = assistant_options.find_element_by_css_selector("div[aria-label='{}']".format(assistant))
        assistant.click()
    
    def handle_cookie_message(self):
        try:
            cookies_button = self.driver.find_element_by_class_name('cookies-usage-info__ok-button')
            cookies_button.click()
        except:
            return

    def retrain_assistant(self):
        header = self.driver.find_element_by_class_name('header-assistants-select__label')
        header.click()
        bundles = self.driver.find_elements_by_class_name('bundle-section__card')
        first_bundle = bundles[0]
        first_bundle.click()
        intent = self.driver.find_element_by_class_name('assistant-intent__title')
        intent.click()
        save_button = self.driver.find_element_by_class_name('save-intent-button')
        save_button.click()
    
    def get_assistant(self, assistant):
        # Can read the html to get the entire windows state
        # and return the assistant part of it
        assistant = {
            "id": "proj_TEST",
            "title": "Test",
            "userId": "user_TEST",
            "language": "en",
            "analyticsEnabled": true,
            "hotwordId": "jarvis",
            "platform": {
                "type": "id",
                "id": "$Assistant:proj_TEST.platform",
                "generated": true
            },
            "asr": {
                "type": "id",
                "id": "$Assistant:proj_TEST.asr",
                "generated": true
            },
            "__typename": "Assistant",
            "bundles": [{
                "type": "id",
                "id": "Bundle:bundle_TEST",
                "generated": false
            }],
            "training": {
                "type": "id",
                "id": "$Assistant:proj_TEST.training",
                "generated": true
            },
            "languagemodel": {
                "type": "id",
                "id": "$Assistant:proj_TEST.languagemodel",
                "generated": true
            }
        }
        return Assistant(

        def get_bundles(self, assistant, bundle):
            # select the assistant
            # can read the html to get the entire windows state
            # and return the specific bundle as a python dict
            bundle = {"Bundle:bundle_TEST": {
                        "id": "bundle_TEST",
                        "__typename": "Bundle",
                        "name": "Weather",
                        "description": "Ask questions",
                        "language": "en",
                        "userId": "user_TEST",
                        "username": "Snips",
                        "private": false,
                        "canCustomize": null,
                        "imageUrl": "https://console.snips.ai/images/bundles/bundle-sun.svg",
                        "hidden": null,
                        "migrated": null,
                        "forked": null,
                        "statistics": {
                            "type": "id",
                            "id": "$Bundle:bundle_TEST.statistics",
                            "generated": true
                        },
                        "rating": {
                            "type": "id",
                            "id": "$Bundle:bundle_TEST.rating",
                            "generated": true
                        },
                        "intents": [{
                            "type": "id",
                            "id": "PartialIntent:intent_TEST",
                            "generated": false
                        }]
                    }}
            return bundle

    def download_assistant(self, timeout=60):        
        download_button = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[download]")))
        download_button = self.driver.find_element_by_css_selector("[download]")
        download_button.click()

Class Assistant:
    # So assistant now has a list of bundles as self.bundles
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
    def get_bundle(self, bundle)
        """Return a Bundle object."""
        return Bundle(ConsoleHelper.get_bundle(self, bundle))

Class Bundle:
    # So bundle now has a list of intents as self.intents
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def export_slots(self, intent)
        # need to find out slots which have unique ids
        return True

    def export_training_examples(self, intent)
        # these are utterances but pretty straightforward
        return True

    def import_slot(self, intent, slot)
        return True

    def import_training_examples(self, intent)
        # these are utterances but pretty straightforward
        return True

    
