import random
import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed, RESOURCE_HEADERS  # noqa F401
from locustio.jira.requests_params import Login, BrowseIssue, CreateIssue, SearchJql, ViewBoard, BrowseBoards, \
    BrowseProjects, AddComment, ViewDashboard, EditIssue, ViewProjectSummary, jira_datasets
import json

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

@jira_measure("locust_version_manager")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def version_manager(locust):
    raise_if_login_failed(locust)
    project_key = random.choice(jira_dataset['issues'])[2]
    logger.locust_info(f'Testing project: {project_key}')

    # create version
    release_1_body = { "name": "locust test release 1", "status": "Unreleased" }
    r = locust.post(f'/rest/versionmanager/1.0/versionmanager/{project_key}', json=release_1_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    release_1_id = content["id"]
    assert content["name"] == "locust test release 1"

    release_2_body = { "name": "locust test release 2", "status": "Unreleased" }
    r = locust.post(f'/rest/versionmanager/1.0/versionmanager/{project_key}', json=release_2_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    release_2_id = content["id"]
    assert content["name"] == "locust test release 2"

    # update version
    release_1_update_body = { "id": release_1_id, "name": "locust test release 1 updated" }
    r = locust.put(f'/rest/versionmanager/1.0/versionmanager/{project_key}/{release_1_id}', json=release_1_update_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    assert content["name"] == "locust test release 1 updated"

    release_2_update_body = { "id": release_2_id, "name": "locust test release 2 updated" }
    r = locust.put(f'/rest/versionmanager/1.0/versionmanager/{project_key}/{release_2_id}', json=release_2_update_body, headers=RESOURCE_HEADERS, catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    assert content["name"] == "locust test release 2 updated"

    # # move version
    move_release_body = { "after": f'/jira/rest/versionmanager/1.0/versionmanager/{project_key}/{release_1_id}'}
    r = locust.post(f'/rest/versionmanager/1.0/versionmanager/{project_key}/{release_2_id}/move', json=move_release_body, headers=RESOURCE_HEADERS, catch_response=True)
    
    # delete version
    r = locust.delete(f'/rest/versionmanager/1.0/versionmanager/{project_key}/{release_1_id}', headers=RESOURCE_HEADERS, catch_response=True)
    r = locust.delete(f'/rest/versionmanager/1.0/versionmanager/{project_key}/{release_2_id}', headers=RESOURCE_HEADERS, catch_response=True)

    # get version
    r = locust.get(f'/rest/versionmanager/1.0/versionmanager/{project_key}', catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    has_test_releases = False
    for i in content:
        if i["name"] == "locust test release 1 updated" or i["name"] == "locust test release 2 updated":
            has_test_releases = True
            break
    assert has_test_releases == False


