#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque

"""
rfc4648
   (1) The final quantum of encoding input is an integral multiple of 40
       bits; here, the final unit of encoded output will be an integral
       multiple of 8 characters with no "=" padding.

   (2) The final quantum of encoding input is exactly 8 bits; here, the
       final unit of encoded output will be two characters followed by
       six "=" padding characters.

   (3) The final quantum of encoding input is exactly 16 bits; here, the
       final unit of encoded output will be four characters followed by
       four "=" padding characters.

   (4) The final quantum of encoding input is exactly 24 bits; here, the
       final unit of encoded output will be five characters followed by
       three "=" padding characters.

   (5) The final quantum of encoding input is exactly 32 bits; here, the
       final unit of encoded output will be seven characters followed by
       one "=" padding character.
"""

"""
    新的BASE32编码方式，保留全部数字，将部分容易混淆的字母留作他用。
    从字节流的右边开始编码，前部补齐
    补齐时也不按照字节方式补齐，仅仅按位补齐
"""

suffix = (b'', b'I', b'L', b'O', b'V')  # 结尾字符表，用于表示最前端补了几位
tm = (
    b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'J',
    b'K', b'M', b'N', b'P', b'Q', b'R', b'S', b'T', b'U', b'W', b'X', b'Y', b'Z')  # translate_map
rm = (
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None, None, None,
    None, None, None, 10, 11, 12, 13, 14, 15, 16, 17, None, 18, 19, None, 20, 21, None, 22, 23, 24, 25, 26, 27, None,
    28, 29, 30, 31)  # reverse_map
operands = (0, 1, 3, 7, 15, 31)  # 与运算辅助表


def and_operand(right, left=None):
    """
    根据给定的位置信息，生成字节数据，用于与运算提取字节中指定位的数据
    :param right: 
    :param left: 
    :return: 
    """
    assert type(right) == int
    assert 0 <= right <= 7
    if left is None:
        left = right + 4
    else:
        assert type(left) == int
    if left > 7:
        left = 7
    assert left >= right
    length = left + 1 - right
    assert 0 < length <= 5
    o = operands[length]
    return o << right


def b32encode(_bytes):
    bit_len = len(_bytes) * 8
    base_len = bit_len // 5
    buf = deque()
    for idx in range(0, base_len):
        bit_idx = idx * 5
        bit_idx_next = bit_idx + 4
        b0 = bit_idx // 8
        b1 = bit_idx_next // 8
        byte_idx = len(_bytes) - 1 - b0
        if b0 == b1:
            c = _bytes[byte_idx]
            right = bit_idx % 8
            op = and_operand(right)
            b = (c & op) >> right
            # print('c={:08b}, op={:08b}, b={:05b}'.format(c, op, b))
        else:
            byte_idx_next = len(_bytes) - 1 - b1
            assert byte_idx - 1 == byte_idx_next
            c0 = _bytes[byte_idx]
            c1 = _bytes[byte_idx_next]
            right = bit_idx % 8
            # print('right={}'.format(right))
            op0 = and_operand(right, 7)
            b0 = (c0 & op0) >> right
            left = bit_idx_next % 8
            # print('left={}'.format(left))
            op1 = and_operand(0, left)
            b1 = (c1 & op1) << (8 - right)
            b = b0 | b1
            # print('c0={:08b}, op0={:08b}, b0={:08b}'.format(c0, op0, b0))
            # print('c1={:08b}, op1={:08b}, b1={:08b}'.format(c1, op1, b1))
            # print('b={:08b}'.format(b))
        base = tm[b]
        buf.insert(0, base)
    tail = bit_len - base_len * 5
    if tail > 0:
        padding = 5 - tail
        c = _bytes[0]
        right = 8 - tail
        op = and_operand(right)
        b = (c & op) >> right
        base = tm[b]
        buf.insert(0, base)
        buf.append(suffix[padding])
    return b''.join(buf)


def b32decode(_bytes):
    def pos_from_bit_count(bc):
        byte_pos = (bc + 7) // 8 - 1
        p = bc % 8
        bit_pos = 0 if p == 0 else 8 - p
        return byte_pos, bit_pos
    tail = chr(_bytes[-1]).encode()
    buf = deque()
    if tail in suffix:
        padding = suffix.index(tail)
        bit_len = (len(_bytes) - 1) * 5 - padding
        b32data = _bytes[1:-1]
        # 处理第一个字符
        op = and_operand(0, 4 - padding)
        b = (rm[_bytes[0]] & op) << (3 + padding)
        bit_count = 5 - padding
        buf.append(b)
        byte_len = bit_len // 8 - 1
    else:
        bit_count = 0
        bit_len = len(_bytes) * 5
        b32data = _bytes
        byte_len = bit_len // 8
    assert bit_len % 8 == 0
    for i in range(byte_len):
        buf.append(0)
    for c in b32data:
        byte0, bit0 = pos_from_bit_count(bit_count)
        byte1, bit1 = pos_from_bit_count(bit_count + 5)
        if byte0 == byte1:
            b = rm[c] << bit1
            buf[byte0] = buf[byte0] | b
        else:
            assert byte0 + 1 == byte1
            b0 = rm[c] >> (5 - bit0)
            buf[byte0] = buf[byte0] | b0
            right = bit1
            op = and_operand(right, 7)
            b1 = (rm[c] << right) & op
            buf[byte1] = buf[byte1] | b1
        bit_count += 5
    return b''.join([chr(c & 0xff).encode() for c in buf])


def check(_bytes):
    if _bytes != _bytes.upper():
        return False
    for c in _bytes[:-1]:
        if c not in tm:
            return False
    tail = _bytes[-1]
    if tail not in tm and tail not in suffix:
        return False


def main():
    d = b'1234567890'
    b = b32encode(d)
    print(b, len(b))
    d = b32decode(b)
    print(d, len(d))


def main1():
    print(and_operand(0, 0))


if '__main__' == __name__:
    main()
