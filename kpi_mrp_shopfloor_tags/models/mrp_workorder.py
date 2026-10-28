# -*- coding: utf-8 -*-
from odoo import models, fields

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    production_tag_ids = fields.Many2many(
        related='production_id.tag_ids',
        string='Etiquetas MO',
        readonly=True,
    )

    def _get_shopfloor_fields(self):
        """Asegura que el campo viaje en el payload RPC hacia los componentes OWL del Shopfloor."""
        res = super()._get_shopfloor_fields() if hasattr(super(), '_get_shopfloor_fields') else []
        if 'production_tag_ids' not in res:
            res.append('production_tag_ids')
        return res