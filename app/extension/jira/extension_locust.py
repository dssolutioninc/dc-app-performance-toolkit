import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_cl_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    url = '/rest/appbox/1.0/properties/search'

    # Define the payload for the POST request
    payload = {
    "maxResult": 10,
    "startAt": 0
    }

    # Define the headers for the POST request (optional)
    headers = {
        "Content-Type": "application/json"
    }
    r = locust.post(url, json=payload, headers=headers, catch_response=True)  # call app-specific POST endpoint
    assert r.status_code == 200, 'get search property error'
