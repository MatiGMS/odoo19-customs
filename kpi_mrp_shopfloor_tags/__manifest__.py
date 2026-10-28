# -*- coding: utf-8 -*-
{
    'name': 'KPI+ MRP Shop Floor Tags & Specs',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Etiquetas y especificaciones visuales en tarjetas de Taller',
    'depends': ['mrp', 'mrp_workorder'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'kpi_mrp_shopfloor_tags/static/src/scss/mrp_workorder_tags.scss',
            'kpi_mrp_shopfloor_tags/static/src/xml/mrp_workorder_tags.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}