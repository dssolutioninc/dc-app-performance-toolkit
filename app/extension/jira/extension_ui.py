import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_1_view_project_specific(webdriver, datasets):
    page = BasePage(webdriver)
    project_specific = Project(webdriver, project_key=datasets['project_key'])

    @print_timing("selenium_view_project_specific")
    def measure():
        # Statistics panel
        project_specific.go_to_project_specific_statistics()
        project_specific.wait_for_project_specific()

        # Manage Options panel
        project_specific.go_to_project_specific_manage_options()
        project_specific.wait_for_project_specific()

    @print_timing("selenium_view_project_specific_user_login")
    def measure_user_login():
        login_page = Login(webdriver)
        login_page.delete_all_cookies()
        login_page.go_to()
        login_page.set_credentials(username='admin', password='admin')
        if login_page.is_first_login():
            login_page.first_login_setup()
        if login_page.is_first_login_second_page():
            login_page.first_login_second_page_setup()
        login_page.wait_for_page_loaded()

        # Manage Custom Field Contexts panel
        project_specific.go_to_project_specific_custom_field_context()
        page.wait_until_present((By.CLASS_NAME, "aui-page-header-main"))    # Wait for header of administration page present

    measure()
    measure_user_login()

