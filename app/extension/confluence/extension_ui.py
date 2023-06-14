import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates, AdvancedImageGallery
from util.conf import CONFLUENCE_SETTINGS


def test_1_view_advanced_image_gallery_config(webdriver, datasets):
    page = BasePage(webdriver)
    advanced_image_gallery = AdvancedImageGallery(webdriver)

    @print_timing("selenium_view_advanced_image_gallery")
    def measure_user_login(username='admin', password='admin'):
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

        # go to configuration page
        advanced_image_gallery.go_to_advanced_image_gallery_configuration()
        if advanced_image_gallery.element_exists((By.CLASS_NAME, "aui-message-warning")):
            advanced_image_gallery.get_element((By.ID, "password")).send_keys(password)
            advanced_image_gallery.wait_until_visible((By.ID, "authenticateButton")).click()
        advanced_image_gallery.wait_until_present((By.ID, "advanced-gallery-config-form"))

        # go to reference configuration page
        advanced_image_gallery.go_to_advanced_image_gallery_reference_configuration()
        # if advanced_image_gallery.element_exists((By.CLASS_NAME, "aui-message-warning")):
        #     advanced_image_gallery.get_element((By.ID, "password")).send_keys(password)
        #     advanced_image_gallery.wait_until_visible((By.ID, "authenticateButton")).click()
        advanced_image_gallery.wait_until_present((By.ID, "aig-reference-config-form")) 
    measure_user_login()
