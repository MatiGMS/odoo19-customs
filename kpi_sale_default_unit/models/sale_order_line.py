from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_default_packaging_unit(self):
        for line in self:
            if not line.product_id:
                continue

            # Buscar embalajes primero en la variante, luego en la plantilla
            packagings = getattr(line.product_id, 'packaging_ids', False)
            if not packagings and hasattr(line.product_id, 'product_tmpl_id'):
                packagings = getattr(line.product_id.product_tmpl_id, 'packaging_ids', False)

            if not packagings:
                continue

            # Filtrar por embalajes habilitados para ventas (campo booleano 'sales')
            sale_packagings = packagings.filtered(lambda p: getattr(p, 'sales', True))
            if not sale_packagings:
                continue

            default_pack = sale_packagings[0]

            # 1. Asignar el embalaje nativo si existe el campo en sale.order.line
            if hasattr(line, 'product_packaging_id'):
                line.product_packaging_id = default_pack.id
            if hasattr(line, 'product_packaging_qty'):
                line.product_packaging_qty = 1.0

            # 2. Asignar la cantidad base de la unidad
            if default_pack.qty:
                line.product_uom_qty = default_pack.qty

            # 3. Forzar la unidad de medida si el empaque tiene una UoM asociada
            if hasattr(default_pack, 'product_uom_id') and default_pack.product_uom_id:
                line.product_uom_id = default_pack.product_uom_id.id
            elif hasattr(line, 'product_uom') and hasattr(default_pack, 'uom_id') and default_pack.uom_id:
                line.product_uom = default_pack.uom_id.id