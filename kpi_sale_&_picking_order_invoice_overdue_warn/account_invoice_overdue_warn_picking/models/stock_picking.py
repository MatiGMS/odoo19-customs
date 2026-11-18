from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # 1. Traemos las variables numéricas y relacionales desde la venta.
    # NOTA: Revisa el código del módulo OCA para confirmar el nombre exacto de estos campos.
    # Suelen llamarse así:
    sale_has_overdue = fields.Boolean(related='sale_id.has_overdue_invoices')
    sale_overdue_count = fields.Integer(related='sale_id.overdue_invoice_count') 
    sale_overdue_amount = fields.Monetary(related='sale_id.overdue_amount', currency_field='sale_currency_id')
    sale_partner_invoice_id = fields.Many2one(related='sale_id.partner_invoice_id')
    sale_currency_id = fields.Many2one(related='sale_id.currency_id')

    # 2. Replicamos el botón de la imagen para que funcione desde la entrega
    def action_view_overdue_invoices_from_picking(self):
        self.ensure_one()
        if self.sale_id:
            # Llama a la misma función que usa el módulo OCA en la venta
            return self.sale_id.action_view_overdue_invoices()