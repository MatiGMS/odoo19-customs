from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_pricelist_id = fields.Many2one(
        related='move_id.sale_pricelist_id',
        string='Tarifa de Venta',
        store=True,
        readonly=True,
        help='Lista de precios de la orden de venta origen.'
    )