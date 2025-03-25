import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed  # noqa F401
from locustio.jira.requests_params import jira_datasets
import json
import random
import time

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

@jira_measure("locust_project_role_tab")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def project_role_tab(locust):
    ts = time.time()
    raise_if_login_failed(locust)
    project_key = random.choice(jira_dataset['projects'])[0] #key or id
    logger.locust_info(f'Testing project: {project_key}')

    # get group member
    r = locust.get(f'/rest/projectrole/1.0/projectrole/10002/{project_key}/groupmember?groupname=jira-administrators',auth=('admin', 'admin'), catch_response=True)  # call app-specific GET endpoint //fix project role & groupname
    assert r.status_code == 200
