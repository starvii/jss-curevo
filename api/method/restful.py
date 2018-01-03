import json
from method.serial import to_json

METHOD_OVERRIDE = 'X-HTTP-Method-Override'
JSON_SUCCESS = to_json({'result': 'success'})
JSON_FAILED = to_json({'result': 'failed'})


def parse_body(body_bytes):
    j = body_bytes
    j = j.decode('utf-8').strip()
    if len(j) == 0:
        j = '{}'
    d = json.loads(j)
    return d
