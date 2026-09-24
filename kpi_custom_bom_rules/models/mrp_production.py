from odoo import models, api

class MrpProduction(models.Model):
    _inherit = 'mrp_production'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(MrpProduction, self).create(vals_list)
        for order in orders:
            order._filter_dynamic_raw_components()
        return orders

    def _filter_dynamic_raw_components(self):
        self.ensure_one()
        
        sale_line = self.sale_line_id or self.move_dest_ids.sale_line_id[:1]
        if not sale_line:
            return

        sale_order = sale_line.order_id
        
        terminacion = (sale_line.x_studio_terminacion or '').strip().upper()
        es_flex = sale_order.x_studio_es_flex
        es_metalica = getattr(sale_line, 'x_studio_metalica', False)
        qty = sale_line.product_uom_qty

        FLEX_COMUN_ID = 6364
        FLEX_DOBLE_ID = 6366
        METALICA_ID = 14211

        moves_to_unlink = self.env['stock.move']

        for move in self.move_raw_ids:
            product = move.product_id
            product_id = product.id
            product_name = (product.name or '').upper()

            if terminacion == 'BLANCA':
                if 'NEGRA' in product_name:
                    moves_to_unlink |= move
            elif terminacion == 'NEGRA':
                if 'BLANCA' in product_name:
                    moves_to_unlink |= move
            else:
                if 'BLANCA' in product_name or 'NEGRA' in product_name:
                    moves_to_unlink |= move

            if product_id in (FLEX_COMUN_ID, FLEX_DOBLE_ID):
                if not es_flex:
                    moves_to_unlink |= move
                else:
                    if qty == 1 and product_id == FLEX_DOBLE_ID:
                        moves_to_unlink |= move
                    elif qty == 2 and product_id == FLEX_COMUN_ID:
                        moves_to_unlink |= move

            if product_id == METALICA_ID:
                if not es_metalica:
                    moves_to_unlink |= move

        if moves_to_unlink:
            moves_to_unlink.action_cancel()
            moves_to_unlink.unlink()