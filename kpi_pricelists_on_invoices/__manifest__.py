{
    'name': 'KPI+ Tarifa de Venta en Facturas',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Agrega la lista de precios de la SO de origen en facturas y listas',
    'author': 'KPI+',
    'depends': [
        'account', 
        'sale',
        'account_payment_pro',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/account_move_line_views.xml', 
        'views/account_payment_views.xml',  
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}