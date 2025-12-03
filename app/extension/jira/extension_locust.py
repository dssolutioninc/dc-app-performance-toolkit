import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
import json

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
# WebSudo is a feature that enhances security by requiring administrators to re-authenticate before
# accessing administrative functions within Atlassian applications.
# do_websudo=True requires user administrative rights, otherwise requests fail.
#@run_as_specific_user(username='admin', password='admin', do_websudo=False)  # run as specific user
def app_specific_action(locust):
    url = '/plugins/servlet/tfj/timesheetlicense'
    body = json.dumps(True)  # Send JSON boolean true as string "true"
    headers = {'content-type': 'application/json'}
    r = locust.post(url, body, headers, catch_response=True)
    content = r.content.decode('utf-8')

    logger.locust_info(f'POST response: {content}')
    if '"success":true' not in content or 'You are licensed!' not in content:
        logger.error(f'Expected license success not found in {content}')
    assert '"success":true' in content and 'You are licensed!' in content  # assertion after POST request