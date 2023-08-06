# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta


__all__ = ['User']
__metaclass__ = PoolMeta


class User(ModelSQL, ModelView):
    __name__ = "res.user"
    
    contactlettr = fields.Many2One(model_name=u'party.party', 
            string=u'Contact', help=u'Contact for serial letter')

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        if 'contactlettr' not in cls._preferences_fields:
            cls._preferences_fields.extend([
                    'contactlettr',
                    ])
