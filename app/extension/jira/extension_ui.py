import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Project
from util.conf import JIRA_SETTINGS


def test_1_view_version_manager(webdriver, datasets):
    version_manager = Project(webdriver, project_key=datasets['project_key'])

    @print_timing("selenium_view_version_manager")
    def measure():
        version_manager.go_to_version_manager()
        version_manager.wait_for_version_manager()

    measure()

