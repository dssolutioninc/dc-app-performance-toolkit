import random
from selenium_ui.conftest import print_timing, measure_browser_navi_metrics, measure_dom_requests
from selenium.webdriver.common.by import By


from selenium_ui.confluence.pages.pages import Login, AllUpdates, PopupManager, Page, Dashboard, TopNavPanel, Editor, \
    Logout
from selenium_ui.confluence.pages.selectors import EditorLocators
from selenium_ui.base_page import BasePage
from util.api.confluence_clients import ConfluenceRestClient
from util.confluence.browser_metrics import browser_metrics
from util.conf import CONFLUENCE_SETTINGS

USERS = "users"
PAGES = "pages"
CUSTOM_PAGES = "custom_pages"
BLOGS = "blogs"


def setup_run_data(datasets):
    user = random.choice(datasets[USERS])
    page = random.choice(datasets[PAGES])
    if CUSTOM_PAGES in datasets:
        if len(datasets[CUSTOM_PAGES]) > 0:
            custom_page = random.choice(datasets[CUSTOM_PAGES])
            datasets['custom_page_id'] = custom_page[0]
    blog = random.choice(datasets[BLOGS])
    datasets['username'] = user[0]
    datasets['password'] = user[1]
    datasets['page_id'] = page[0]
    datasets['blog_id'] = blog[0]

    datasets['view_page'] = None
    datasets['view_page_cache'] = None
    datasets['edit_page'] = None
    datasets['edit_page_click'] = None
    datasets['create_comment_page'] = None
    datasets['view_blog'] = None


def login(webdriver, datasets):
    setup_run_data(datasets)
    rest_client = ConfluenceRestClient(
        CONFLUENCE_SETTINGS.server_url,
        CONFLUENCE_SETTINGS.admin_login,
        CONFLUENCE_SETTINGS.admin_password,
        verify=CONFLUENCE_SETTINGS.secure,
    )
    login_page = Login(webdriver)

    def measure():

        def sub_measure():
            login_page.go_to()
            if login_page.is_logged_in():
                login_page.delete_all_cookies()
                login_page.go_to()
            login_page.wait_for_page_loaded()
            node_id = login_page.get_node_id()
            node_ip = rest_client.get_node_ip(node_id)
            webdriver.node_ip = node_ip
            print(f"node_id:{node_id}, node_ip: {webdriver.node_ip}")
            measure_dom_requests(
                webdriver, interaction="selenium_login:open_login_page")

        sub_measure()

        login_page.set_credentials(
            username=datasets['username'], password=datasets['password'])

        def sub_measure():
            login_page.click_login_button()
            if login_page.is_first_login():
                login_page.first_user_setup()
            all_updates_page = AllUpdates(webdriver)
            all_updates_page.wait_for_page_loaded()
            measure_dom_requests(
                webdriver, interaction="selenium_login:login_and_view_dashboard")
            if CONFLUENCE_SETTINGS.extended_metrics:
                measure_browser_navi_metrics(
                    webdriver, datasets, expected_metrics=browser_metrics['selenium_login'])

        sub_measure()

    measure()
    PopupManager(webdriver).dismiss_default_popup()


def view_page(webdriver, datasets):
    random_page = random.choice(datasets[PAGES])
    page_id = random_page[0]
    page_description = random_page[2]
    datasets['view_page'] = random_page
    datasets['view_page_cache'] = random_page
    page = Page(webdriver, page_id=page_id)

    def measure():
        page.go_to()
        page.wait_for_page_loaded()
        measure_dom_requests(
            webdriver, interaction=f"selenium_view_page", description=page_description)
        if CONFLUENCE_SETTINGS.extended_metrics:
            measure_browser_navi_metrics(
                webdriver, datasets, expected_metrics=browser_metrics['selenium_view_page'])

    measure()


