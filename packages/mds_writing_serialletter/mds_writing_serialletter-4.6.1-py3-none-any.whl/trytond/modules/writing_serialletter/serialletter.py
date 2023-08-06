# -*- coding: utf-8 -*-

from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from sql.functions import DateTrunc


__all__ = ['Serialletter', 'SerialletterRel']
__metaclass__ = PoolMeta


# (placeholdername, fieldname, menutext, formatstring, replacelist, replacedict)
repl_party_lst = [
        ('partyname','full_name', u'Name', '%s', [], None),
        ('salutation','salutation_string', u'Form of address', '%s', [], None),
        ('greeting','greeting_string', u'Greeting', '%s', [], None),
        ('correspondence','welcoming', u'Correspondence intro', '%s', [], None),
        ('phone','phone', u'Phone', '%s', [], None),
        ('mobile','mobile', u'Mobile', '%s', [], None),
        ('fax','fax', u'Fax', '%s', [], None),
        ('email','email', u'E-Mail', '%s', [], None),
        ('website','website', u'Website', '%s', [], None),
        ('addrname','mailaddrname', u'Name of Address', '%s', [], None),
        ('zip','mailaddrzip', u'ZIP', '%s', [], None),
        ('city','mailaddrcity', u'City', '%s', [], None),
        ('street','mailaddrstreet', u'Street', '%s', [], None),
        ('firstname','pfafirstname', u'First name', '%s', [], None),
        ('department','pfadepartment', u'Department', '%s', [], None),
        ('company','pfacompany', u'Company', '%s', [], None),
        ('country','mailaddrcountry', u'Country', '%s', [], None),
    ]

repl_contact_lst = [
        ('name','full_name', u'Name', '%s', [], None),
        ('salutation','salutation_string', u'Form of address', '%s', [], None),
        ('phone','phone', u'Phone', '%s', [], None),
        ('mobile','mobile', u'Mobile', '%s', [], None),
        ('fax','fax', u'Fax', '%s', [], None),
        ('email','email', u'E-Mail', '%s', [], None),
        ('website','website', u'Website', '%s', [], None),
        ('firstname','pfafirstname', u'First name', '%s', [], None),
        ('department','pfadepartment', u'Department', '%s', [], None),
        ('company','pfacompany', u'Company', '%s', [], None),
    ]

SEL_PLCHLDR_NONE = 'none'
sel_placeholder =[(SEL_PLCHLDR_NONE, u'-- insert placeholder --')]
dict_placeholder = {}
for i in repl_party_lst:
    (k1, k2, t1, f1, l1, d1) = i
    sel_placeholder.append(('pty:%s' % k1, u'Receiver: %s' % t1))
    dict_placeholder['pty:%s' % k1] = '[party:%s]' % k1
for i in repl_contact_lst:
    (k1, k2, t1, f1, l1, d1) = i
    sel_placeholder.append(('ct:%s' % k1, u'Contact: %s' % t1))
    dict_placeholder['ct:%s' % k1] = '[contact:%s]' % k1


WF_SERIALLETTER_EDIT = 'b'
WF_SERIALLETTER_FINISHED = 'f'
sel_state = [(WF_SERIALLETTER_EDIT, u'Editing'),
            (WF_SERIALLETTER_FINISHED, u'Finished')]


