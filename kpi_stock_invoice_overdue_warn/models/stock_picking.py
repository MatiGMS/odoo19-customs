from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Puenteamos los campos usando los nombres exactos del módulo OCA
    sale_overdue_invoice_count = fields.Integer(
        related='sale_id.overdue_invoice_count', 
        string="Cantidad facturas vencidas (Venta)"
    )
    sale_company_currency_id = fields.Many2one(
        related='sale_id.company_currency_id'
    )
    sale_overdue_invoice_amount = fields.Monetary(
        related='sale_id.overdue_invoice_amount',
        currency_field='sale_company_currency_id',
        string="Monto vencido (Venta)"
    )
    sale_commercial_partner_invoicing_id = fields.Many2one(
        related='sale_id.commercial_partner_invoicing_id',
        string="Socio de facturación (Venta)"
    )

    # Puenteamos la acción del botón de la OCA
    def action_jump_to_overdue_invoices_picking(self):
        self.ensure_one()
        if self.sale_id:
            return self.sale_id.jump_to_overdue_invoices()