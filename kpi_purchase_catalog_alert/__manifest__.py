# -*- coding: utf-8 -*-
{
    'name': 'KPI Purchase Catalog Stock Max Warning',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Valida stock máximo directamente contra la cantidad pedida',
    'author': 'KPI+',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_warning_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}