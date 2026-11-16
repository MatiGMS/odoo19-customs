# -*- coding: utf-8 -*-
{
    'name': 'Líneas de Entregas (Vista Plana)',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Añade un menú para visualizar de forma consolidada las líneas de todas las entregas.',
    'description': """
        Este módulo crea una vista de lista (Tree) plana dirigida al modelo stock.move.
        Filtra únicamente los movimientos que pertenecen a una orden de entrega (outgoing).
        Incluye sumatorias al final de las columnas de demanda y cantidad.
    """,
    'author': 'KPI+',
    'depends': ['stock'],
    'data': [
        'views/stock_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}