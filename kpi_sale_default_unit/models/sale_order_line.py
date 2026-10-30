from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id')
    def _compute_product_packaging_id(self):
        super()._compute_product_packaging_id()
        for line in self:
            if not line.product_id:
                continue

            # Buscar embalajes habilitados específicamente para ventas
            sale_packagings = line.product_id.packaging_ids.filtered(lambda p: p.sales)
            if sale_packagings and not line.product_packaging_id:
                default_pack = sale_packagings[0]
                line.product_packaging_id = default_pack
                line.product_packaging_qty = 1.0
                line.product_uom_qty = default_pack.qty

    @api.onchange('product_id')
    def _onchange_product_id_set_packaging_v19(self):
        """
        Garantiza que en el cliente web el cambio de producto dispare
        la asignación inmediata de empaque y cantidad de venta.
        """
        for line in self:
            if not line.product_id:
                continue

            sale_packagings = line.product_id.packaging_ids.filtered(lambda p: p.sales)
            if sale_packagings:
                default_pack = sale_packagings[0]
                line.product_packaging_id = default_pack
                line.product_packaging_qty = 1.0
                line.product_uom_qty = default_pack.qty