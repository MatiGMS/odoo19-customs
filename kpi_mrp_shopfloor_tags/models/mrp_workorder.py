# -*- coding: utf-8 -*-
from odoo import models, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.model
    def get_workorders_data(self, domain=None):
        """Sobrescribe el payload RPC que alimenta la pantalla de Taller."""
        res = super().get_workorders_data(domain=domain)
        records = res if isinstance(res, list) else res.get('workorders', [])

        # Prefetching de órdenes para optimizar la consulta en bloque
        wo_ids = [w['id'] for w in records if isinstance(w, dict) and 'id' in w]
        workorders = {wo.id: wo for wo in self.browse(wo_ids)}

        for w_data in records:
            wo = workorders.get(w_data.get('id'))
            if wo and wo.production_id and wo.production_id.tag_ids:
                # Inyectamos el array con id, nombre y color nativo de Odoo (0 a 11)
                w_data['production_tags'] = [
                    {
                        'id': tag.id,
                        'name': tag.name,
                        'color': tag.color or 0,
                    }
                    for tag in wo.production_id.tag_ids
                ]
            else:
                w_data['production_tags'] = []

        return res