#!/usr/bin/env python
# coding=utf-8

import io
import weapprobot
import platform

from setuptools import setup, find_packages

with io.open("README.rst", encoding="utf8") as f:
    readme = f.read()
readme = readme.replace("latest", "v" + weapprobot.__version__)

version = platform.python_version_tuple()
install_requires = open("requirements.txt").readlines()
if version < ('3', '3'):
    install_requires.append('funcsigs')

setup(
    name='WeAppRobot',
    version=weapprobot.__version__,
    author=weapprobot.__author__,
    author_email='help@instome.com',
    url='https://github.com/instome/WeAppRobot',
    packages=find_packages(),
    keywords="wechat weixin weapp miniprogram weapprobot",
    description='WeAppRobot: writing WeApp Backend Robots with fun',
    long_description=readme,
    install_requires=install_requires,
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    extras_require={
        'crypto': ["cryptography"]
    },
    package_data={'weapprobot': ['contrib/*.html']}
)
