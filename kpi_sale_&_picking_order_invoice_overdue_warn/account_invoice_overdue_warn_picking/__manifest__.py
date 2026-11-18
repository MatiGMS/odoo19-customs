{
    'name': 'Alertas en Entregas',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Muestra las alertas de crédito de la OCA en los albaranes.',
    'depends': [
        'stock', 
        'account_invoice_overdue_warn_sale' # O el nombre exacto del módulo OCA que estés usando
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}