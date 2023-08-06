# Copyright 2017, Ryan P. Kelly.

import io
import gzip
import zlib


CHUNK_SIZE = 32768


def _bytes_or_file(fileobj):
    data = fileobj
    if isinstance(fileobj, bytes):
        data = io.BytesIO(fileobj)

    return data


class Compressor(object):

    def __init__(self, fileobj, chunk_size=CHUNK_SIZE):
        self.fileobj = _bytes_or_file(fileobj)
        self.buffer = io.BytesIO()
        self.chunk_size = chunk_size

        self.com = gzip.GzipFile(fileobj=self.buffer, mode="wb")

    def read(self, size=-1):

        no_more_data = False

        while size < 0 or self.buffer.tell() < size:
            chunk = self.fileobj.read(self.chunk_size)
            if not chunk:
                no_more_data = True
                break

            self.com.write(chunk)
            if size > 0 and self.buffer.tell() >= size:
                self.com.flush()
                break

        if no_more_data or size < 0:
            self.com.close()

        self.buffer.seek(0)

        if size < 0:
            ret = self.buffer.getvalue()
            self.buffer.close()
            self.buffer = None
            return ret

        ret = self.buffer.read(size)
        remainder = self.buffer.read()
        self.buffer.seek(0)
        self.buffer.truncate()
        self.buffer.write(remainder)

        return ret


def compress(fileobj, chunk_size=CHUNK_SIZE):
    return Compressor(fileobj, chunk_size=chunk_size)


class Decompressor(object):

    def __init__(self, fileobj, chunk_size=CHUNK_SIZE):
        self.fileobj = _bytes_or_file(fileobj)
        self.buffer = io.BytesIO()
        self.chunk_size = chunk_size

        # offset 32 to skip the header
        self.dec = zlib.decompressobj(32 + zlib.MAX_WBITS)

    def read(self, size=-1):

        while size < 0 or self.buffer.tell() < size:
            chunk = self.fileobj.read(self.chunk_size)
            if not chunk:
                break

            rv = self.dec.decompress(chunk)
            if rv:
                self.buffer.write(rv)

        self.buffer.seek(0)

        if size < 0:
            ret = self.buffer.getvalue()
            self.buffer.close()
            self.buffer = None
            return ret

        ret = self.buffer.read(size)
        remainder = self.buffer.read()
        self.buffer.seek(0)
        self.buffer.truncate()
        self.buffer.write(remainder)

        return ret


def decompress(fileobj, chunk_size=CHUNK_SIZE):
    return Decompressor(fileobj, chunk_size=chunk_size)
