import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_timela_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    r = locust.get('/plugins/servlet/app/property?propertyKey=company', catch_response=True)  # call app-specific GET endpoint
    assert r.status_code == 200, 'get app property error'
