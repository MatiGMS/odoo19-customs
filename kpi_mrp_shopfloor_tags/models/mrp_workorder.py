# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    production_tag_ids = fields.Many2many(
        related='production_id.tag_ids',
        string='Etiquetas MO',
        readonly=True,
    )

    def _get_workorder_data(self):
        """Sobrescribe el payload individual de cada orden de trabajo para Shop Floor."""
        data = super()._get_workorder_data()
        # Empaquetamos id, nombre y color_index de cada tag de la orden padre
        data['production_tags'] = [
            {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color or 0,
            }
            for tag in self.production_id.tag_ids
        ]
        return data

    @api.model
    def get_workorders_data(self, domain=None):
        """Asegura la compatibilidad si tu versión serializa directamente en bloque."""
        res = super().get_workorders_data(domain=domain)
        # Si el core utiliza un mapeo directo de workorders en res['workorders']:
        if isinstance(res, dict) and 'workorders' in res:
            workorders_by_id = {wo.id: wo for wo in self.browse([w['id'] for w in res['workorders'] if 'id' in w])}
            for w_data in res['workorders']:
                wo = workorders_by_id.get(w_data.get('id'))
                if wo:
                    w_data['production_tags'] = [
                        {
                            'id': tag.id,
                            'name': tag.name,
                            'color': tag.color or 0,
                        }
                        for tag in wo.production_id.tag_ids
                    ]
        return res