class Serialletter(Workflow, ModelSQL, ModelView):
    u'Serial letter'
    __name__ = 'writing_serialletter.letter'

    name = fields.Char(string=u'Name', required=True, depends=['state'],
                    help=u'Description of the serial letter',
                    states = {
                        'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    })
    subject = fields.Char(string=u'Subject', required=True, depends=['state'],
                    states = {
                        'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    })
    text = fields.Text(string=u'Text', required=True, depends=['state'],
                    states = {
                        'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    })
    created = fields.Function(fields.Date(string=u'created', readonly=True), 
                    'get_dates', searcher='search_created')
    edited = fields.Function(fields.Date(string=u'edited', readonly=True), 
                    'get_dates', searcher='search_edited')
    placeholder = fields.Selection(string=u'Placeholder', 
                    help=u'The selected placeholder is inserted at the end of the text.',
                    selection=sel_placeholder, depends=['state'],
                    states = {
                        'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    })
    parties = fields.Many2Many(relation_name='writing_serialletter.letter_rel',
                    origin='serlettr', target='party', string=u'Parties', depends=['state'],
                    states = {
                        'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    })
    contact = fields.Many2One(string=u'Contact', required=True, depends=['state'],
                        help=u'Contact for the serial letter',
                        model_name=u'party.party',
                        states = {
                            'readonly': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                        })
    finished_at = fields.Date(string=u'finished', readonly=True)
    state = fields.Selection(selection=sel_state, string=u'State', select=True, readonly=True)
    state_string = state.translated('state')

    @classmethod
    def __setup__(cls):
        super(Serialletter, cls).__setup__()
        cls._order.insert(0, ('finished_at', 'DESC'))
        cls._transitions |= set((
                (WF_SERIALLETTER_EDIT, WF_SERIALLETTER_FINISHED),
                ))
        cls._buttons.update({
                'finishletter': {
                    'invisible': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                    },
                'enable_mailaddresses': {
                    'invisible': Eval('state').in_([WF_SERIALLETTER_FINISHED]),
                },
                })
        cls._error_messages.update({
                'delete_serialletter': (u"The serial letter is '%s' and can not be deleted."),
                'missing_address': (u"The party '%s' (code: %s) has no address."),
                })

    @classmethod
    def default_placeholder(cls):
        return SEL_PLCHLDR_NONE

    @classmethod
    def default_contact(cls):
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return user.contactlettr and user.contactlettr.id or None

    @classmethod
    def default_state(cls):
        return WF_SERIALLETTER_EDIT

    @classmethod
    @ModelView.button
    def enable_mailaddresses(cls, letters):
        """ activate mailing addresses
        """
        pool = Pool()
        Address = pool.get('party.address')
        Party = pool.get('party.party')
        LettrRel = pool.get('writing_serialletter.letter_rel')
        tab_adr = Address.__table__()
        tab_party = Party.__table__()
        tab_lettr = cls.__table__()
        tab_rel = LettrRel.__table__()
        cursor = Transaction().connection.cursor()
        
        if len(letters) == 0:
            return
            
        # find parties having already mailing-addresses
        tab_enabled_parties = tab_lettr.join(tab_rel, condition=tab_lettr.id==tab_rel.serlettr
                ).join(tab_party, condition=tab_party.id==tab_rel.party
                ).join(tab_adr, condition=tab_adr.party==tab_party.id
                ).select(tab_party.id,
                    group_by=(tab_party.id, tab_adr.mailing_addr),
                    having=tab_adr.mailing_addr==True,
                    where=tab_lettr.id.in_([x.id for x in letters])
                )

        # find not enabled mailing addresses
        qu1 = tab_lettr.join(tab_rel, condition=tab_lettr.id==tab_rel.serlettr
                ).join(tab_party, condition=tab_party.id==tab_rel.party
                ).select(tab_party.id,
                    where=~tab_party.id.in_(tab_enabled_parties) &
                        tab_lettr.id.in_([x.id for x in letters])
                )
        cursor.execute(*qu1)
        todo_lst = cursor.fetchall()
        
        # enable first address
        for i in todo_lst:
            (id1, ) = i
            
            p1 = Party(id1)
            if len(p1.addresses) == 0:
                cls.raise_user_error('missing_address', (p1.name, p1.code))

            for k in p1.addresses:
                k.mailing_addr = True
                k.save()
                break

    @fields.depends('placeholder', 'text')
    def on_change_placeholder(self):
        """ inserts the placeholder
        """
        if not isinstance(self.placeholder, type(None)) and \
            not isinstance(self.text, type(None)):
            if self.placeholder != SEL_PLCHLDR_NONE:
                self.text += dict_placeholder.get(self.placeholder, '')
                self.placeholder = SEL_PLCHLDR_NONE

    @classmethod
    def search_created(cls, name, clause):
        """ sql-code for search
        """
        pool = Pool()
        SerLettr = pool.get('writing_serialletter.letter')
        tab_serlettr = SerLettr.__table__()
        
        Operator = fields.SQL_OPERATORS[clause[1]]
        qu1 = tab_serlettr.select(tab_serlettr.id, 
                        where=Operator(DateTrunc('day', tab_serlettr.create_date), clause[2])
                    )
        return [('id', 'in', qu1)]
        
    @classmethod
    def search_edited(cls, name, clause):
        """ sql-code for search
        """
        pool = Pool()
        SerLettr = pool.get('writing_serialletter.letter')
        tab_serlettr = SerLettr.__table__()
        
        Operator = fields.SQL_OPERATORS[clause[1]]
        qu1 = tab_serlettr.select(tab_serlettr.id, 
                        where=Operator(DateTrunc('day', tab_serlettr.write_date), clause[2])
                    )
        return [('id', 'in', qu1)]

    @classmethod
    def get_dates(cls, serlettrs, names):
        """ get dates
        """
        erg1 = {'created':{}, 'edited':{}}
                
        pool = Pool()
        SerLettr = pool.get('writing_serialletter.letter')
        tab_serlettr = SerLettr.__table__()
        cursor = Transaction().connection.cursor()

        qu1 = tab_serlettr.select(tab_serlettr.id,
                    DateTrunc('day', tab_serlettr.create_date).as_('created'),
                    DateTrunc('day', tab_serlettr.write_date).as_('edited'),
                    where=tab_serlettr.id.in_([x.id for x in serlettrs])
                )
        cursor.execute(*qu1)
        txinf = cursor.fetchall()
        
        for i in txinf:
            (id1, cr1, ed1) = i
            erg1['created'][id1] = cr1.date()
            erg1['edited'][id1] = None
            if not isinstance(ed1, type(None)):
                erg1['edited'][id1] = ed1.date()            

        # remove not requested infos
        erg2 = {}
        for i in erg1.keys():
            if i in names:
                erg2[i] = erg1[i]
        return erg1

    @classmethod
    def replace_placeholder(cls, pty_obj, cont_obj, text):
        """ return the text with replaced placeholders
            pty_obj = party
            cont_obj = contact
            text = letter text
        """
        for m in [
                (pty_obj, 'party', repl_party_lst),
                (cont_obj, 'contact', repl_contact_lst)
                ]:
            (quell_obj, namesp, namelst) = m
            
            if not isinstance(quell_obj, type(None)):
                for i in namelst:
                    (suchkey, key1, beschr, form1, repllst, dictquelle) = i
                    
                    obj_attr = getattr(quell_obj, key1)

                    if isinstance(obj_attr, type(None)):
                        neutxt = ''
                    else :
                        if isinstance(dictquelle, type(None)):
                            neutxt = form1 % obj_attr
                        else :
                            neutxt = form1 % dictquelle[obj_attr]

                    for k in repllst:
                        (von, nach) = k
                        neutxt = neutxt.replace(von, nach)
                    text = text.replace(u'[%s:%s]' % (namesp, suchkey), neutxt)

        return text

    @classmethod
    @ModelView.button
    @Workflow.transition(WF_SERIALLETTER_FINISHED)
    def finishletter(cls, seriallettr):
        """ finishing the letter
        """
        pool = Pool()
        Date = pool.get('ir.date')
        for i in seriallettr:
            i.finished_at = Date.today()
            i.save()

    @classmethod
    def delete(cls, seriallettr):
        if not seriallettr:
            return True
        for i in seriallettr:
            if i.state == WF_SERIALLETTER_FINISHED:
                cls.raise_user_error('delete_serialletter', (i.state_string))
        return super(Serialletter, cls).delete(seriallettr)

# ende Serialletter


class SerialletterRel(ModelSQL):
    'Serial letter - Party'
    __name__ = 'writing_serialletter.letter_rel'
    
    serlettr = fields.Many2One(model_name='writing_serialletter.letter', 
                string=u'Serial letter', ondelete='CASCADE',
                required=True, select=True)
    party = fields.Many2One(model_name='party.party', 
                string=u'Party', ondelete='SET NULL', 
                required=True, select=True)
# ende SerialletterRel
