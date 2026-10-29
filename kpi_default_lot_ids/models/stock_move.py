# -*- coding: utf-8 -*-
from odoo import models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_assign(self, force_qty=False):
        """
        Sobrescribe la reserva automática en v18.
        Conserva la cantidad reservada en la línea detallada pero elimina la
        asignación automática de lotes para exigir ingreso manual.
        """
        res = super()._action_assign(force_qty=force_qty)
        tracked_moves = self.filtered(lambda m: m.has_tracking != 'none')
        
        if tracked_moves:
            # En v18, limpiamos tanto lot_id como lot_name en move_line_ids
            move_lines = tracked_moves.mapped('move_line_ids').filtered(lambda l: l.lot_id or l.lot_name)
            if move_lines:
                move_lines.write({
                    'lot_id': False,
                    'lot_name': False,
                })
        return res