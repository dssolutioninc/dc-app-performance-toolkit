import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_view_rules_configuration(webdriver, datasets):
    page = BasePage(webdriver)
    project_organization = Project(webdriver, project_key=datasets['project_key'])

    @print_timing("selenium_app_customer_organization")

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
        project_organization.go_to_organization_service_configuration__context()
        page.wait_until_present((By.CLASS_NAME, "aui-page-panel-content"))    # Wait for header of administration page present

    measure_user_login()