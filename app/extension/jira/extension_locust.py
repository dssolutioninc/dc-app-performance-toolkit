import re
from locustio.common_utils import init_logger, jira_measure, raise_if_login_failed, RESOURCE_HEADERS  # noqa F401
from locustio.jira.requests_params import jira_datasets
import random

logger = init_logger(app_type='jira')

jira_dataset = jira_datasets()


@jira_measure("locust_purgo_ai_specific_action")
# run as specific user
def app_specific_action(locust):
    raise_if_login_failed(locust)

    project_key = random.choice(jira_dataset['projects'])[0]  # key or id
    logger.locust_info(f'Testing for project: {project_key}')

    # Get project config
    url = f'/rest/purgo-ai/1.0/projectConfig/{project_key}'

    # call app-specific GET endpoint
    r = locust.get(url, headers=RESOURCE_HEADERS, auth=('admin', 'admin'), catch_response=True)
    assert r.status_code == 200