def view_page_from_cache(webdriver, datasets):
    cached_page = datasets['view_page_cache']
    page_id = cached_page[0]
    page_description = cached_page[2]
    datasets['view_page'] = cached_page

    page = Page(webdriver, page_id=page_id)

    def measure():
        page.go_to()
        page.wait_for_page_loaded()
        measure_dom_requests(
            webdriver, interaction=f"selenium_view_page_from_cache", description=page_description)
        if CONFLUENCE_SETTINGS.extended_metrics:
            measure_browser_navi_metrics(webdriver, datasets,
                                         expected_metrics=browser_metrics['selenium_view_page_from_cache'])

    measure()


def view_blog(webdriver, datasets):
    random_blog = random.choice(datasets[BLOGS])
    blog_id = random_blog[0]
    blog_description = random_blog[2]
    blog = Page(webdriver, page_id=blog_id)
    datasets['view_blog'] = random_blog

    def measure():
        blog.go_to()
        blog.wait_for_page_loaded()
        measure_dom_requests(
            webdriver, interaction=f"selenium_view_blog", description=blog_description)
        if CONFLUENCE_SETTINGS.extended_metrics:
            measure_browser_navi_metrics(
                webdriver, datasets, expected_metrics=browser_metrics['selenium_view_blog'])

    measure()


def view_dashboard(webdriver, datasets):
    dashboard_page = Dashboard(webdriver)

    def measure():
        dashboard_page.go_to()
        dashboard_page.wait_for_page_loaded()
        measure_dom_requests(webdriver, interaction="selenium_view_dashboard")
        if CONFLUENCE_SETTINGS.extended_metrics:
            measure_browser_navi_metrics(webdriver, datasets,
                                         expected_metrics=browser_metrics['selenium_view_dashboard'])

    measure()


def create_confluence_page(webdriver, datasets):
    nav_panel = TopNavPanel(webdriver)
    create_page = Editor(webdriver)

    def measure():
        def sub_measure():
            nav_panel.click_create()
            PopupManager(webdriver).dismiss_default_popup()
            create_page.wait_for_create_page_open()
            measure_dom_requests(
                webdriver, interaction="selenium_create_page:open_create_page_editor")
            if CONFLUENCE_SETTINGS.extended_metrics:
                measure_browser_navi_metrics(webdriver, datasets,
                                             expected_metrics=browser_metrics['selenium_create_page'])

        sub_measure()

        PopupManager(webdriver).dismiss_default_popup()

        create_page.write_title()
        create_page.write_content()

        def sub_measure():
            create_page.click_submit()
            page = Page(webdriver)
            page.wait_for_page_loaded()
            measure_dom_requests(
                webdriver, interaction="selenium_create_page:save_created_page")

        sub_measure()

    measure()


def edit_confluence_page_by_url(webdriver, datasets):
    random_page = random.choice(datasets[PAGES])
    page_id = random_page[0]
    page_description = random_page[2]
    datasets['edit_page'] = random_page
    edit_page = Editor(webdriver, page_id=page_id)

    def measure():
        def sub_measure():
            edit_page.go_to()
            edit_page.wait_for_page_loaded()
            measure_dom_requests(webdriver, interaction=f"selenium_edit_page_by_url:open_create_page_editor",
                                 description=page_description)
            if CONFLUENCE_SETTINGS.extended_metrics:
                measure_browser_navi_metrics(webdriver, datasets,
                                             expected_metrics=browser_metrics['selenium_edit_page_by_url'])

        sub_measure()

        edit_page.write_content()

        def sub_measure():
            edit_page.save_edited_page()
            measure_dom_requests(webdriver, interaction=f"selenium_edit_page_by_url:save_edited_page",
                                 description=page_description)

        sub_measure()

    measure()


