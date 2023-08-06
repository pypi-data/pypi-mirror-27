# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Salutes']
__metaclass__ = PoolMeta


class Salutes(ModelSQL, ModelView):
    u'Salutes'
    __name__ = 'writing_serialletter.salutes'

    name = fields.Char(string=u'Name', required=True)
# end Salutes
