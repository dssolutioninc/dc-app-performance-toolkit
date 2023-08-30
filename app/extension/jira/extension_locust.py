import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
import time
import string
import json
import random
from locustio.jira.requests_params import jira_datasets
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed, RESOURCE_HEADERS

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

@jira_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def customer_specific(locust):

    ts = time.time()
    raise_if_login_failed(locust)

    # update rules
    list_organizations = []
    for num in range(1, 10):
        organization_id = random.choice(jira_dataset['organizations'])[0]
        logger.locust_info(f'Testing organization: {organization_id}')
        list_organizations.append({ 'organizationId': organization_id, 'domain': "".join([random.choice(string.ascii_lowercase) for _ in range(20)]), "addToTicket": random.choice([True, False]) })
    option_1_body = {'organizationDomains' : list_organizations}
    r = locust.post(f'/rest/organization-automation/1.0/configuration/domain-config', json=option_1_body, headers=RESOURCE_HEADERS, catch_response=True)
    assert r.status_code == 200, 'put rules error'

    # map customer
    r = locust.post(f'/rest/organization-automation/1.0/configuration/map-customers', headers=RESOURCE_HEADERS, catch_response=True)
    assert r.status_code == 200, 'map customer error'
