import re
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401
import json

logger = init_logger(app_type='confluence')

EVENT_ID = 'QUFNa0FEQTVaVFkwTm1ZMUxUSTNaVEV0TkRBNU9DMWlNMkkyTFRkak5tRmtNbVZpWXpRME5nQkdBQUFBQUFEK0hZaXdXQ3EyUUtvZnZ6eEF6Q0pGQndEZndEMWlSZ1JnU0w4VjJHOW1Ra3R1QUFBQUFBRU5BQURmd0QxaVJnUmdTTDhWMkc5bVFrdHVBQUFlUEQ4bEFBQT0='


@confluence_measure("locust_meetical_for_confluence")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def meetical_for_confluence(locust):
    ### Config for 'Meeting for confluence' app
    # Add EWS Credentials
    ews_body = {
        "ewsUrl" : "https://mail.agile-meetings.net/EWS/Exchange.asmx",
        "ewsUsername" :"ewsuser2@meetical.local",
        "ewsPassword" : "AccessDenied22@"
    }
    r = locust.post('/rest/meetical-api/1.0/ews-config/credentials', json=ews_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = r.content.decode('utf-8')
    assert content == "Settings updated.", 'Add AWS Credentials error'

    # Add plugin-setting
    plugin_setting_body = {
        "calendarProvider": "MICROSOFT365"
    }
    r = locust.post('/rest/meetical-api/1.0/plugin-settings', json=plugin_setting_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = r.content.decode('utf-8')
    assert content == "\"MICROSOFT365\"", 'Add plugin-setting error'