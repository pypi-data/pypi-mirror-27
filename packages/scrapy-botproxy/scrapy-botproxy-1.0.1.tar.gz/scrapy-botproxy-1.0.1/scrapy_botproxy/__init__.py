# -*- coding: utf-8 -*
import base64
from scrapy.exceptions import NotConfigured


class BotProxyMiddleware(object):
    def __init__(self, settings):
        self.proxy_user = settings.get('BOTPROXY_USER')
        self.proxy_password = settings.get('BOTPROXY_PASSWORD')
        if self.proxy_user is None or self.proxy_password is None:
            raise NotConfigured(
                'BOTPROXY_USER and BOTPROXY_PASSWORD must be set')
        if not settings.getbool('PROXYMESH_ENABLED', True):
            raise NotConfigured
        self.location = settings.get('BOTPROXY_LOCATION')
        self.country = settings.get('BOTPROXY_COUNTRY')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        # ignore if proxy is already set
        if 'proxy' in request.meta:
            return

        if request.meta.get('botproxy_disable', False):
            return

        # build username
        user = self.proxy_user
        if self.location:
            user += '+%s' % self.location
        elif self.country:
            user += '+%s' % self.country
        user_pass = '%s:%s' % (user, self.proxy_password)
        creds = base64.b64encode(user_pass.encode()).strip()
        request.meta['proxy'] = 'http://x.botproxy.net:8080'
        request.headers['Proxy-Authorization'] = b'Basic ' + creds
