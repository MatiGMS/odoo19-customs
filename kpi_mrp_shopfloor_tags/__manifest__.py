{
    'name': 'KPI+ MRP Shop Floor Tags & Visual Styling',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Muestra etiquetas de mrp.production en las tarjetas del Shop Floor con estilo y acentos de color.',
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