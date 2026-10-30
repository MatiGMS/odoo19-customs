# -*- coding: utf-8 -*-
{
    'name': 'Website Sale - Custom Sorting & Bestsellers',
    'version': '19.0.1.0.0',
    'category': 'Website/eCommerce',
    'summary': 'Orden por más vendidos y favoritos en destacados para tienda eCommerce',
    'author': 'KPI+ Partner Técnico',
    'license': 'LGPL-3',
    'depends': [
        'website_sale',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}