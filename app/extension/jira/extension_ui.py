import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
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

    @print_timing("selenium_view_issue_panel_purgo_ai")
    def measure_issue_panel():
        # Issue panel view
        test_issue_key = "AANES-469" # ensure this issue exists in Jira
        
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{test_issue_key}")
        page.wait_until_visible((By.ID, "purgo-issue-panel-view"))

    @print_timing("selenium_project_setting_purgo_ai")
    def measure_project_setting():
        # Project settings view
        test_project_key = "AANES" # ensure this project exists in Jira
        
        page.go_to_url(
            f"{JIRA_SETTINGS.server_url}/secure/ProjectSettings.jspa?projectKey={test_project_key}")
        page.wait_until_visible((By.ID, "purgo-ai-project-settings-view"))

    @print_timing("selenium_admin_page_purgo_ai")
    def measure_admin_page():
        # Admin page view
        page.go_to_url(
            f"{JIRA_SETTINGS.server_url}/secure/AdminPage.jspa")
        page.wait_until_visible((By.ID, "purgo-ai-admin-page-view"))

    measure_issue_panel()
    measure_project_setting()
    measure_admin_page()
