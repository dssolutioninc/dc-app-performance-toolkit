import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, AdvancedTabs
from util.conf import CONFLUENCE_SETTINGS


def test_1_view_page_with_advanced_tabs(webdriver, datasets):
    page = BasePage(webdriver)
    advanced_tabs = AdvancedTabs(webdriver)

    @print_timing("selenium_view_page_with_advanced_tabs")
    def measure_user_login(username='admin', password='admin'):
        login_page = Login(webdriver)
        login_page.delete_all_cookies()
        login_page.go_to()
        login_page.wait_for_page_loaded()
        login_page.set_credentials(username=username, password=password)
        login_page.click_login_button()
        if login_page.is_first_login():
            login_page.first_user_setup()
        all_updates_page = AllUpdates(webdriver)
        all_updates_page.wait_for_page_loaded()

        # go to configuration page
        advanced_tabs.go_to_page_with_advanced_tabs()
        advanced_tabs.wait_until_present((By.CLASS_NAME, "advanced-tabs-container"))
    measure_user_login()
