# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Greetings']
__metaclass__ = PoolMeta


class Greetings(ModelSQL, ModelView):
    u'Greetings'
    __name__ = 'writing_serialletter.greetings'

    name = fields.Char(string=u'Name', required=True)