def action_for_macros(webdriver, datasets):
    tab_a = "Tab A"
    tab_b = "Tab B"
    
    def create_page():
        nav_panel = TopNavPanel(webdriver)
        create_page = Editor(webdriver)

        def measure():
            def sub_measure():
                nav_panel.click_create()
                PopupManager(webdriver).dismiss_default_popup()
                create_page.wait_for_create_page_open()
                measure_dom_requests(
                    webdriver, interaction="selenium_create_page:open_create_page_editor")
                if CONFLUENCE_SETTINGS.extended_metrics:
                    measure_browser_navi_metrics(webdriver, datasets,
                                                expected_metrics=browser_metrics['selenium_create_page'])

            sub_measure()

            PopupManager(webdriver).dismiss_default_popup()

            def write_title():
                title_field = BasePage(webdriver).wait_until_visible(EditorLocators.title_field)
                title = "Selenium - " + BasePage(webdriver).generate_random_string(10)
                title_field.clear()
                title_field.send_keys(title)

            write_title()

            def click_publish():
                create_page.click_submit()
                page = Page(webdriver)
                page.wait_for_page_loaded()
                measure_dom_requests(
                    webdriver, interaction="selenium_create_page:save_created_page")

            click_publish()

        measure()

    def go_to_edit_page():
        page = Page(webdriver)
        edit_page = Editor(webdriver)
        page.click_edit()
        edit_page.wait_for_page_loaded()

    def add_advanded_tabs():
        edit_page = Editor(webdriver)
        edit_page.click_insert_more_content_btn()
        edit_page.click_other_macros_btn()
        edit_page.search_input("Advanced Tabs")
        edit_page.click_macros_app()
        edit_page.click_insert_btn()
        BasePage(webdriver).wait_until_available_to_switch(EditorLocators.page_content_field)
        advanced_input_loc = (By.XPATH, '//table[@data-macro-name= "advanced-tabs"]//td[@class = "wysiwyg-macro-body"]/p')
        advanced_input = BasePage(webdriver).get_element(advanced_input_loc)
        advanced_input.click()
        def generate_loc__input_text_of_tabs(tab_name:str):
            input_text_tabs_loc = (By.XPATH, f'//table[@data-macro-parameters = "tabName={tab_name}"]//p')
            return input_text_tabs_loc
        def generate_loc__space_behind_one_tab(tab_name:str):
            space_behind_tab = (By.XPATH, f'//table[@data-macro-parameters = "tabName={tab_name}"]/following-sibling::p[@class = "auto-cursor-target"]')
            return space_behind_tab
        def add_two_tabs():
            
            # insert `tab a` + content
            BasePage(webdriver).return_to_parent_frame()
            edit_page.click_insert_more_content_btn()
            edit_page.click_other_macros_btn()
            edit_page.search_input("Tabs")
            edit_page.click_tabs()
            edit_page.tab_name_input(tab_a)
            edit_page.click_insert_btn()
            BasePage(webdriver).wait_until_available_to_switch(EditorLocators.page_content_field)
            input_text_of_tabs = BasePage(webdriver).get_element(generate_loc__input_text_of_tabs(tab_a))
            input_text_of_tabs.click()
            input_text_of_tabs.send_keys(tab_a)
            # insert `tab_b` + content
            space_behinh = BasePage(webdriver).wait_until_visible(generate_loc__space_behind_one_tab(tab_a))
            space_behinh.click()
            BasePage(webdriver).return_to_parent_frame()
            edit_page.click_insert_more_content_btn()
            edit_page.click_other_macros_btn()
            edit_page.search_input("Tabs")
            edit_page.click_tabs()
            edit_page.tab_name_input(tab_b)
            edit_page.click_insert_btn()
            BasePage(webdriver).wait_until_available_to_switch(EditorLocators.page_content_field)
            input_text_of_tabs = BasePage(webdriver).get_element(generate_loc__input_text_of_tabs(tab_b))
            input_text_of_tabs.click()
            input_text_of_tabs.send_keys(tab_b)
            BasePage(webdriver).return_to_parent_frame()
        add_two_tabs()

    def update():
        edit_page = Editor(webdriver)
        edit_page.save_edited_page()
        measure_dom_requests(
            webdriver, interaction=f"selenium_edit_page_by_url:save_edited_page")
        
    def verify_data():
        def generate_loc__tabs_in_list(tab_name: str):
            tab_in_list_loc = (By.XPATH, f'//ul[@class="tabs-menu"]//a[text()="{tab_name}"]')
            return tab_in_list_loc
        def generate_loc__contents_of_list(tab_name: str):
            content = (By.XPATH, f'//div[@data-tab-name = "{tab_name}"]')
            return content
        # verify tab_a
        first_tab = BasePage(webdriver).get_element(generate_loc__tabs_in_list(tab_a))
        first_tab.click()
        assert first_tab.get_attribute("aria-selected") == "true"
        content_of_first_tab = BasePage(webdriver).get_element(generate_loc__contents_of_list(tab_a))
        assert content_of_first_tab.text == tab_a
        # verify tab_b
        second_tab = BasePage(webdriver).get_element(generate_loc__tabs_in_list(tab_b))
        second_tab.click()
        assert second_tab.get_attribute("aria-selected") == "true"
        content_of_second_tab = BasePage(webdriver).get_element(generate_loc__contents_of_list(tab_b))
        assert content_of_second_tab.text == tab_b
        
    def delete_page():
        more_option_loc = (By.XPATH, '//a[@id = "action-menu-link"]')
        more_option_ele = BasePage(webdriver).get_element(more_option_loc)
        more_option_ele.click()
        delete_page_loc = (By.XPATH, '//a[@id = "action-remove-content-link"]')
        BasePage(webdriver).get_element(delete_page_loc).click()
        delete_page_confirm_btn = (By.XPATH, '//button[@id = "delete-dialog-next"]')
        BasePage(webdriver).wait_until_visible(delete_page_confirm_btn).click()
        confirm_message_loc = (By.XPATH, '//div[@class = "aui-message closeable aui-message-success"]/p[2]')
        confirm_message_ele = BasePage(webdriver).wait_until_visible(confirm_message_loc)
        assert confirm_message_ele.text == "Space admins can restore this page from the trash."
    create_page()
    go_to_edit_page()
    add_advanded_tabs()
    update()
    verify_data()
    delete_page()


