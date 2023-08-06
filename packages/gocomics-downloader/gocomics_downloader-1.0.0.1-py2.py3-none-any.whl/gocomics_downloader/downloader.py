#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

import sys, os

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


def download_file(url, dest=None):
    """ 
    Download and save a file specified by url to dest directory,
    """
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not dest is None:
        filename = dest
    else:
        if not filename:
            filename = 'downloaded.file'
        if dest:
            filename = os.path.join(dest, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += int(len(buffer))
            f.write(buffer)
            status = "{b} bytes, {kb} kilobytes, {mb} megabytes".format(b=str(file_size_dl), kb=str(int(round(
                file_size_dl / 1024, 0))), mb=str(int(round(file_size_dl / (1024 ** 2), 0))))
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename


if __name__ == "__main__":  # Only run if this file is called directly
    print("Testing with 10MB download")
    url = "http://speedtest-ny.turnkeyinternet.net/10000mb.bin"
    filename = download_file(url)
    print(filename)
