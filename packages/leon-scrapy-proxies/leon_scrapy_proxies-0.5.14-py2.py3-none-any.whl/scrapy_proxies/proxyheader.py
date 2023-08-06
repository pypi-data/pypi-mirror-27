# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from faker import Faker
faker = Faker()

log = logging.getLogger('scrapy.proxies')

class Mode:
    RANDOMIZE_PROXY_HEADER, LOCAL_PROXY_HEADER = range(2)

class ProxyHeader(object):
    def __init__(self, settings):
        self.mode = int(settings.get('PROXY_HEADER_MODE'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # allow spider instance to control if enable proxy or not
        if not getattr(spider, 'enable_proxy_header', False):
            return

        ipaddr = '127.0.0.1'

        if self.mode == Mode.RANDOMIZE_PROXY_HEADER:
            ipaddr = faker.ipv4()

        request.headers['X-Originating-IP'] = ipaddr
        request.headers['X-Forwarded-For'] = ipaddr
        request.headers['X-Remote-IP'] = ipaddr
        request.headers['X-Remote-Addr'] = ipaddr
        request.headers['X-Client-IP'] = ipaddr
