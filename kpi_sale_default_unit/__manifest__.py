{
    'name': 'KPI+ Sale Default Unit / Packaging',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Asigna por defecto la unidad/embalaje en líneas de venta',
    'author': 'KPI+',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
        'stock',       # Define packaging_ids en product.product y product.template
        'sale_stock',  # Vincula packaging con las líneas de venta (sale.order.line)
    ],
    'data': [
        # Tus vistas si corresponden
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}