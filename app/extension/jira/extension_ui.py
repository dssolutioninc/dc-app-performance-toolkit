import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_1_view_project_page_timela(webdriver, datasets):
    page = BasePage(webdriver)
    project_page_timela = Project(webdriver, project_key=datasets['current_session']['project_key'])

    @print_timing("selenium_view_project_page_timela")
    def measure_project_page():
        # Project page
        project_page_timela.go_to_project_page_timela()
        project_page_timela.wait_for_project_page_timela()

    @print_timing("selenium_view_global_page_timela")
    def measure_global_page():
        # Global page
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/TimelaGeneralPage.jspa")
        page.wait_until_visible((By.ID, 'general-page-root'))  # Wait for you app-specific UI element by ID selector

    measure_project_page()
    measure_global_page()

