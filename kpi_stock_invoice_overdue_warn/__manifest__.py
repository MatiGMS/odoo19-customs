{
    'name': 'KPI+ Picking Sale Overdue Warning',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Muestra alerta de facturas vencidas en entregas vinculadas a ventas',
    'depends': [
        'stock', 
        'sale_stock', 
        'account_invoice_overdue_warn_sale'
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}