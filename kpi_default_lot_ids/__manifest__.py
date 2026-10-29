# -*- coding: utf-8 -*-
{
    'name': 'Stock Picking Empty Lots by Default',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Evita la asignación automática de lotes en transferencias de stock',
    'author': 'KPI+',
    'license': 'LGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}