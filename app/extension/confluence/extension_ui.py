import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, Page
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = Page(webdriver)
    # if datasets['custom_pages']:
    random_page = datasets['current_session']['edit_page']
    page_description = random_page[2]
    datasets['current_session']['edit_page_click'] = random_page
    page = Page(webdriver, page_id=random_page[0])

    @print_timing("selenium_markdown_exporter_action")
    def measure():

        page.go_to()
        page.wait_for_resources_loaded()
        page.wait_for_page_loaded()
        page.click_export_to_markdown()
        page.wait_until_visible((By.ID, "root"))

    measure()
