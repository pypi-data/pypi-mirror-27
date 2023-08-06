# coding: utf-8

import sys
import logging
import logging.config
import logging.handlers


SYSLOG_ADDRESS = '/var/run/syslog' if sys.platform == 'darwin' else '/dev/log'


class SimpleSysLogHandler(logging.handlers.SysLogHandler):

    DEFAULTS = {
        'format': '%(levelname)s - %(message)s',
        'level': 'DEBUG',
        'address': SYSLOG_ADDRESS,
        'facility': 'local6',
        'ident': 'python',
    }

    def __init__(self, **kwargs):
        Cls = self.__class__
        kwargs.setdefault('address', Cls.DEFAULTS['address'])
        kwargs.setdefault('facility', Cls.DEFAULTS['facility'])
        ident = kwargs.pop('ident', Cls.DEFAULTS['ident'])
        super(Cls, self).__init__(**kwargs)
        self.ident = ident

    def format(self, record):
        msg = super(self.__class__, self).format(record)
        return u'{}[{}]: {}'.format(self.ident, record.process, msg)

    @classmethod
    def config_logging(Cls,
                       format=None,
                       level=None,
                       address=None,
                       facility=None,
                       ident=None):
        """
        [Reference]:
          https://docs.python.org/2/howto/logging-cookbook.html#configuring-filters-with-dictconfig
        """

        class_name = '{}.{}'.format(__name__, Cls.__name__)
        format = format or Cls.DEFAULTS['format']
        level = level or Cls.DEFAULTS['level']
        address = address or Cls.DEFAULTS['address']
        facility = facility or Cls.DEFAULTS['facility']
        ident = ident or Cls.DEFAULTS['ident']

        log_config = {
            'version': 1,
            'formatters': {
                'local': {
                    'format': format,
                }
            },
            'handlers': {
                'syslog': {
                    'class': class_name,
                    'formatter': 'local',
                    'address': address,
                    'facility': facility,
                    'ident': ident,
                },
            },
            'root': {
                'level': level,
                'handlers': ['syslog']
            },
        }
        logging.config.dictConfig(log_config)
