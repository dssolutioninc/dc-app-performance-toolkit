import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_xstudio_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def xstudio_action(locust):
    assert True, "get xstudio_action error"