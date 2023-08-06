#!/usr/bin/env python
"""
Simple SysLog Handler
----------------

Example
```````

.. code:: python

    from simple_syslog_handler import SimpleSysLogHandler

    SimpleSysLogHandler.config_logging()

Links
`````

* `Github <https://github.com/TheWaWaR/simple-syslog-handler>`

"""

from setuptools import setup

setup(
    name='Simple-SysLog-Handler',
    version='0.1.0',
    url='https://github.com/TheWaWaR/simple-syslog-handler',
    license='MIT',
    author='Qian Linfeng',
    author_email='thewawar@gmail.com',
    description='A simple wrapper of logging.handlers.SysLogHandler',
    long_description=__doc__,
    packages=['simple_syslog_handler'],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ]
)
