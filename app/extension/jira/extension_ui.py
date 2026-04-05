import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage
from util.conf import JIRA_SETTINGS

XSTUDIO_ISSUE_KEYS = ['AANES-469', 'AANES-467', 'AANES-385']


def test_1_view_xstudio_config_page(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_xstudio_admin_login")
    def measure_login():
        login_page = Login(webdriver)
        login_page.delete_all_cookies()
        login_page.go_to()
        login_page.wait_for_login_page_loaded()
        login_page.set_credentials(username='admin', password='admin')
        login_page.wait_for_dashboard_or_first_login_loaded()
        if login_page.is_first_login():
            login_page.first_login_setup()
        if login_page.is_first_login_second_page():
            login_page.first_login_second_page_setup()
        login_page.wait_for_page_loaded()
        AdminPage(webdriver).go_to(password='admin')

    measure_login()

    @print_timing("selenium_view_xstudio_config_page")
    def measure_config():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/admin/XStudioIntegrationConfigAction.jspa")
        page.wait_until_visible((By.CLASS_NAME, 'aui-page-panel'))

    measure_config()


def test_2_view_xstudio_issue_tab(webdriver, datasets):
    page = BasePage(webdriver)
    issue_key = random.choice(XSTUDIO_ISSUE_KEYS)

    @print_timing("selenium_view_xstudio_issue_tab")
    def measure_issue_tab():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
        page.wait_until_visible((By.ID, 'summary-val'))
        page.wait_until_present((By.ID, 'issuetabpanel-xstudiointegration'))

    measure_issue_tab()
