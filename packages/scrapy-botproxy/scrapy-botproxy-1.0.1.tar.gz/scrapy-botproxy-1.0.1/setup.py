# -*- coding: utf-8 -*
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
try:
    import pypandoc
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')
except(IOError, ImportError):
    with open(path.join(here, 'README.md'), encoding='utf-8') as inp:
        long_description = inp.read()

setup(
    name='scrapy-botproxy',
    version='1.0.1',
    packages=['scrapy_botproxy'],
    url='https://github.com/botproxy/scrapy-botproxy',
    license='MIT',
    author='botproxy',
    author_email='%s%s@botproxy.net' % ('sup', 'port'),
    description=(
        'BotProxy (IP Rotating HTTP proxy) downloader middleware'
        'for Scrapy'),
    long_description=long_description,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'scrapy>=1.4.0'
    ],
)
