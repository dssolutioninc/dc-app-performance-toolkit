import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    r = locust.get(f'/rest/issueeditor/latest/config',auth=('admin', 'admin'), catch_response=True)
    assert r.status_code == 200, 'get config error'