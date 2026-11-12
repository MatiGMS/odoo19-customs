from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    max_qty_warning_msg = fields.Html(
        string='Mensaje de Advertencia', 
        compute='_compute_max_qty_warning_msg'
    )

    @api.depends('order_line.product_id', 'order_line.product_qty', 'picking_type_id')
    def _compute_max_qty_warning_msg(self):
        for order in self:
            exceeded_lines = []
            warehouse_id = order.picking_type_id.warehouse_id.id
            
            for line in order.order_line.filtered(lambda l: l.product_id):
                real_product_id = line.product_id._origin.id or line.product_id.id
                if not real_product_id:
                    continue

                domain = [
                    ('product_id', '=', real_product_id),
                    '|', ('warehouse_id', '=', warehouse_id), ('warehouse_id', '=', False)
                ]
                op = self.env['stock.warehouse.orderpoint'].search(domain, limit=1)
                
                if op and op.product_max_qty > 0 and line.product_qty > op.product_max_qty:
                    exceeded_lines.append(
                        f"<li><b>{line.product_id.display_name}</b>: Ordenó {line.product_qty} (Máximo permitido: {op.product_max_qty})</li>"
                    )

            if exceeded_lines:
                order.max_qty_warning_msg = _(
                    "<p>Las siguientes líneas superan el límite máximo establecido en sus reglas de stock:</p><ul>%s</ul>"
                ) % "".join(exceeded_lines)
            else:
                order.max_qty_warning_msg = False

    def button_confirm(self):
        if self.env.context.get('skip_max_qty_check'):
            return super().button_confirm()

        for order in self:
            if order.max_qty_warning_msg:
                return {
                    'name': _('Alerta de Exceso de Compra'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'purchase.max.qty.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_purchase_id': order.id}
                }
                
        return super().button_confirm()