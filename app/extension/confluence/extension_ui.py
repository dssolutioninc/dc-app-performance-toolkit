import random

from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import (
    ConfluencePageWithSync,
    SpaceSyncConfigPage,
    SpaceSyncAdminConfigPage,
    SpaceSyncMainPage,
    Login,
    AllUpdates
)
from util.conf import CONFLUENCE_SETTINGS
from selenium.webdriver.common.by import By


def test_page_sync_button(webdriver, datasets):
    page_id = datasets.get('custom_page_id') if datasets.get('custom_pages') else random.choice(datasets['pages'])[0]
    page = ConfluencePageWithSync(webdriver, page_id=page_id)
    
    @print_timing("selenium_test_page_sync_button")
    def measure():
        page.go_to()
        page.wait_for_page_loaded()
        if not page.has_sync_button(timeout=10):
            raise Exception(f"page-sync-button not found on page {page_id}")
    measure()


def test_space_sync_config(webdriver, datasets):
    page = SpaceSyncConfigPage(webdriver)
    
    @print_timing("selenium_test_space_sync_config")
    def measure():
        
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.wait_for_page_loaded()
            login_page.set_credentials(username=username, password=password)
            login_page.click_login_button()
            if login_page.is_first_login():
                login_page.first_user_setup()
            all_updates_page = AllUpdates(webdriver)
            all_updates_page.wait_for_page_loaded()

            page.go_to()
            page.wait_for_page_loaded()
            if not page.has_space_sync_section(timeout=10):
                raise Exception(f"Space Sync section not found")

        app_specific_user_login(username='admin', password='admin')

    measure()


def test_admin_config(webdriver, datasets):
    page = SpaceSyncAdminConfigPage(webdriver)

    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.wait_for_page_loaded()
            login_page.set_credentials(username=username, password=password)
            login_page.click_login_button()
            if login_page.is_first_login():
                login_page.first_user_setup()
            all_updates_page = AllUpdates(webdriver)
            all_updates_page.wait_for_page_loaded()
    
            page.go_to_admin_page(password=password)
            if page.element_exists((By.CLASS_NAME, "aui-message-warning")):
                page.get_element((By.ID, "password")).send_keys(password)
                page.wait_until_visible((By.ID, "authenticateButton")).click()
            page.wait_until_present((By.CLASS_NAME, "aui-page-header-main"))
        app_specific_user_login(username='admin', password='admin')
    measure()


def test_main_page_container(webdriver, datasets):
    page = SpaceSyncMainPage(webdriver)
    
    @print_timing("selenium_test_main_page_container")
    def measure():
        page.go_to()
        page.wait_for_page_loaded()
        if not page.has_main_container(timeout=10):
            raise Exception("main-page-container not found")
    measure()
    
