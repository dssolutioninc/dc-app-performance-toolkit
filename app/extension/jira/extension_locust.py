import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
from locustio.jira.requests_params import jira_datasets
import json
import random

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

@jira_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    issue_key = random.choice(jira_dataset['issues'])[0]

    # GET watch-issue
    r = locust.get(f'/rest/filtersactivitystream/1.0/actions/issue-watch/{issue_key}', catch_response=True)
    assert r.status_code == 200, 'GET watch issue failed'
    content = json.loads(r.content.decode('utf-8'))

    if content == "false":
        # POST watch-issue
        r = locust.post(f'/rest/filtersactivitystream/1.0/actions/issue-watch/{issue_key}', catch_response=True)
        assert r.status_code == 204, 'POST watch issue failed'

    # # POST vote-issue
    # r = locust.post(f'/rest/filtersactivitystream/1.0/actions/issue-vote/{issue_key}', catch_response=True)
    # assert r.status_code == 204, 'POST vote issue failed'

    # FILENAME = '././datasets/jira/test.csv'
    # DELETE_LINE_NUMBER = 1
    # with open(FILENAME) as f:
    #     data = f.read().splitlines() # Read csv file
    # with open(FILENAME, 'w') as g:
    #     g.write('\n'.join([data[:DELETE_LINE_NUMBER]] + data[DELETE_LINE_NUMBER + 1:])) # Write to file
