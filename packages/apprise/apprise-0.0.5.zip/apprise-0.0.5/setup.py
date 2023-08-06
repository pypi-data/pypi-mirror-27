#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SetupTools Script
#
# Copyright (C) 2017 Chris Caron <lead2gold@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

import os
try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

from setuptools import find_packages

install_options = os.environ.get("APPRISE_INSTALL", "").split(",")
libonly_flags = set(["lib-only", "libonly", "no-cli", "without-cli"])
if libonly_flags.intersection(install_options):
    console_scripts = []
else:
    console_scripts = ['apprise = apprise:_main']

setup(
    name='apprise',
    version='0.0.5',
    description='A universal notification service',
    license='GPLv3',
    long_description=open('README.md').read(),
    url='https://github.com/caronc/apprise',
    keywords='push notifications email boxcar faast growl Join KODI '
        'Mattermost NotifyMyAndroid Prowl Pushalot PushBullet Pushjet '
        'Pushover Rocket.Chat Slack Toasty Telegram Twitter XBMC ',
    author='Chris Caron',
    author_email='lead2gold@gmail.com',
    packages=find_packages(),
    package_data={
        'apprise': [
            'assets/NotifyXML-1.0.xsd',
            'assets/themes/default/*.png',
        ],
    },
    scripts=['cli/notify.py', ],
    install_requires=open('requirements.txt').readlines(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ),
    entry_points={'console_scripts': console_scripts},
    python_requires='>=2.7',
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'coverage', 'pytest-cov', 'pycodestyle', 'tox'],
)
