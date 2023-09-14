import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, AdvancedCollaborativeTableUpdater
from util.conf import CONFLUENCE_SETTINGS


def test_1_view_advanced_collaborative_table_updater(webdriver, datasets):
    page = BasePage(webdriver)
    advanced_collaborative_table_updater = AdvancedCollaborativeTableUpdater(webdriver)

    @print_timing("selenium_view_advanced_collaborative_table_handler")
    def measure():
        advanced_collaborative_table_updater.go_to_advanced_collaborative_table_handle()
        advanced_collaborative_table_updater.wait_until_present((By.ID, "actu-app"))    # Wait for you app-specific UI element by ID selector
    measure()
