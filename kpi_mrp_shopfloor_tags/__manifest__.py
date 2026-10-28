# -*- coding: utf-8 -*-
{
    'name': 'KPI+ Shop Floor MO Tags',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Muestra etiquetas de mrp.production en el Shopfloor de Odoo',
    'depends': [
        'mrp',
        'mrp_workorder',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'kpi_mrp_shopfloor_tags/static/src/scss/mrp_workorder_tags.scss',
            'kpi_mrp_shopfloor_tags/static/src/xml/mrp_workorder_tags.xml',
        ],
        # Bundle específico de Shop Floor (crítico si no carga en la terminal)
        'mrp_workorder.assets_shopfloor': [
            'kpi_mrp_shopfloor_tags/static/src/scss/mrp_workorder_tags.scss',
            'kpi_mrp_shopfloor_tags/static/src/xml/mrp_workorder_tags.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}