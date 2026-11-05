# -*- coding: utf-8 -*-
from odoo import models, fields

class PurchaseStockMaxWarningWizard(models.TransientModel):
    _name = 'purchase.stock.max.warning.wizard'
    _description = 'Advertencia de Stock Maximo en Pedido'

    message = fields.Text(string="Detalle", readonly=True)

    def action_continue(self):
        return {'type': 'ir.actions.act_window_close'}