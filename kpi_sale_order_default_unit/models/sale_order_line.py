from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_default_packaging(self):
        """
        Asigna el primer embalaje de venta disponible para el producto.
        Si el producto no tiene embalajes, conserva el flujo nativo de UdM.
        """
        for line in self:
            if not line.product_id:
                continue

            available_packagings = line.product_id.packaging_ids.filtered(lambda p: p.sales)

            if not available_packagings:
                continue

            default_pack = available_packagings[0]
            line.product_packaging_id = default_pack.id
            line.product_packaging_qty = 1.0
            line.product_uom_qty = default_pack.qty