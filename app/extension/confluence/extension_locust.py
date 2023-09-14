import re
import json
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_advanced_collaborative_table_updater")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def advanced_collaborative_table_updater(locust):

    payload={'spaceKey': 'QT'}
    files=[
        ('csvFile',('actu_sample_data.csv',open("././datasets/actu_sample_data.csv",'rb'),'text/csv'))
    ]
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': '"en-US,en;q=0.5"',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Atlassian-Token': 'no-check',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Cookie': 'INGRESSCOOKIE=96193ba44dd63e5c402aedc3413fdb5e|bc7938bbab5da9ce7e6ee05df935b659; JSESSIONID=EB5CF6954C0C1B7A83512C2E9492CFF1'
    }

    r = locust.post('/rest/advanced-collaborative-table-updater/1.0/actu', headers=headers, data=payload, files=files)
    content = json.loads(r.content.decode('utf-8'))
    assert content['message'] == "Form data and file successfully received", 'An error occurred'