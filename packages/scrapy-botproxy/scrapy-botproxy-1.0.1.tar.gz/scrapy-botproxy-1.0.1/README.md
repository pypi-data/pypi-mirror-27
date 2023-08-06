# scrapy-botproxy

BotProxy downloader middleware for Scrapy.

## Overview

BotProxy is an IP Rotating HTTP Proxy. Plug BotProxy into your web scraping application and it will automatically route your requests through one of our outgoing proxy servers. Multiple locations, fresh IP addresses every day. Typical integrations take less than 5 minutes into any script or application.

Please note, in order to use this service you need to have active subscription. You can get one at [BotProxy website](https://botproxy.net).

## Installation

##### From PyPI

    pip install scrapy-botproxy

##### From GitHub

    pip install -e git+https://github.com/botproxy/scrapy-botproxy@master#egg=scrapy_botproxy

## Usage

settings.py:

    DOWNLOADER_MIDDLEWARES = {
        'scrapy_botproxy.BotProxyMiddleware': 100,
    }

    BOTPROXY_USER = 'proxy_username'
    BOTPROXY_PASSWORD = 'proxy_password'
    BOTPROXY_LOCATION = 'us-ny'  # optional
    BOTPROXY_COUNTRY = 'US'  # optional


You can also control botproxy behavior using scrapy `request.meta` property. Set `botproxy_disable` to `True` to temorary bypass proxy for current request. Set `location` or `country` to route request through selected location or any location in the specific country.
