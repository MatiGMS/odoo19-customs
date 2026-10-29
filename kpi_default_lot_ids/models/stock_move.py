# -*- coding: utf-8 -*-
from odoo import models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        Hook nativo que construye el diccionario de valores para cada stock.move.line.
        Forzamos que no precargue ningún lot_id ni lot_name, obligando al operario
        a escanear o seleccionar el lote manualmente.
        """
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        
        # Si el producto requiere trazabilidad y no estamos ejecutando tests automáticos
        if self.has_tracking != 'none' and not self.env.registry.test_mode:
            vals['lot_id'] = False
            vals['lot_name'] = False
            
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        """
        Asegura que si se inyectan lotes por defecto en la creación interactiva,
        se limpien antes de confirmar el movimiento.
        """
        for vals in vals_list:
            if 'lot_ids' in vals and not self.env.registry.test_mode:
                vals.pop('lot_ids', None)
        return super().create(vals_list)