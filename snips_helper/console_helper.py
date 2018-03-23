from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from .bundle import Bundle


class ConsoleHelper:
    LOGIN_URL = 'https://console.snips.ai/login'
    IMPLICIT_DELAY = 30

    def __init__(self, chrome_driver_path='/usr/bin/chromedriver',
                 download_dir=None, headless=True):
        if download_dir is None:
            download_dir = os.getcwd()

        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,
                                       executable_path=chrome_driver_path)

        self.driver.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow',
                             'downloadPath': download_dir}}

        self.driver.execute("send_command", params)
        self.driver.implicitly_wait(self.IMPLICIT_DELAY)

        self.driver.set_window_position(0,0)
        self.driver.set_window_size(4096, 2160)
        self.driver.maximize_window()

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
        assistant_selector = self.driver.find_element_by_class_name(
            "header-assistants-select")
        assistant_selector.click()
        assistant_options = self.driver.find_element_by_class_name(
            "Select-menu-outer")
        assistant = assistant_options.find_element_by_css_selector(
            "div[aria-label='{}']".format(assistant))
        assistant.click()

    def handle_cookie_message(self):
        try:
            cookies_button = self.driver.find_element_by_class_name(
                'cookies-usage-info__ok-button')
            cookies_button.click()
        except:
            return

    def get_header(self):
        return self.driver.find_element_by_class_name(
            'header-assistants-select__label')

    def get_bundles(self):
        bundle_elements = self.driver.find_elements_by_class_name(
            'bundle-header__title')
        bundles = []
        for bundle_element in bundle_elements:
            bundles.append(Bundle(bundle_element.text, self.driver))

        return bundles

    def retrain_assistant(self):
        self.get_header().click()
        bundle = self.get_bundles()[0]
        intent = bundle.get_intents()[0]
        intent.save()

    def get_download_button(self, timeout):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[download]")))

    def get_download_close_button(self, timeout):
        download_modal = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "download-assistant-modal")))

        return WebDriverWait(download_modal, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[text()='Close']")))

    def download_assistant(self, timeout=120):
        self.get_download_button(timeout).click()
        self.get_download_close_button(timeout).click()
