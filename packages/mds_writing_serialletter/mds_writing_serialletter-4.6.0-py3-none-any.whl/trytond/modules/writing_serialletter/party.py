# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from sql.functions import CharLength


__all__ = ['Party']
__metaclass__ = PoolMeta


class Party(ModelSQL, ModelView):
    "Party" 
    __name__ = 'party.party'
    
    salutation = fields.Many2One(model_name='writing_serialletter.salutes', 
                    string=u'Form of address', help=u'Ms., Mr. etc.')
    salutation_string = fields.Function(fields.Char(string=u'Form of address String', 
                    readonly=True), 'get_greetings')
    greeting = fields.Many2One(model_name='writing_serialletter.greetings', 
                    string=u'Greeting', help=u'Dear, Hello, Hi, etc.')
    greeting_string = fields.Function(fields.Char(string=u'Welcoming String', 
                    readonly=True), 'get_greetings')
    welcoming = fields.Function(fields.Char('Correspondence intro', 
                    help=u'Welcoming in letter (placeholder: [party:correspondence])', readonly=True), 'get_welcoming')
    mailingaddr_valid = fields.Function(fields.Boolean(string=u'Valid mailing address',
                    help=u'Party has a valid mailing address',
                    readonly=True), 'get_mailingaddr_valid', searcher='search_mailingaddr_valid')
    mailaddrname = fields.Function(fields.Char('Mailing - Name-Address', readonly=True), 'get_mailaddr')
    mailaddrzip = fields.Function(fields.Char('Mailing - Zip-Address', readonly=True), 'get_mailaddr')
    mailaddrcity = fields.Function(fields.Char('Mailing - City-Address', readonly=True), 'get_mailaddr')
    mailaddrstreet = fields.Function(fields.Char('Mailing - Street-Address', readonly=True), 'get_mailaddr')
    mailaddrcountry = fields.Function(fields.Char('Mailing - Country-Address', readonly=True), 'get_mailaddr')

    @classmethod
    def get_mailingaddr_valid_sql(cls):
        """ sql-code for valid-mailingaddress
        """
        pool = Pool()
        Address = pool.get('party.address')
        Party = pool.get('party.party')
        tab_adr = Address.__table__()
        tab_party = Party.__table__()

        qu1 = tab_party.join(tab_adr, condition=tab_party.id==tab_adr.party
                ).select(tab_party.id,
                    where=(tab_adr.mailing_addr == True) &
                        (tab_adr.active == True) &
                        (CharLength(tab_adr.zip) > 0) & 
                        (CharLength(tab_adr.city) > 0) & 
                        (CharLength(tab_adr.street) > 0)
                )
        return qu1
        
    @classmethod
    def search_mailingaddr_valid(cls, name, clause):
        """ create sql-code for search
        """
        tab_validadr = cls.get_mailingaddr_valid_sql()
        tab_party = cls.__table__()
        Operator = fields.SQL_OPERATORS[clause[1]]

        if clause[2] == True:
            adrvalid = tab_party.select(tab_party.id, 
                            where=tab_party.id.in_(tab_validadr)
                        )
        else :
            adrvalid = tab_party.select(tab_party.id, 
                            where=~tab_party.id.in_(tab_validadr)
                        )
        return [('id', 'in', adrvalid)]
        
    @classmethod
    def get_mailingaddr_valid(cls, parties, names):
        """ search for parties with valid mailing address
        """
        erg1 = {'mailingaddr_valid': {}}
        
        if len(parties) == 0:
            return erg1

        p_lst = [x.id for x in parties]
        tab_validadr = cls.get_mailingaddr_valid_sql()
        cursor = Transaction().connection.cursor()
                    
        # prepare result
        for i in p_lst:
            erg1['mailingaddr_valid'][i] = False
        
        pool = Pool()
        Address = pool.get('party.address')
        Party = pool.get('party.party')
        tab_adr = Address.__table__()
        tab_party = Party.__table__()

        # search for valid addresses
        qu1 = tab_validadr.select(tab_validadr.id.as_('id_party'),
                where=tab_validadr.id.in_(p_lst)
            )
        cursor.execute(*qu1)
        party_lst = cursor.fetchall()
        
        for i in party_lst:
            (id_party,) = i
            erg1['mailingaddr_valid'][id_party] = True
        return erg1
        
    @classmethod
    def get_mailaddr(cls, parties, names):
        """ gets fields of mailing address
        """
        erg1 = {'mailaddrname': {}, 'mailaddrzip': {}, 'mailaddrcity':{}, 
                'mailaddrstreet': {}, 'mailaddrcountry': {}}

        pool = Pool()
        Address = pool.get('party.address')
        Party = pool.get('party.party')
        tab_adr = Address.__table__()
        tab_party = Party.__table__()
        cursor = Transaction().connection.cursor()

        p_lst = [x.id for x in parties]
        
        # prepare result
        for i in p_lst:
            erg1['mailaddrname'][i] = ''
            erg1['mailaddrzip'][i] = ''
            erg1['mailaddrcity'][i] = ''
            erg1['mailaddrstreet'][i] = ''
            erg1['mailaddrcountry'][i] = ''
        
        qu1 = tab_party.join(tab_adr, condition=tab_party.id==tab_adr.party
                ).select(tab_party.id,
                    tab_adr.id, 
                    tab_adr.name, 
                    tab_adr.zip, 
                    tab_adr.city, 
                    tab_adr.street,
                    where=(tab_adr.mailing_addr == True) & \
                        tab_party.id.in_(p_lst)
                )
        cursor.execute(*qu1)
        party_lst = cursor.fetchall()
        
        for i in party_lst:
            (id_party, id_adr, name1, zip1, city1, street1) = i
            erg1['mailaddrname'][id_party] = name1
            erg1['mailaddrzip'][id_party] = zip1
            erg1['mailaddrcity'][id_party] = city1
            erg1['mailaddrstreet'][id_party] = street1
            adr_obj = Address(id_adr)
            if isinstance(adr_obj, type(None)):
                erg1['mailaddrcountry'][id_party] = adr_obj.country.name
        
        erg2 = {}
        for i in erg1.keys():
            if i in names:
                erg2[i] = erg1[i]
        return erg2

    @classmethod
    def get_greetings(cls, parties, names):
        """ gets texts from many2one
        """
        erg1 = {'salutation_string': {}, 'greeting_string': {}}
        
        for i in parties:
            erg1['salutation_string'][i.id] = ''
            if not isinstance(i.salutation, type(None)):
                erg1['salutation_string'][i.id] = i.salutation.name
            erg1['greeting_string'][i.id] = ''
            if not isinstance(i.greeting, type(None)):
                erg1['greeting_string'][i.id] = i.greeting.name

        erg2 = {}
        for i in erg1.keys():
            if i in names:
                erg2[i] = erg1[i]
        return erg1
        
    @classmethod
    def get_welcoming(cls, parties, names):
        """ gets welcometexts
        """
        erg1 = {'welcoming': {}}
        
        for i in parties:
            t2 = u''
            if not isinstance(i.greeting, type(None)):
                t2 = u'%s ' % i.greeting.name

            t3 = u''
            if not isinstance(i.salutation, type(None)):
                t3 = u'%s ' % i.salutation.name

            t1 = u'%s%s%s' % (t2, t3, i.name)
            erg1['welcoming'][i.id] = t1.strip()

        erg2 = {}
        for i in erg1.keys():
            if i in names:
                erg2[i] = erg1[i]
        return erg1
# end Party


class Address(ModelSQL, ModelView):
    "Address"
    __name__ = 'party.address'
    mailing_addr = fields.Boolean(string=u'Mailing address', 
                    help=u'use this address for serial letter')
# end Address
