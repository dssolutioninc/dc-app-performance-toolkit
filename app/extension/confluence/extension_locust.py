import re
import random
import string
import os
import base64
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user, RESOURCE_HEADERS, JSON_HEADERS  # noqa F401
import json

logger = init_logger(app_type='confluence')

EVENT_ID = 'QUFNa0FEQTVaVFkwTm1ZMUxUSTNaVEV0TkRBNU9DMWlNMkkyTFRkak5tRmtNbVZpWXpRME5nQkdBQUFBQUFEK0hZaXdXQ3EyUUtvZnZ6eEF6Q0pGQndEZndEMWlSZ1JnU0w4VjJHOW1Ra3R1QUFBQUFBRU5BQURmd0QxaVJnUmdTTDhWMkc5bVFrdHVBQUFlUEQ4bEFBQT0='


@confluence_measure("locust_advanced_image_gallery")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def advanced_image_gallery(locust):
    # admin config
    response = locust.put('/rest/xalt-gallery/1.0/admin-config/rescale')
    response = locust.get('/rest/xalt-gallery/1.0/admin-config/get-reference-config')
    update_body = {"referenceMessage":"hello"}
    headers = {
        "Content-Type": "application/json",
        "Content-Length": "<calculated when request is sent>",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive" 
    }
    response = locust.post('/rest/xalt-gallery/1.0/admin-config/update-reference-config', json=update_body, headers=headers, catch_response=True)
    assert json.loads(response.text)['referenceMessage'] == "hello"

    # gallery API
    random_gallery_name = "".join([random.choice(string.ascii_lowercase) for _ in range(36)])
    prepared_gallery_name = 'f04cc637-6724-42da-bdec-b682f525b9e6'
    spaceKey = "BT"
    pageId = "393246"
    attachment_name = 'invincibles.jpeg'
    create_gallery_payload = {"name": random_gallery_name,"displayType":"slideshow","galleryWidth":600,"spaceKey":spaceKey,"pageId":pageId,"sortingType":"name","savedFromDraft":False,"showCopyright":False,"displayPlainInMobile":False,"galleryHeight":300,"pictures":[],"gallerySize":"SMALL"}
    response = locust.post('/rest/xalt-gallery/1.0/xalt-gallery', json=create_gallery_payload, headers=headers, catch_response=True)
    response = locust.get(f"/rest/xalt-gallery/1.0/xalt-gallery/{random_gallery_name}?pageId={pageId}", catch_response=True)
    response = locust.put(f"/rest/xalt-gallery/1.0/xalt-gallery/{random_gallery_name}", json=create_gallery_payload, headers=headers, catch_response=True)
    response = locust.post(f"/rest/xalt-gallery/1.0/scale-image/gallery?galleryName={random_gallery_name}&pageId={pageId}", json={}, headers=headers, catch_response=True)
    response = locust.get(f"/rest/xalt-gallery/1.0/xalt-gallery-macro/getmacro?spaceKey={spaceKey}&pageId={pageId}&galleryName={prepared_gallery_name}&galleryType=default")

    # crop API
    headers = {
        "Content-Length": "<calculated when request is sent>",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "X-Atlassian-Token": 'no-check'
    }
    files = {
        "croppedImage": ""
    }
    response = locust.post(f"/rest/xalt-gallery/1.0/scale-image/crop-v2?pageId={pageId}&galleryName={prepared_gallery_name}&attachmentName={attachment_name}", files=files, headers=headers, catch_response=True)
    