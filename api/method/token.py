import hashlib
import os
import base64
from method.idgen import object_id


def create_cookie_token():
    """
    generate a pair of key and value, for verifying of the mechanism of tornado secret cookie
    :return: cookie_id, cookie_value
    """
    prefix = object_id()
    suffix = os.urandom(12)
    seed = hashlib.sha224(prefix + suffix).digest()
    cv = base64.urlsafe_b64encode(seed)
    ci = base64.b32encode(hashlib.sha224(seed).digest()[:20])
    return ci, cv


def verify_cookie_token(cookie_id, cookie_value):
    seed = base64.urlsafe_b64decode(cookie_value)
    ci = base64.b32encode(hashlib.sha224(seed).digest()[:20])
    if ci == cookie_id:
        return True
    return False
