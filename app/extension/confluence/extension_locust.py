import re
import json
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user, RESOURCE_HEADERS  # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_horizzonview")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    # save host api
    body = {
        "host" : "test.host.com"
    }
    r = locust.put('/rest/horizzonview-admin/1.0/', json=body, headers=RESOURCE_HEADERS, catch_response=True)
    assert r.status_code == 204, 'PUT save host failed'

    # get host api
    r = locust.get('/rest/horizzonview-admin/1.0/', catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    assert content["host"] == "test.host.com", 'GET host failed'
