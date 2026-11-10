{
    'name': 'KPI: Tarifa de Venta en Facturas',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Agrega la lista de precios de la SO de origen en facturas y listas',
    'author': 'KPI+',
    'depends': ['account', 'sale'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}