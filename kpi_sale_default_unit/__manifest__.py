{
    'name': 'KPI+ Sale Default Unit',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'author': 'KPI+',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'sale_management',
        'uom',
        'website_sale',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'kpi_sale_default_unit/static/src/js/website_sale_default_uom.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}