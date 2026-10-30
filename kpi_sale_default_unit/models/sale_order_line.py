from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_default_uom_pack(self):
        """
        Si el producto tiene embalajes adicionales (uom_ids),
        asigna el primero de ellos como unidad de la línea.
        """
        for line in self:
            if not line.product_id:
                continue

            tmpl = line.product_id.product_tmpl_id
            # Verificar si tiene embalajes/unidades cargados en uom_ids
            if tmpl and tmpl.uom_ids:
                target_uom = tmpl.uom_ids[0]
                
                # Asignar la unidad en la línea de venta
                line.product_uom = target_uom.id
                if hasattr(line, 'product_uom_id'):
                    line.product_uom_id = target_uom.id