def edit_confluence_page_quick_edit(webdriver, datasets):
    random_page = datasets['edit_page']
    page_description = random_page[2]
    datasets['edit_page_click'] = random_page
    page = Page(webdriver, page_id=random_page[0])
    edit_page = Editor(webdriver, page_id=random_page[0])

    def measure():
        def sub_measure():
            page.go_to()
            page.wait_for_resources_loaded()
            page.wait_for_page_loaded()
            page.click_edit()
            edit_page.wait_for_page_loaded()
            measure_dom_requests(webdriver, interaction=f"selenium_quick_edit_page_click:open_create_page_editor",
                                 description=page_description)
            if CONFLUENCE_SETTINGS.extended_metrics:
                measure_browser_navi_metrics(webdriver, datasets,
                                             expected_metrics=browser_metrics['selenium_quick_edit_page_click'])

        sub_measure()

        edit_page.write_content()

        def sub_measure():
            edit_page.save_edited_page()
            measure_dom_requests(webdriver, interaction=f"selenium_quick_edit_page_click:save_edited_page",
                                 description=page_description)

        sub_measure()

    measure()


def create_inline_comment(webdriver, datasets):
    page = random.choice(datasets[PAGES])
    page_id = page[0]
    datasets['create_comment_page'] = page
    page = Page(webdriver, page_id=page_id)

    @print_timing("selenium_create_comment")
    def measure(webdriver):
        page.go_to()
        page.wait_for_page_loaded()
        edit_comment = Editor(webdriver)

        @print_timing("selenium_create_comment:write_comment")
        def sub_measure(webdriver):
            page.click_add_comment()
            edit_comment.write_content(text='This is selenium comment')

        sub_measure(webdriver)

        @print_timing("selenium_create_comment:save_comment")
        def sub_measure(webdriver):
            edit_comment.click_submit()
            page.wait_for_comment_field()

        sub_measure(webdriver)

    measure(webdriver)


def log_out(webdriver, datasets):
    @print_timing("selenium_log_out")
    def measure(webdriver):
        logout_page = Logout(webdriver)
        logout_page.go_to()
        logout_page.wait_for_logout()

    measure(webdriver)
