# -*- coding: utf-8 -*-
{
    'name': 'KPI+ MRP Shop Floor Tags',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Muestra etiquetas de producción en las tarjetas del módulo Taller',
    'depends': [
        'mrp',
        'mrp_workorder',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'kpi_mrp_shopfloor_tags/static/src/scss/mrp_workorder_tags.scss',
            'kpi_mrp_shopfloor_tags/static/src/js/workorder_tags.js',
            'kpi_mrp_shopfloor_tags/static/src/xml/mrp_workorder_tags.xml',
        ],
        'mrp_workorder.assets_shopfloor': [
            'kpi_mrp_shopfloor_tags/static/src/scss/mrp_workorder_tags.scss',
            'kpi_mrp_shopfloor_tags/static/src/js/workorder_tags.js',
            'kpi_mrp_shopfloor_tags/static/src/xml/mrp_workorder_tags.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}