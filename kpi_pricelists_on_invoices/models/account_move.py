from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Tarifa de Venta',
        compute='_compute_sale_pricelist_id',
        store=True,
        help='Lista de precios de la orden de venta que originó esta factura.'
    )

    @api.depends('invoice_line_ids.sale_line_ids.order_id.pricelist_id')
    def _compute_sale_pricelist_id(self):
        for move in self:
            # Obtiene las SO vinculadas a través de las líneas de la factura
            sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
            if sale_orders:
                # Asigna la tarifa de la primera orden encontrada
                move.sale_pricelist_id = sale_orders[0].pricelist_id
            else:
                move.sale_pricelist_id = False