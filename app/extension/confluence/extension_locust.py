import re
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def status_micro_action(locust):
    r = locust.get('/rest/xalt-status-macro-admin/1.0/')
    assert r.status_code == 200, 'get status macro error'

    body = {"statusSet1": "enabled"}
    r = locust.client.put('/rest/xalt-status-macro-admin/1.0/', json=body, headers=RESOURCE_HEADERS)
    assert r.status_code == 204, 'put status macro error'