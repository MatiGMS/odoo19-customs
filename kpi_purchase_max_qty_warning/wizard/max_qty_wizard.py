from odoo import models, fields

class PurchaseMaxQtyWizard(models.TransientModel):
    _name = 'purchase.max.qty.wizard'
    _description = 'Wizard de Advertencia de Stock Máximo'

    purchase_id = fields.Many2one('purchase.order', string="Orden de Compra", required=True)
    message = fields.Html(related='purchase_id.max_qty_warning_msg', readonly=True)

    def action_confirm_anyway(self):
        """Continúa con la confirmación ignorando la advertencia."""
        self.ensure_one()
        return self.purchase_id.with_context(skip_max_qty_check=True).button_confirm()