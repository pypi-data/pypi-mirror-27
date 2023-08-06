# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from sql.conditionals import Case
from sql.functions import Substring, CharLength
from sqlextension import Replace, Concat2

__all__ = ['Party']


class Party(ModelSQL, ModelView):
    'Party'
    __name__ = 'party.party'

    notizen = fields.Text(string=u'Notes')
    notizen_tree = fields.Function(fields.Char(string=u'Notes', readonly=True), 
        'get_notizen_tree', searcher='search_notizen_tree')
    
    @classmethod
    def get_notizen_tree_sql(cls):
        """ get sql-code for 'notizen_tree'
        """
        tab_party = cls.__table__()
        
        qu1 = tab_party.select(tab_party.id,
                tab_party.notizen.as_('fulltext'),
                Case (
                    (CharLength(tab_party.notizen) > 40,
                     Concat2(Substring(Replace(tab_party.notizen, '\n', '; '), 1, 40), '...')
                    ),
                    else_ = Replace(tab_party.notizen, '\n', '; ')
                ).as_('shorttext'),                
            )
        return qu1
        
    @classmethod
    def get_notizen_tree(cls, notes, names):
        """ get notes for selected parties
        """
        tab_note = cls.get_notizen_tree_sql()
        cursor = Transaction().connection.cursor()
        note_ids = [x.id for x in notes]

        # prepare result
        res1 = {'notizen_tree': {}}
        for i in note_ids:
            res1['notizen_tree'][i] = None

        # query
        qu1 = tab_note.select(tab_note.id,
                tab_note.shorttext,
                where=tab_note.id.in_(note_ids)
            )
        cursor.execute(*qu1)
        l1 = cursor.fetchall()
        
        for i in l1:
            (id1, txt1) = i
            res1['notizen_tree'][id1] = txt1
        return res1

    @classmethod
    def search_notizen_tree(cls, name, clause):
        """ search in fulltext
        """
        tab_note = cls.get_notizen_tree_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        
        qu1 = tab_note.select(tab_note.id,
                where=Operator(tab_note.fulltext, clause[2])
            )
        return [('id', 'in', qu1)]

    @staticmethod
    def order_notizen_tree(tables):
        table, _ = tables[None]
        return [table.notizen]

# ende Party
