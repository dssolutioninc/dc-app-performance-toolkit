from selenium_ui.confluence import modules
from extension.confluence import extension_ui  # noqa F401


# this action should be the first one
def test_0_selenium_a_login(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.login(confluence_webdriver, confluence_datasets)


def test_1_selenium_view_blog(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.view_blog(confluence_webdriver, confluence_datasets)


def test_1_selenium_view_dashboard(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.view_dashboard(confluence_webdriver, confluence_datasets)


def test_1_selenium_view_page(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.view_page(confluence_webdriver, confluence_datasets)


def test_1_selenium_view_page_from_cache(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.view_page_from_cache(confluence_webdriver, confluence_datasets)

def test_1_selenium_create_page(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.create_confluence_page(confluence_webdriver, confluence_datasets)


def test_1_selenium_edit_by_url(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.edit_confluence_page_by_url(confluence_webdriver, confluence_datasets)


def test_1_selenium_cql_search_two_words(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.cql_search_two_words(confluence_webdriver)


def test_1_selenium_edit_page_quick_edit(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.edit_confluence_page_quick_edit(confluence_webdriver, confluence_datasets)


def test_1_selenium_create_inline_comment(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.create_inline_comment(confluence_webdriver, confluence_datasets)


def test_1_selenium_cql_search_three_words(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.cql_search_three_words(confluence_webdriver)



"""
Excel-like Tables for Confluence DC — plugin-specific extension tests.
Configure ETC_MACRO_PAGE_IDS in extension/confluence/extension_ui.py before
running the macro-view test.
"""

# --- Non-admin UI tests ---

def test_1_selenium_etc_view_macro_page(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    extension_ui.etc_view_macro_page(confluence_webdriver, confluence_datasets)


def test_1_selenium_etc_view_homepage(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    extension_ui.etc_view_homepage(confluence_webdriver, confluence_datasets)


# --- Admin UI test (must run just before logout) ---

def test_1_selenium_etc_view_attachment_manager(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    extension_ui.etc_view_attachment_manager(confluence_webdriver, confluence_datasets)


# this action should be the last one
def test_2_selenium_z_log_out(confluence_webdriver, confluence_datasets, confluence_screen_shots):
    modules.log_out(confluence_webdriver, confluence_datasets)
