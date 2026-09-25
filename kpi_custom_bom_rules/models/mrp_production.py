import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp_production'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(MrpProduction, self).create(vals_list)
        for order in orders:
            order._filter_dynamic_raw_components()
        return orders

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for order in self:
            order._filter_dynamic_raw_components()
        return res

    def _filter_dynamic_raw_components(self):
        self.ensure_one()
        
        # Intentar obtener la sale_line por relación directa o a través de los movimientos de stock
        sale_line = self.sale_line_id
        if not sale_line and self.move_dest_ids:
            sale_line = self.move_dest_ids.mapped('sale_line_id')[:1]
        
        if not sale_line:
            _logger.warning("KPI+ BOM Rule: No se encontró sale_line_id para la MO %s", self.name)
            return

        sale_order = sale_line.order_id
        
        # Normalización estricta del valor del campo
        raw_terminacion = sale_line.x_studio_terminacion or ''
        if isinstance(raw_terminacion, tuple):
            raw_terminacion = raw_terminacion[0]
        terminacion = str(raw_terminacion).strip().upper()

        es_flex = bool(sale_order.x_studio_es_flex)
        es_metalica = bool(getattr(sale_line, 'x_studio_metalica', False))
        qty = sale_line.product_uom_qty

        _logger.info(
            "KPI+ BOM Rule Executing on MO %s | Terminacion: '%s' | Flex: %s | Metalica: %s | Qty: %s",
            self.name, terminacion, es_flex, es_metalica, qty
        )

        FLEX_COMUN_ID = 6364
        FLEX_DOBLE_ID = 6366
        METALICA_ID = 14211

        moves_to_unlink = self.env['stock.move']

        for move in self.move_raw_ids:
            product = move.product_id
            product_id = product.id
            product_name = (product.name or '').upper()

            # REGLA 1: Terminación (BLANCA / NEGRA)
            if terminacion == 'BLANCA':
                if 'NEGRA' in product_name:
                    moves_to_unlink |= move
            elif terminacion == 'NEGRA':
                if 'BLANCA' in product_name:
                    moves_to_unlink |= move
            else:
                if 'BLANCA' in product_name or 'NEGRA' in product_name:
                    moves_to_unlink |= move

            # REGLA 2: Lógica FLEX
            if product_id in (FLEX_COMUN_ID, FLEX_DOBLE_ID):
                if not es_flex:
                    moves_to_unlink |= move
                else:
                    if qty == 1 and product_id == FLEX_DOBLE_ID:
                        moves_to_unlink |= move
                    elif qty == 2 and product_id == FLEX_COMUN_ID:
                        moves_to_unlink |= move

            # REGLA 3: Lógica METÁLICA
            if product_id == METALICA_ID:
                if not es_metalica:
                    moves_to_unlink |= move

        if moves_to_unlink:
            _logger.info("KPI+ BOM Rule: Unlinking %s moves from MO %s", len(moves_to_unlink), self.name)
            moves_to_unlink.action_cancel()
            moves_to_unlink.unlink()