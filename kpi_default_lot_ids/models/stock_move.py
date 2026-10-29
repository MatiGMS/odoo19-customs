# -*- coding: utf-8 -*-
from odoo import models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_assign(self, force_qty=False):
        """
        Ejecuta la reserva estándar de stock del core y limpia los lotes
        asignados automáticamente, forzando la selección manual por parte del operador.
        """
        res = super()._action_assign(force_qty=force_qty)
        # Filtrar solo movimientos tracked para optimizar operaciones masivas
        tracked_moves = self.filtered(lambda m: m.has_tracking != 'none')
        if tracked_moves:
            # Vacia lot_id en stock.move.line respetando la cantidad reservada
            tracked_moves.move_line_ids.filtered(lambda l: l.lot_id).write({'lot_id': False})
        return res