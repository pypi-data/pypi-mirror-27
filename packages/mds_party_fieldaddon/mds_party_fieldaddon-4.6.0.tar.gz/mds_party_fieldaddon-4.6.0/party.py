# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from sqlextension import Concat2


__all__ = ['Party']
__metaclass__ = PoolMeta


class Party(ModelSQL, ModelView):
    'Party'
    __name__ = 'party.party'
    _rec_name = 'pfacomposedname'

    pfafirstname = fields.Char(string=u'First name')
    pfadepartment = fields.Char(string=u'Department')
    pfacompany = fields.Char(string=u'Company')
    pfacomposedname = fields.Function(fields.Char(string=u'Composed Name', 
            readonly=True), 
            'get_pfacomposedname', searcher='search_pfacomposedname')
    
    @classmethod
    def default_pfafirstname(cls):
        return ''
        
    @classmethod
    def default_pfadepartment(cls):
        return ''

    @classmethod
    def default_pfacompany(cls):
        return ''

    @classmethod
    def search_rec_name(cls, name, clause):
        """ extend search in rec_name for new fields
        """
        qu1 = super(Party, cls).search_rec_name(name, clause)
        qu2 = cls.search_pfacomposedname(name, clause)
        qu1.append(qu2)
        return qu1
    
    @classmethod
    def search_pfacomposedname(cls, name, clause):
        """ gets sql-code for searching
        """
        return ['OR', ('name', 'ilike', clause[2]), 
                    ('pfafirstname', 'ilike', clause[2]),
                    ('pfacompany', 'ilike', clause[2]),
                    ('pfadepartment', 'ilike', clause[2]),
                    ]

    @classmethod
    def get_pfacomposedname(cls, parties, names):
        """ gets Name, Firstname - Company, Department
        """
        erg1 = {'pfacomposedname': {}}
        tab_party = cls.__table__()
        cursor = Transaction().cursor
        
        qu1 = tab_party.select(tab_party.id,
                    Concat2(tab_party.name, u', ', 
                            tab_party.pfafirstname, u' [',
                            tab_party.pfacompany, u', ',
                            tab_party.pfadepartment, ']').as_('compname'),
                    where=tab_party.id.in_([x.id for x in parties])
                )
        
        cursor.execute(*qu1)
        p_lst = cursor.fetchall()
        
        for i in p_lst:
            (id1, txt1) = i
            erg1['pfacomposedname'][id1] = txt1
        return erg1

    @staticmethod
    def order_pfacomposedname(tables):
        """ sort by name --> firstname --> company
        """
        tab_party, _ = tables[None]
        return [tab_party.name, tab_party.pfafirstname, 
                tab_party.pfafirstname, tab_party.pfacompany]

# end Party
