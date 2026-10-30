# -*- coding: utf-8 -*-
from odoo import models, fields

class Website(models.Model):
    _inherit = 'website'

    # Amplía el selection nativo para admitir la clave 'bestseller'
    shop_default_sort = fields.Selection(
        selection_add=[('bestseller', 'Más vendido')],
        ondelete={'bestseller': 'set default'}
    )