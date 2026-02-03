import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage, Project
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    project_page_cl = Project(webdriver, project_key=datasets['current_session']['project_key'])

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.wait_for_login_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.wait_for_dashboard_or_first_login_loaded()
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #         # uncomment below line to do web_sudo and authorise access to admin pages
    #         # AdminPage(webdriver).go_to(password=password)
    #
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_view_project_page_cl")
    def measure_project_page():
        # Project page
        project_page_cl.go_to_project_page_cl()
        project_page_cl.wait_for_project_page_cl()

    @print_timing("selenium_view_global_page_cl")
    def measure_global_page():
        # Global page
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/ChecklistAdminConfigAction.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))  # Wait for you app-specific UI element by ID selector

    measure_project_page()
    measure_global_page()
