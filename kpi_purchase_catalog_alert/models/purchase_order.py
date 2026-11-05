# -*- coding: utf-8 -*-
from odoo import models, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _check_max_stock_and_notify(self):
        """Revisa si hay líneas con cantidad superior a x_studio_stock_maximo y notifica."""
        for order in self:
            if order.state not in ('draft', 'sent'):
                continue

            overstock_items = []
            for line in order.order_line:
                product = line.product_id
                if not product:
                    continue

                stock_max = getattr(product, 'x_studio_stock_maximo', 0.0) or 0.0
                if stock_max > 0.0 and line.product_qty > stock_max:
                    overstock_items.append({
                        'name': product.display_name,
                        'qty': line.product_qty,
                        'max': stock_max,
                    })

            if overstock_items:
                if len(overstock_items) > 1:
                    title = _("Alerta de Stock Máximo")
                    msg = _("¡Atención! Revise el pedido: más de 1 producto está superando el stock máximo permitido.\n\n")
                    for item in overstock_items:
                        msg += _("• %s: Pidiendo %s | Máximo: %s\n") % (item['name'], item['qty'], item['max'])
                else:
                    item = overstock_items[0]
                    title = _("Stock Máximo Superado")
                    msg = _("¡Atención! El producto '%s' supera el stock máximo (Pidiendo: %s | Máximo: %s).") % (
                        item['name'], item['qty'], item['max']
                    )

                # Envío directo al bus websocket del usuario en sesión
                self.env['bus.bus']._sendone(
                    self.env.user.partner_id,
                    'simple_notification',
                    {
                        'title': title,
                        'message': msg,
                        'type': 'warning',
                        'sticky': True,  # Fijo en pantalla para obligar a leer
                    }
                )

    def read(self, fields=None, load='_classic_read'):
        """Se ejecuta SIEMPRE que Odoo vuelve del catálogo y pinta el formulario."""
        res = super().read(fields=fields, load=load)
        # Solo verificar cuando estamos consultando los productos de la orden
        if not fields or 'order_line' in fields:
            self._check_max_stock_and_notify()
        return res