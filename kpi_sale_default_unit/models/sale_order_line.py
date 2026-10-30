from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_packaging_v19(self):
        for line in self:
            if not line.product_id:
                continue

            # Verificar de forma segura que el campo exista en el modelo
            packagings = getattr(line.product_id, 'packaging_ids', False)
            if not packagings:
                continue

            sale_packagings = packagings.filtered(lambda p: getattr(p, 'sales', False))
            if sale_packagings:
                default_pack = sale_packagings[0]
                # Asignar empaque y sincronizar cantidades
                if hasattr(line, 'product_packaging_id'):
                    line.product_packaging_id = default_pack.id
                if hasattr(line, 'product_packaging_qty'):
                    line.product_packaging_qty = 1.0
                line.product_uom_qty = default_pack.qty