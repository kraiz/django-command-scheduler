#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-command-scheduler',
    description='Runs your Django management commands via crontab or onclick in admin site and gives you some success and log infos.',
    version='0.1.0',
    author='Lars Kreisz',
    author_email='der.kraiz@gmail.com',
    license='MIT',
    url='https://github.com/ponyriders/django-command-scheduler',
    long_description=open('README.rst').read(),
    packages=[
        'command_scheduler',
        'command_scheduler.management',
        'command_scheduler.management.commands'
    ],
    requires=[
        'Django',
        'croniter>=0.3.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ]
)
