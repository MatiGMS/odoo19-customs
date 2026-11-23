{
    'name': 'KPI+ Website Cart Salesperson Info',
    'version': '1.0',
    'category': 'Website/Website',
    'summary': 'Agrega campos comerciales (Cliente, Comisiones, etc.) en el carrito de compras',
    'description': """
        Módulo desarrollado por KPI+ para extender el checkout de Odoo.
        Permite a los vendedores cargar datos comerciales en el carrito mediante AJAX,
        reflejándolos automáticamente en la orden de venta (backend).
    """,
    'author': 'KPI+',
    'website': 'https://kpiplus.com',
    'depends': [
        'sale_management', 
        'website_sale'
    ],
    'data': [
        # 'views/sale_order_views.xml', 
        'views/website_sale_templates.xml',
    ],
    'assets': {
        # web.assets_frontend es el bundle correcto para inyectar JS/CSS en la web pública
        'web.assets_frontend': [
            'kpi_website_cart_note/static/src/js/cart_salesperson_info.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}