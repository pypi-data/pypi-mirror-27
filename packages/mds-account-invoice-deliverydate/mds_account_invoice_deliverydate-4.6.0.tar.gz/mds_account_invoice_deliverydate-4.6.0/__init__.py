from trytond.pool import Pool
from .invoice import Invoice

def register():
    Pool.register(
        Invoice,
        module='account_invoice_deliverydate', type_='model')
