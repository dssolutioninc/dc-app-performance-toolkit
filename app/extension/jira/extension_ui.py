import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    project_page_milestone = Project(webdriver, project_key=datasets['current_session']['project_key'])

    @print_timing("selenium_view_project_page_milestone")
    def measure_project_page():
        # Project page
        project_page_milestone.go_to_project_page_milestone()
        project_page_milestone.wait_for_project_page_milestone()

    @print_timing("selenium_view_global_page_milestone")
    def measure_global_page():
        # Global page
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ProjectMilestonesOverview.jspa?moduleKey=pci-global-page")
        page.wait_until_visible((By.ID, 'content'))  # Wait for you app-specific UI element by ID selector

    measure_project_page()
    measure_global_page()

