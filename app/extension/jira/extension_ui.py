import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage
from util.conf import JIRA_SETTINGS


def test_1_view_project_page_xstudio(webdriver, datasets):
    page = BasePage(webdriver)

    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.wait_for_login_page_loaded()
            login_page.set_credentials(username=username, password=password)
            login_page.wait_for_dashboard_or_first_login_loaded()
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
            # uncomment below line to do web_sudo and authorise access to admin pages
            # AdminPage(webdriver).go_to(password=password)
    
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_view_global_page_config_xstudio")
    def measure_global_page_config_xstudio():
        # Global page config
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/XStudioIntegrationConfigAction.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))

    @print_timing("selenium_view_global_page_function_config_xstudio")
    def measure_global_page_function_config_xstudio():
        # Global page function config
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/XStudioIntegrationConfigAction.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))  # Wait for you app-specific UI element by ID selector


    measure_global_page_config_xstudio()
    measure_global_page_function_config_xstudio()

