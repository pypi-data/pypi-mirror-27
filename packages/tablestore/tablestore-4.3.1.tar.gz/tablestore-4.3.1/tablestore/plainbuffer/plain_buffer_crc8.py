# -*- coding: utf8 -*-

import sys
import six
import crcmod
import struct
from builtins import bytes

class PlainBufferCrc8(object):
    @staticmethod
    def update(crc, bytes_):
        return PlainBufferCrc8._update(crc, bytes_)

    @staticmethod
    def _update(crc, bytes_):
        if isinstance(bytes_, six.text_type):
            bytes_ = bytes_.encode('utf-8')
        elif not isinstance(bytes_, six.binary_type):
            raise TypeError("must be string or buffer, actual:" + str(type(bytes_)))
        crc8Checker = crcmod.predefined.Crc('crc-8')
        crc = crc8Checker._crc(bytes_, crc = crc)
        
        return crc

    @staticmethod
    def crc_string(crc, bytes_):
        return PlainBufferCrc8.update(crc, bytes_)

    @staticmethod
    def crc_int8(crc, byte):
        crcChecker = crcmod.predefined.Crc('crc-8')
        crc = crcChecker._crc(bytes([byte]), crc = crc)
        return crc

    @staticmethod
    def crc_int32(crc, byte):
        for i in range(0, 4):
            crc = PlainBufferCrc8.crc_int8(crc, (byte>>(i*8)) & 0xff)
        return crc

    @staticmethod
    def crc_int64(crc, byte):
        crcChecker = crcmod.predefined.Crc('crc-8')
        crc=crcChecker._crc(struct.pack('q', byte), crc=crc)
        return crc


__all__ = ['PlainBufferCrc8']
