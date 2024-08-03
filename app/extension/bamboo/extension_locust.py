import re
from locustio.common_utils import init_logger, bamboo_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='bamboo')


@bamboo_measure("locust_app_specific_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):

    body = {
        "admin_token": 'NDg2MDMyOTA4NDQxOv7FKjeQL7EGKykE7al9WOTdosXJ1', 
        "bamboo_server_url": "http://a73555c5b7a434dc3afdde5cb82b532a-1162269827.us-east-2.elb.amazonaws.com/bamboo"
    }  # include parsed variables to POST request body
    headers = {
        'content-type': 'application/json',
    }
    r = locust.post('/rest/ci-cd/1.0/balra/admin', body, headers, catch_response=True)  # call app-specific POST endpoint
    assert r.status_code == 200, 'Config admin error'
