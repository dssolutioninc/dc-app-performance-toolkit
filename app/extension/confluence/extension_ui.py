"""Selenium UI extension tests for the Excel-like Tables for Confluence DC plugin.

Covered modules
---------------
1. etc_view_macro_page         – Open pages that contain an excel-like-tables macro
                                 and verify the macro renders.
2. etc_view_homepage           – Open the plugin homepage (/users/etc-homepage.action).
3. etc_view_attachment_manager – Open the Attachment Health Manager admin page
                                 (WebSudo required).
"""

import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import AdminPage
from util.conf import CONFLUENCE_SETTINGS

# ---------------------------------------------------------------------------
# Configure the page IDs of Confluence pages that contain an
# excel-like-tables macro.
# ---------------------------------------------------------------------------
ETC_MACRO_PAGE_IDS = [
    # "123456",   # Example: "My Table Page"
    # "789012",   # Example: "Budget Overview"
]

# Timeout (seconds) to wait for the macro container after the page loads.
MACRO_LOAD_TIMEOUT = 30


# ---------------------------------------------------------------------------
# 1. Macro view
# ---------------------------------------------------------------------------

def etc_view_macro_page(webdriver, datasets):
    """Navigate to a configured page and verify the excel-like-tables macro renders.
    The macro is identified by class name "view-screen-loading".
    """
    if not ETC_MACRO_PAGE_IDS:
        raise RuntimeError(
            "ETC_MACRO_PAGE_IDS is empty. "
            "Add at least one Confluence page ID that contains an excel-like-tables macro."
        )

    page_id = random.choice(ETC_MACRO_PAGE_IDS)
    page = BasePage(webdriver)
    url = f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={page_id}"

    @print_timing("selenium_etc_view_macro_page")
    def measure():
        @print_timing("selenium_etc_view_macro_page:navigate")
        def sub_navigate():
            page.go_to_url(url)
            page.wait_until_visible((By.ID, "title-text"))
        sub_navigate()

        @print_timing("selenium_etc_view_macro_page:macro_loaded")
        def sub_macro():
            page.wait_until_visible(
                (By.CLASS_NAME, "view-screen-loading"),
                timeout=MACRO_LOAD_TIMEOUT,
            )
        sub_macro()

    measure()


# ---------------------------------------------------------------------------
# 2. Homepage
# ---------------------------------------------------------------------------

def etc_view_homepage(webdriver, datasets):
    """Navigate to the Excel-like Tables plugin homepage and verify it renders.

    URL: /users/etc-homepage.action
    The React app mounts on ``#homepage-root``

    Note: the homepage link only appears when ``homepageDisplay`` is enabled
    in admin settings.  Make sure it is enabled before running this test.
    """
    page = BasePage(webdriver)
    url = f"{CONFLUENCE_SETTINGS.server_url}/users/etc-homepage.action"

    @print_timing("selenium_etc_view_homepage")
    def measure():
        @print_timing("selenium_etc_view_homepage:navigate")
        def sub_navigate():
            page.go_to_url(url)
            page.wait_until_visible((By.ID, "homepage-root"))
        sub_navigate()

    measure()


# ---------------------------------------------------------------------------
# 3. Attachment Health Manager (admin)
# ---------------------------------------------------------------------------

def etc_view_attachment_manager(webdriver, datasets):
    """Navigate to the Attachment Health Manager admin page and verify it renders.

    URL: /admin/plugins/excel-like-tables/attachment-management.action
    Requires admin credentials and a WebSudo session
    """
    admin_password = CONFLUENCE_SETTINGS.admin_password
    page = BasePage(webdriver)

    @print_timing("selenium_etc_view_attachment_manager")
    def measure():
        @print_timing("selenium_etc_view_attachment_manager:websudo")
        def sub_websudo():
            AdminPage(webdriver).go_to(password=admin_password)
        sub_websudo()

        @print_timing("selenium_etc_view_attachment_manager:navigate")
        def sub_navigate():
            url = (
                f"{CONFLUENCE_SETTINGS.server_url}"
                "/admin/plugins/excel-like-tables/attachment-management.action"
            )
            page.go_to_url(url)
            page.wait_until_visible((By.CSS_SELECTOR, ".attachment-management-container"))
        sub_navigate()

    measure()


# ---------------------------------------------------------------------------
# Default entry point — called via the commented block in confluence_ui.py.
# Runs non-admin actions only; the admin test is wired as a separate function.
# ---------------------------------------------------------------------------

def app_specific_action(webdriver, datasets):
    etc_view_macro_page(webdriver, datasets)
    etc_view_homepage(webdriver, datasets)
