from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ws_client_name = fields.Char(string="Cliente (Web eCommerce)")
    ws_commission = fields.Char(string="Comisiones (Web)")
    ws_indications = fields.Text(string="Indicaciones (Web)")
    ws_is_new_client = fields.Boolean(string="¿Cliente Nuevo? (Web)")