from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_default_uom_pack(self):
        """
        Asigna como unidad por defecto el primer embalaje configurado en uom_ids 
        de la plantilla del producto.
        """
        for line in self:
            if not line.product_id:
                continue

            tmpl = line.product_id.product_tmpl_id
            # Validar que existan unidades/embalajes adicionales en uom_ids
            if tmpl and tmpl.uom_ids:
                target_uom = tmpl.uom_ids[0]
                
                # Asignación sobre el campo Many2one real
                line.product_uom_id = target_uom