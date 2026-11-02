# -*- coding: utf-8 -*-
from odoo import models, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_max_stock_warning_data(self):
        """
        Evalúa todas las líneas del pedido.
        Retorna None si todo está OK, o un dict con los datos de alerta si hay incumplimiento.
        """
        self.ensure_one()
        overstocked_products = []
        warehouse = self.picking_type_id.warehouse_id

        for line in self.order_line:
            product = line.product_id
            if not product:
                continue

            max_stock = getattr(product, 'x_studio_stock_maximo', 0.0) or 0.0
            if max_stock <= 0.0:
                continue

            # Evaluar stock en el almacén del pedido
            prod_ctx = product.with_context(warehouse_id=warehouse.id) if warehouse else product
            stock_actual = prod_ctx.qty_available
            proyeccion = stock_actual + line.product_qty

            if proyeccion > max_stock:
                overstocked_products.append({
                    'name': product.display_name,
                    'projected': proyeccion,
                    'max': max_stock,
                })

        if not overstocked_products:
            return None

        total = len(overstocked_products)
        if total > 1:
            title = _("Advertencia: Stock Máximo Superado")
            message = _(
                "¡Revise! Más de 1 producto está incumpliendo el stock máximo permitido en esta compra."
            )
        else:
            item = overstocked_products[0]
            title = _("Stock Máximo Excedido")
            message = _(
                "El producto '%s' supera su stock máximo (A pedir + Stock: %s | Máximo: %s)."
            ) % (item['name'], item['projected'], item['max'])

        return {
            'has_warning': True,
            'count': total,
            'title': title,
            'message': message,
        }

    def _update_order_line_info(self, product_id, quantity, **kwargs):
        """
        Sobrescribe el hook RPC que dispara el catálogo.
        Inyecta el diccionario de validación en la respuesta enviada al frontend.
        """
        res = super()._update_order_line_info(product_id, quantity, **kwargs)
        
        warning_data = self._get_max_stock_warning_data()
        if warning_data and isinstance(res, dict):
            res['stock_warning'] = warning_data
        elif warning_data and not isinstance(res, dict):
            # Si en la versión actual res solo retorna la cantidad entera
            res = {
                'quantity': res,
                'stock_warning': warning_data,
            }
        return res