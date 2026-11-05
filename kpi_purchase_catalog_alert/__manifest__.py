# -*- coding: utf-8 -*-
{
    'name': 'KPI Purchase Catalog Stock Max Warning',
    'version': '19.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Alerta interactiva de stock máximo al salir del catálogo de compras',
    'author': 'KPI+',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        'product',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'kpi_purchase_catalog_alert/static/src/js/product_catalog_controller.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}