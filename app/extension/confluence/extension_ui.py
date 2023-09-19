import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, StatusMacroConfiguration
from util.conf import CONFLUENCE_SETTINGS


def test_1_view_status_macro_configuration(webdriver, datasets):
    page = BasePage(webdriver)
    status_macro_configuration = StatusMacroConfiguration(webdriver)

    @print_timing("selenium_view_status_marco_configuration")
    def measure():
        login_page = Login(webdriver)
        login_page.delete_all_cookies()
        login_page.go_to()
        login_page.wait_for_page_loaded()
        login_page.set_credentials(username='admin', password='admin')
        login_page.click_login_button()
        if login_page.is_first_login():
            login_page.first_user_setup()
        status_macro_configuration.go_to_status_macro_configuration()
        status_macro_configuration.wait_until_present((By.ID, "admin-heading-container"))
    measure()
