# -*- coding: utf-8 -*-
from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    # 1. Tu nuevo campo de fecha informativo
    x_fecha_informativa = fields.Date(
        string='Fecha de Gestión',
        help='Campo informativo de fecha editable por el usuario.'
    )

    # 2. Campos relacionados desde el contacto (Asegúrate de usar los nombres correctos de tu DB)
    x_zona_cliente = fields.Char(
        string='Zona del Cliente',
        related='partner_id.x_studio_zona',
        store=True
    )
    x_expreso = fields.Char(
        string='Expreso',
        related='partner_id.x_studio_expreso',
        store=True
    )