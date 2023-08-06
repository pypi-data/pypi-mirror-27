#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Management tools for RapidPro components """

from codecs import open

from setuptools import setup, find_packages

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='rapidpro_controller',
    version='1.0',
    description="Management tools for RapidPro components",
    long_description=readme,
    author='renaud gaudin',
    author_email='rgaudin@gmail.com',
    url='http://github.com/rgaudin/rapidpro-controller',
    keywords="rapidpro",
    license="Public Domain",
    packages=find_packages('.'),
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    package_data={'': ['README.rst', 'LICENSE']},
    package_dir={'rapidpro_controller': 'rapidpro_controller'},
    install_requires=[
        'termcolor',
        'path.py',
        'requests',
        'simplejson',
        'iso8601',
    ],
    scripts=[
        'rapidpro-alert',
        'rapidpro-backup-cleanup',
        'rapidpro-change-role',
        'rapidpro-change-status',
        'rapidpro-cluster-available',
        'rapidpro-cluster-check',
        'rapidpro-cluster-ip',
        'rapidpro-cluster-requestip',
        'rapidpro-cluster-setipmaster',
        'rapidpro-cluster-status',
        'rapidpro-cluster-unavailable',
        'rapidpro-config',
        'rapidpro-configure-master',
        'rapidpro-configure-slave',
        'rapidpro-disable',
        'rapidpro-dumpdb',
        'rapidpro-enable',
        'rapidpro-html-state',
        'rapidpro-monit-reconfigure',
        'rapidpro-notify-peer',
        'rapidpro-peer-state',
        'rapidpro-pgdump-to',
        'rapidpro-postgres-status',
        'rapidpro-receive-notif',
        'rapidpro-record-failure',
        'rapidpro-record-ipmaster',
        'rapidpro-record-ipslave',
        'rapidpro-restart',
        'rapidpro-set-clustermode',
        'rapidpro-set-role',
        'rapidpro-set-status',
        'rapidpro-start',
        'rapidpro-state',
        'rapidpro-status',
        'rapidpro-stop',
        'rapidpro-test-sms',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
