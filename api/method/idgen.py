#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
import struct
import hashlib
import binascii
from method.codec import b32encode


class ObjectId(object):
    _index, = struct.unpack('>I', os.urandom(4))
    _hostname_bytes = hashlib.md5(socket.gethostname().encode('utf-8')).digest()[0:3]

    def __init__(self):
        pass

    def gen_id(self):
        # 0|1|2|3 | 4|5|6 | 7|8 | 9|10|11
        # 时间戳 | 机器  | PID | 计数器
        ObjectId._index += 1
        timestamp = int(time.time())
        oid = struct.pack('>I', timestamp)
        oid += self._hostname_bytes
        # 在 celery 中，多个worker首次获取到的 os.getpid() 是同一个值！
        # 这会导致唯一性出现致命问题，所以保险起见生成一次取一次
        oid += struct.pack('>H', os.getpid() % 0xffff)
        oid += struct.pack('>I', ObjectId._index % 0xfff)[1:]
        return oid

_ObjectId = ObjectId()


def object_id(code=None):
    """
    :return: bytes(12)
    """
    global _ObjectId
    oid = _ObjectId.gen_id()
    if code is None or code.upper() == 'BASE32':
        return b32encode(oid)[:-1].decode()
    elif code.upper() == 'HEX':
        return binascii.hexlify(oid).decode()
    else:
        return oid


# def b32oid():
#     oid = object_id()
#     b = bytes.translate(base64.b32encode(oid), codec.Base32.translate_map, b"=")
#     return b.decode('UTF-8')
#
#
# def create_session_id():
#     oid = object_id()
#     sid = hashlib.sha1(oid).hexdigest()
#     return sid.upper()


def main():
    for i in range(100):
        print(object_id('bytes'))


if '__main__' == __name__:
    main()
