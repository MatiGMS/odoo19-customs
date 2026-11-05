from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Campo requerido por sale_order_views.xml
    packaging_uom_display = fields.Char(
        string='Unidad',
        compute='_compute_packaging_uom_display',
        store=False,
    )

    @api.depends('product_uom_id')
    def _compute_packaging_uom_display(self):
        for line in self:
            line.packaging_uom_display = line.product_uom_id.name if line.product_uom_id else ''

    @api.onchange('product_id')
    def _onchange_product_id_set_default_uom_pack(self):
        """Asigna por defecto el primer embalaje al crear líneas manualmente en backend."""
        for line in self:
            if not line.product_id:
                continue

            tmpl = line.product_id.product_tmpl_id
            if tmpl and tmpl.uom_ids:
                line.product_uom_id = tmpl.uom_ids[0]

    @api.model_create_multi
    def create(self, vals_list):
        """Garantiza la asignación del embalaje en pedidos creados desde eCommerce o API."""
        for vals in vals_list:
            if 'product_uom_id' not in vals and vals.get('product_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product.product_tmpl_id.uom_ids:
                    vals['product_uom_id'] = product.product_tmpl_id.uom_ids[0].id
        return super().create(vals_list)