import json
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_app_specific_action")
# WebSudo is a feature that enhances security by requiring administrators to re-authenticate before
# accessing administrative functions within Atlassian applications.
# do_websudo=True requires user administrative rights, otherwise requests fail.
@run_as_specific_user(username='admin', password='admin', do_websudo=False)  # run as specific user
def app_specific_action(locust):
    # GET request - use 'with' statement for Locust 2.x
    with locust.get('/rest/space-sync-for-confluence-dc/1.0/oauth-client', catch_response=True) as r:
        content = r.content.decode('utf-8')   # decode response content
        
        try:
            response_data = json.loads(content)
            success = response_data.get('success', False)
            
            if not success:
                logger.error(f"GET API returned success=false. Response: {content}")
                r.failure(f"Expected success=true, got success={success}")
            else:
                r.success()
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {content}. Error: {e}")
            r.failure(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            r.failure(f"Error: {e}")
    
    # POST request to save OAuth client - use 'with' statement for Locust 2.x
    
    body = {"clientId": "af86cb6592c42ab900771f153fca2", "clientSecret": "0771f153fca2a-1009538739-u"}
    headers = {'content-type': 'application/json'}
    with locust.post('/rest/space-sync-for-confluence-dc/1.0/oauth-client', data=json.dumps(body), headers=headers, catch_response=True) as r_post:
        content_post = r_post.content.decode('utf-8')
        
        try:
            response_data_post = json.loads(content_post)
            success_post = response_data_post.get('success', False)
            
            if not success_post:
                logger.error(f"POST API returned success=false. Response: {content_post}")
                r_post.failure(f"Expected success=true, got success={success_post}")
            else:
                r_post.success()
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from POST: {content_post}. Error: {e}")
            r_post.failure(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in POST: {e}")
            r_post.failure(f"Error: {e}")
