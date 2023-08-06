# coding: utf-8

import os
import sys
from setuptools import setup, find_packages
from pip.req import parse_requirements

setup(
    name='ecs_manager',
    version='0.0.5',
    url='https://github.com/pistatium/ecs_service_manager',
    author='pistatium',
    description='Manage ecs service',
    packages=['ecs_manager'],
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'ecs_manager=ecs_manager.cmd:main'
        ]
    },
)

