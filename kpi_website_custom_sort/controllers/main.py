# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSaleCustomSort(WebsiteSale):

    def _get_product_sort_mapping(self):
        """
        Extiende el dropdown visible de ordenación en el frontend.
        Formato nativo: { 'clave_url': ('order_sql', 'Etiqueta') }
        """
        mapping = super()._get_product_sort_mapping()

        # 1. Modificar 'Destacado' para que siempre priorice favoritos (estrella)
        if 'website_sequence' in mapping:
            label = mapping['website_sequence'][1] if isinstance(mapping['website_sequence'], tuple) else 'Destacado'
            mapping['website_sequence'] = ('priority desc, website_sequence asc, id desc', label)

        # 2. Agregar 'Más vendido' al dropdown
        mapping['bestseller'] = (
            'sales_count_stored desc, website_sequence asc, id desc',
            'Más vendido'
        )
        return mapping

    def _get_shop_order(self, post):
        """
        Traduce la clave de orden a SQL.
        Si no se pasa parámetro 'order' en la URL, se aplica 'bestseller' por defecto.
        """
        order_key = post.get('order')

        # CASO 1: El usuario seleccionó explícitamente una opción
        if order_key == 'bestseller':
            return 'sales_count_stored desc, website_sequence asc, id desc'
        if order_key == 'website_sequence':
            return 'priority desc, website_sequence asc, id desc'
        
        # CASO 2: Navegación inicial a /shop (sin parámetro order) -> Default: Más Vendidos
        if not order_key:
            return 'sales_count_stored desc, website_sequence asc, id desc'

        # Para el resto (precio ascendente, descendente, nombre), respeta el método nativo
        return super()._get_shop_order(post)

    def _shop_lookup_products(self, *args, **kwargs):
        """
        Blindaje para la búsqueda predictiva o paginación.
        Asegura que el alias nunca llegue crudo al ORM.
        """
        # Intercepción si options viene como kwarg
        if 'options' in kwargs:
            order_val = kwargs['options'].get('order')
            if not order_val or order_val == 'bestseller':
                kwargs['options']['order'] = 'sales_count_stored desc, website_sequence asc, id desc'
            elif order_val == 'website_sequence':
                kwargs['options']['order'] = 'priority desc, website_sequence asc, id desc'

        # Intercepción si options viene como argumento posicional (args[1])
        elif len(args) >= 2 and isinstance(args[1], dict):
            order_val = args[1].get('order')
            if not order_val or order_val == 'bestseller':
                args[1]['order'] = 'sales_count_stored desc, website_sequence asc, id desc'
            elif order_val == 'website_sequence':
                args[1]['order'] = 'priority desc, website_sequence asc, id desc'

        return super()._shop_lookup_products(*args, **kwargs)