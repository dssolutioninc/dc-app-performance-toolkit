from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401
from util.conf import CONFLUENCE_SETTINGS

logger = init_logger(app_type='confluence')

ETC_API_BASE = '/rest/excel-like-tables/1.0'

# ---------------------------------------------------------------------------
# API: GET /rest/excel-like-tables/1.0/language
# ---------------------------------------------------------------------------

@confluence_measure("locust_etc_get_language")
def etc_get_language(locust):
    r = locust.get(f'{ETC_API_BASE}/language', catch_response=True)
    content = r.content.decode('utf-8')
    assert '"userLanguage"' in content, \
        f'[etc_get_language] "userLanguage" key missing from response: {content}'
    logger.locust_info(f'[etc_get_language] response: {content}')


# ---------------------------------------------------------------------------
# API: GET /rest/excel-like-tables/1.0/settings
# This endpoint is annotated @WebSudoRequired, so admin credentials with
# WebSudo are mandatory.  The decorator below re-authenticates as admin
# before the call and restores the original session afterwards.
# ---------------------------------------------------------------------------

@confluence_measure("locust_etc_get_settings")
@run_as_specific_user(
    username=CONFLUENCE_SETTINGS.admin_login,
    password=CONFLUENCE_SETTINGS.admin_password,
    do_websudo=True,
)
def etc_get_settings(locust):
    r = locust.get(f'{ETC_API_BASE}/settings', catch_response=True)
    content = r.content.decode('utf-8')
    assert r.status_code == 200, \
        f'[etc_get_settings] Expected HTTP 200, got {r.status_code}: {content}'
    assert '"homepageDisplay"' in content, \
        f'[etc_get_settings] "homepageDisplay" key missing from response: {content}'
    logger.locust_info(f'[etc_get_settings] response: {content}')


# ---------------------------------------------------------------------------
# API: GET /rest/excel-like-tables/1.0/attachment-management/list-all
# Returns paginated list of all table attachments (admin scope).
# Query params are appended directly to the URL for compatibility with all
# Locust versions.
# ---------------------------------------------------------------------------

@confluence_measure("locust_etc_get_attachment_list")
@run_as_specific_user(
    username=CONFLUENCE_SETTINGS.admin_login,
    password=CONFLUENCE_SETTINGS.admin_password,
    do_websudo=False,
)
def etc_get_attachment_list(locust):
    r = locust.get(
        f'{ETC_API_BASE}/attachment-management/list-all?limit=50&offset=0',
        catch_response=True,
    )
    content = r.content.decode('utf-8')
    assert r.status_code == 200, \
        f'[etc_get_attachment_list] Expected HTTP 200, got {r.status_code}: {content}'
    assert '"attachments"' in content, \
        f'[etc_get_attachment_list] "attachments" key missing from response: {content}'
    logger.locust_info(f'[etc_get_attachment_list] response (first 200 chars): {content[:200]}')


# ---------------------------------------------------------------------------
# Entry point called by the Locust task in locustfile.py.
# Each sub-function is individually measured for separate metrics.
# ---------------------------------------------------------------------------

def app_specific_action(locust):
    etc_get_language(locust)
    etc_get_settings(locust)
    etc_get_attachment_list(locust)
