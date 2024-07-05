import re
import random
import string
import json
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
from locustio.jira.requests_params import jira_datasets

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

def get_new_id():
    return '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

@jira_measure("locust_milestone_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    project_key = random.choice(jira_dataset['projects'])[0]
    new_id = get_new_id()

    # create milestone
    milestone_body = {
        "key": f'{new_id}',
        "projectKey": f'{project_key}',
        "name": f'Milestone {project_key}',
        "description": "",
        "startDate": "",
        "completionDate": "",
        "status": "",
        "documentationLink": ""
    }
    r = locust.post('/plugins/servlet/ij/project/milestones', json=milestone_body, catch_response=True)  # call app-specific POST endpoint
    assert r.status_code == 200, 'create milestone error'

    # get milestone
    r = locust.get(f'/plugins/servlet/ij/project/milestones?projectKey={project_key}', catch_response=True)  # call app-specific GET endpoint
    assert r.status_code == 200, 'get milestone error'
