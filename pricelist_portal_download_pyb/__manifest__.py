# -*- coding: utf-8 -*-
{
    'name': "Product Pricelist Portal Download",

    'summary': """Download Pricelist in PDF or Excel format from Customer Portal""",

    'description': """
    This module allows customers to download personalized pricelists from the portal in PDF or Excel format.
    Features include multi-category selection, stock availability filtering, grouped display, and customer-specific
    stock visibility controls. Perfect for B2B businesses, wholesalers, and distributors.
    """,

    'author': 'PyBeans',
    'category': 'Website/Website',
    'version': '1.0.0',
    'website': 'https://www.pybeans.com/',
    'license': 'LGPL-3',
    'support': 'devpybeans@gmail.com',

    'depends': ['website_sale_stock', 'sale_management'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
        'reports/product_pricelist_report_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'pricelist_portal_download_pyb/static/lib/select2.min.css',
            'pricelist_portal_download_pyb/static/lib/select2.min.js',
            'pricelist_portal_download_pyb/static/lib/jquery.blockUI.js',
            'pricelist_portal_download_pyb/static/src/js/pricelist_download.js',
        ],
    },

    'images': [
        'static/description/pricelist_download_form.png',
    ],

    'application': True,
    'price': 50.00,
    'currency': 'EUR',
    'live_test_url': "https://www.pybeans.com/book-service",
}
