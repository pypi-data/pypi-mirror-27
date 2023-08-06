# -*- coding: utf-8 -*-

from trytond.pool import Pool, PoolMeta
from trytond.modules.company import CompanyReport
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.error import WarningErrorMixin
from datetime import date

__all__ = ['SerialletterOdt']
__metaclass__ = PoolMeta


class SerialletterOdt(WarningErrorMixin, CompanyReport):
    __name__ = 'writing_serialletter.report_serialletter'

    _error_messages = {}
    
    @classmethod
    def __setup__(cls):
        super(SerialletterOdt, cls).__setup__()
        cls._error_messages.update({
                'no_mailing_addr': (u"The party '%s' has no mailing address. Please activate an address for the mailing."),
                })

    @classmethod
    def get_context(cls, records, data):
        report_context = super(SerialletterOdt, cls).get_context(records, data)
        report_context['lettertext'] = cls.get_lettertext
        report_context['mailingaddr'] = cls.get_mailing_addr
        report_context['mailingaddrobj'] = cls.get_mailing_addrobj
        report_context['contactaddr'] = cls.get_contact_addr
        report_context['islastitem'] = cls.is_last_item
        report_context['formatdatum'] = cls.format_datum
        return report_context

    @classmethod
    def format_datum(cls, datum):
        """ datumsschreibweise: dd.mm.yyyy
        """
        if not isinstance(datum, type(None)):
            try :
                return datum.strftime('%d.%m.%Y')
            except :
                return str(datum)
        else :
            return '--.--.----'

    @classmethod
    def is_last_item(cls, liste, item):
        """ ermittelt ob der 'item' der letzte in der 'liste'' ist
        """
        if liste[-1].id == item.id:
            return True
        else :
            return False

    @classmethod
    def get_mailing_addr(cls, party):
        """ get first mailing-address
        """
        t1 = u"no mailing address, please enable 'mailing address' at the party-address"
        if not isinstance(party, type(None)):
            if not isinstance(party.addresses, type(None)):
                for i in party.addresses:
                    if i.mailing_addr == True:
                        return i.full_address
        return t1

    @classmethod
    def get_mailing_addrobj(cls, party):
        """ get first mailing-address
        """
        if not isinstance(party, type(None)):
            if not isinstance(party.addresses, type(None)):
                for i in party.addresses:
                    if i.mailing_addr == True:
                        return i
        cls.raise_user_error('no_mailing_addr', (party.name))

    @classmethod
    def get_contact_addr(cls, party):
        """ get first contact-address
        """
        t1 = u"no contact address, please create a address at the contact"
        if not isinstance(party, type(None)):
            if not isinstance(party.addresses, type(None)):
                for i in party.addresses:
                    return i.full_address
        return t1

    @classmethod
    def get_lettertext(cls, letter, party):
        """ creates the individual letter
        """
        LettrObj = Pool().get('writing_serialletter.letter')
        return LettrObj.replace_placeholder(party, letter.contact, letter.text)

    @classmethod
    def execute(cls, ids, data):
        """ change filename
        """
        ExpObj = Pool().get(data['model'])(data['id'])
        (ext1, cont1, dirprint, titel) = super(SerialletterOdt, cls).execute(ids, data)
        titel = '%s-serialletter-%s' % (date.today().strftime('%Y%m%d'), ExpObj.name)
        return (ext1, cont1, dirprint, titel)
# end SerialletterOdt
