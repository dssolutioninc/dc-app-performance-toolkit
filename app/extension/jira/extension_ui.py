import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def test_1_view_project_page_jtricks(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_view_global_page_config_jtricks")
    def measure_global_page_config_jtricks():
        # Global page config
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/JQLTricksConfigDefault.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))

    @print_timing("selenium_view_global_page_function_config_jtricks")
    def measure_global_page_function_config_jtricks():
        # Global page function config
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/JQLTricksFnConfigDefault.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))  # Wait for you app-specific UI element by ID selector


    measure_global_page_config_jtricks()
    measure_global_page_function_config_jtricks()