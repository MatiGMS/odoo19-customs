# -*- coding: utf-8 -*-
from odoo import models, fields

class PurchaseStockMaxWarningWizard(models.TransientModel):
    _name = 'purchase.stock.max.warning.wizard'
    _description = 'Advertencia de Stock Máximo en Pedido'

    message = fields.Text(string="Mensaje de Alerta", readonly=True)

    def action_close(self):
        """Cierra el wizard modal y deja al usuario en el formulario."""
        return {'type': 'ir.actions.act_window_close'}