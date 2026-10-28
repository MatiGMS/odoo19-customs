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
        """Inyecta los datos directos al diccionario que consume la tarjeta en el frontend."""
        res = super()._get_workorder_data()
        res['production_tags'] = [
            {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color or 0,
            }
            for tag in self.production_id.tag_ids
        ]
        return res

    @api.model
    def get_workorders_data(self, domain=None):
        """Asegura que en la carga masiva inicial las etiquetas viajen en cada registro."""
        res = super().get_workorders_data(domain=domain)
        # res suele ser una lista de dicts o un dict con clave 'workorders'
        records = res if isinstance(res, list) else res.get('workorders', [])
        
        # Mapeo rápido en bloque para no generar N+1 queries
        wo_ids = [w['id'] for w in records if isinstance(w, dict) and 'id' in w]
        workorders = self.browse(wo_ids)
        tags_per_wo = {
            wo.id: [
                {'id': t.id, 'name': t.name, 'color': t.color or 0} 
                for t in wo.production_id.tag_ids
            ]
            for wo in workorders
        }

        for w in records:
            if isinstance(w, dict) and w.get('id') in tags_per_wo:
                w['production_tags'] = tags_per_wo[w['id']]

        return res