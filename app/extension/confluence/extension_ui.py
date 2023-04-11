import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, MeeticalForConfluence
from util.conf import CONFLUENCE_SETTINGS


def test_1_view_meetical_for_confluence(webdriver, datasets):
    page = BasePage(webdriver)
    meetical_for_confluence = MeeticalForConfluence(webdriver)

    @print_timing("selenium_view_meetical_for_confluence")
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

        meetical_for_confluence.go_to_meetical_for_confluence_configuration()
        if meetical_for_confluence.element_exists((By.CLASS_NAME, "aui-message-warning")):
            meetical_for_confluence.get_element((By.ID, "password")).send_keys(password)
            meetical_for_confluence.wait_until_visible((By.ID, "authenticateButton")).click()
        meetical_for_confluence.wait_until_present((By.CLASS_NAME, "aui-page-header-main"))    # Wait for header of administration page present

    measure_user_login()
