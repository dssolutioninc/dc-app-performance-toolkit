import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, RESOURCE_HEADERS  
logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
# WebSudo is a feature that enhances security by requiring administrators to re-authenticate before
# accessing administrative functions within Atlassian applications.
# do_websudo=True requires user administrative rights, otherwise requests fail.
#@run_as_specific_user(username='admin', password='admin', do_websudo=False)  # run as specific user
def app_specific_action(locust):
    url = '/rest/jtricks/1.0/config/archivedVersions'
    
    r = locust.get(url, headers=RESOURCE_HEADERS, catch_response=True)  # call app-specific GET endpoint
    assert r.status_code == 200, 'get config error'
