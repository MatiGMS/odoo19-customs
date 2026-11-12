{
    'name': 'Purchase Max Qty Warning (Wizard)',
    'version': '19.0.1.0',
    'category': 'Inventory/Purchase',
    'summary': 'Evita confirmar órdenes que superen el Orderpoint mediante un Wizard.',
    'author': 'KPI+',
    'depends': ['purchase_stock'], 
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/max_qty_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}