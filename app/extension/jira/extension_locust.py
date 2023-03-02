import random
import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed, RESOURCE_HEADERS  # noqa F401
from locustio.jira.requests_params import jira_datasets
import json
import time

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

SELECT_FIELD_SIMPLE = "jira.plugin.projectspecificselectfield.jpssf:cftype"

@jira_measure("locust_project_specific")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def project_specific(locust):
    ts = time.time()
    raise_if_login_failed(locust)
    project_key = random.choice(jira_dataset['projects'])[0]
    custom_field_keys = [custom_field[0] for custom_field in jira_dataset['custom_fields']]
    custom_field_names = [custom_field[1] for custom_field in jira_dataset['custom_fields']]
    custom_field_types = [custom_field[2] for custom_field in jira_dataset['custom_fields']]
    logger.locust_info(f'Testing project: {project_key}')

    # get custom fields
    r = locust.get(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}', catch_response=True)
    content = json.loads(r.content.decode('utf-8'))
    has_test_custom_fields = False
    for i in content:
        if i["id"] in custom_field_keys or i["name"] in custom_field_names:
            has_test_custom_fields = True
            break
    assert has_test_custom_fields == True, 'get custom fields error'

    for custom_field_key in custom_field_keys:
        options_id = []
        options_value = []
        ### manage options
        # add option
        option_1_body = { "value": f"locust test option 1 {ts}", "disabled": False }
        r = locust.post(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', json=option_1_body, headers=RESOURCE_HEADERS, catch_response=True)
        content = json.loads(r.content.decode('utf-8'))
        option_1_id = content["id"]
        option_1_disabled = content["disabled"]
        if custom_field_types[custom_field_keys.index(custom_field_key)] == SELECT_FIELD_SIMPLE:
            options_id.append(content["id"])
            options_value.append(content["value"])
        assert content["value"] == f"locust test option 1 {ts}", 'add option 1 error'

        option_2_body = { "value": f"locust test option 2 {ts}", "disabled": True }
        r = locust.post(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', json=option_2_body, headers=RESOURCE_HEADERS, catch_response=True)
        content = json.loads(r.content.decode('utf-8'))
        option_2_id = content["id"]
        option_2_disabled = content["disabled"]
        if custom_field_types[custom_field_keys.index(custom_field_key)] == SELECT_FIELD_SIMPLE:
            options_id.append(content["id"])
            options_value.append(content["value"])
        assert content["value"] == f"locust test option 2 {ts}", 'add option 2 error'

        # update option
        if custom_field_types[custom_field_keys.index(custom_field_key)] != SELECT_FIELD_SIMPLE:
            option_1_update_body = { "id": option_1_id, "value": f"locust test option 1 updated {ts}", "disabled": option_1_disabled }
            r = locust.put(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/{option_1_id}', json=option_1_update_body, headers=RESOURCE_HEADERS, catch_response=True)
            content = json.loads(r.content.decode('utf-8'))
            options_id.append(content["id"])
            options_value.append(content["value"])
            assert content["value"] == f"locust test option 1 updated {ts}", 'update option 1 error'

            option_2_update_body = { "id": option_2_id, "value": f"locust test option 2 updated {ts}", "disabled": not option_2_disabled }
            r = locust.put(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/{option_2_id}', json=option_2_update_body, headers=RESOURCE_HEADERS, catch_response=True)
            content = json.loads(r.content.decode('utf-8'))
            options_id.append(content["id"])
            options_value.append(content["value"])
            assert content["value"] == f"locust test option 2 updated {ts}" and content["disabled"] != option_2_disabled, 'update option 2 error'

        # get options
        r = locust.get(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', catch_response=True)
        content = json.loads(r.content.decode('utf-8'))
        has_test_options = False
        first_option = content[0]
        last_option = content[len(content) - 1]
        origin_option_count = len(content)
        for i in content:
            if i["id"] in options_id or i["value"] in options_value:
                has_test_options = True
                break
        assert has_test_options == True, 'get option error'

        if custom_field_types[custom_field_keys.index(custom_field_key)] != SELECT_FIELD_SIMPLE:
            # move option
            moved_option_body = {
                'after': f"/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/{last_option['id']}"
            }
            r = locust.post(f"/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/{first_option['id']}/move", json=moved_option_body, headers=RESOURCE_HEADERS, catch_response=True)
            r = locust.get(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
            content = json.loads(r.content.decode('utf-8'))
            assert first_option['id'] == content[len(content) - 1]['id'], 'move option error'

            # sort option
            r = locust.post(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/sort', headers=RESOURCE_HEADERS, catch_response=True)
            r = locust.get(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
            content = json.loads(r.content.decode('utf-8'))
            is_sorted = True
            i = 1
            while i < len(content) and len(content) > 1:
                if(content[i]['value'] < content[i - 1]['value']):
                    is_sorted = False
                i += 1
            assert is_sorted == True, 'sort options error'

            # delete option
            r = locust.delete(f"/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}/{first_option['id']}", headers=RESOURCE_HEADERS, catch_response=True)
            r = locust.get(f'/rest/projectspecificselectfield/1.0/customfield/{project_key}/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
            content = json.loads(r.content.decode('utf-8'))
            assert len(content) == origin_option_count - 1, 'delete option error'

        # statistics rest
        r = locust.get(f'/rest/projectspecificselectfield/1.0/statistics/{project_key}/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
        content = json.loads(r.content.decode('utf-8'))
        assert len(content['options']) == origin_option_count - 1 or content['id'] == custom_field_key, 'statistics field error'

        ### context manager rest
        # get contexts
        r = locust.get(f'/rest/projectspecificselectfield/1.0/context/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
        content = json.loads(r.content.decode('utf-8'))
        current_context_count = len(content)  
        assert len(content) > 0, 'get contexts error'

        if custom_field_types[custom_field_keys.index(custom_field_key)] != SELECT_FIELD_SIMPLE:
            if current_context_count < len(jira_dataset['projects']) + 1:
                # get Unassoziated Projects
                r = locust.get(f'/rest/projectspecificselectfield/1.0/context/unassociatedprojects/{custom_field_key}', headers=RESOURCE_HEADERS, catch_response=True)
                content = json.loads(r.content.decode('utf-8'))
                unassoziated_project_key = [project['key'] for project in content]
                assert len(content) > 0, 'get Unassoziated Projects error'

                # add context           
                # get issue type JIRA
                r = locust.get(f'/rest/api/2/project/{project_key}', headers=RESOURCE_HEADERS, catch_response=True)
                content = json.loads(r.content.decode('utf-8'))
                issuetypes = content['issueTypes']
                issuetype = random.choice(issuetypes)
                context_body = {
                    'associatedprojets': [project_key],
                    'issuetypes': [{ 'name': issuetype['name'], 'id': issuetype['id'] }]
                }
                if project_key in unassoziated_project_key:
                    r = locust.post(f'/rest/projectspecificselectfield/1.0/context/{custom_field_key}', json=context_body, headers=RESOURCE_HEADERS, catch_response=True)
                    content = json.loads(r.content.decode('utf-8'))
                    assert content['associatedprojets'] == [{ 'name': project_key, 'key': project_key }] \
                        or content['issuetypes'] == [{ 'name': issuetype['name'], 'id': issuetype['id'] }], 'add context error'




