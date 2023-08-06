# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, If


__all__ = ['Invoice']
__metaclass__ = PoolMeta
 

class Invoice(ModelSQL, ModelView):
    "Invoice"
    __name__ = 'account.invoice'
    
    delivery_date = fields.Date(string=u'Delivery date',
        states={
            'readonly': Eval('state').in_(['posted', 'paid', 'cancel']),
            'required': Eval('state').in_(
                If(Eval('type') == 'in',
                    ['validated', 'posted', 'paid'],
                    ['posted', 'paid'])),
            },
        depends=['state'])

    @classmethod
    def default_invoice_date(cls):
        """ default for invoice_date 'today'
        """
        Date = Pool().get('ir.date')
        return Date.today()

    @classmethod
    def default_delivery_date(cls):
        """ default for deliverydate 'today'
        """
        Date = Pool().get('ir.date')
        return Date.today()
        
# end Invoice
