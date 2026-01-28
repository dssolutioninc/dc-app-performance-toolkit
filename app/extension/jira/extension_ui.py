import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_1_view_project_role_tab(webdriver, datasets):
    project_role_tab = Project(webdriver, project_key=datasets['current_session']['project_key'])

    @print_timing("selenium_view_project_role_tab")
    def measure():
        project_role_tab.go_to_project_role_tab()
        project_role_tab.wait_for_project_role_tab()

    measure()

