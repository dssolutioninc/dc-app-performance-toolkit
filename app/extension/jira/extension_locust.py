import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_jtricks_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    url = '/rest/jtricks/1.0/config/archivedVersions'
    
    r = locust.get(url, headers=RESOURCE_HEADERS, catch_response=True)  # call app-specific GET endpoint
    assert r.status_code == 200, 'get config error'