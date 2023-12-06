import re
import json
import random
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user, RESOURCE_HEADERS    # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': '"en-US,en;q=0.5"',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Atlassian-Token': 'no-check',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Cookie': 'INGRESSCOOKIE=8df6887f596aed234584c96ee07ad12a|bc7938bbab5da9ce7e6ee05df935b659; JSESSIONID=D28AB74C7351CDCB60518721584D0EA7'
    }
    # add new task
    payload = {'task': 'new', 'key': 'HEL'}
    files=[]
    r = locust.post('/tfc/timesheetapplication/NewDefault.action', headers=headers, data=payload, files=files)  # call app-specific POST endpoint
    content = json.loads(r.content.decode('utf-8'))
    assert content['success'], 'Add new task failed'  # assertion after POST request

    # get task
    payload={'start': '0',
        'limit': '50',
        'month': '12',
        'year': '2023',
        'key': 'HEL',
        'user': 'admin'}
    r = locust.post('/tfc/timesheetapplication/LoadDefault.action', headers=headers, data=payload, files=files)  # call app-specific POST endpoint
    content = json.loads(r.content.decode('utf-8'))
    assert content['success'], 'Get tasks failed'  # assertion after POST request
    tasks = content['tasks']

    # edit task
    taskId = random.choice(tasks)['id']
    if taskId:
        payload={'task': 'edit',
            'key': 'id',
            'keyID': f'{taskId}',
            'field': 'title',
            'value': f'edit task {taskId}',
            'month': '12',
            'year': '2023',
            'space': 'HEL'}
        r = locust.post('/tfc/timesheetapplication/EditDefault.action', headers=headers, data=payload, files=files)  # call app-specific POST endpoint
        content = json.loads(r.content.decode('utf-8'))
        assert content['success'], 'Edit task failed'  # assertion after POST request

    # delete task
    taskId = random.choice(tasks)['id']
    if taskId:
        payload={'task': 'delete',
            'deleteKeys': f'["{taskId}"]',
            'key': 'id',
            'month': '12',
            'year': '2023',
            'space': 'HEL'}
        r = locust.post('/tfc/timesheetapplication/DeleteDefault.action', headers=headers, data=payload, files=files)  # call app-specific POST endpoint
        content = json.loads(r.content.decode('utf-8'))
        assert content['success'], 'Delete task failed'  # assertion after POST request
