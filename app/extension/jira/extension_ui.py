import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_1_view_application_setting_page(webdriver, datasets):
    page = BasePage(webdriver)
    application_setting_page = Project(webdriver, project_key=datasets['current_session']['project_key'])

    @print_timing("selenium_view_application_setting_page")
    def measure_application_setting_page():
        # Project page
        application_setting_page.go_to_application_setting_page()
        application_setting_page.wait_for_application_setting_page()

    measure_application_setting_page()

