from odoo import models, fields, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    production_tag_ids = fields.Many2many(
        related='production_id.tag_ids',
        string='Etiquetas de Producción',
        readonly=True,
    )

    # Si usas Odoo Shopfloor nativo, en v17/v18/v19 se cargan campos mediante búsqueda directa
    # o vía get_workorder_data. Exponemos una función serializadora:
    def _get_workorder_shopfloor_tags(self):
        self.ensure_one()
        return [
            {
                'id': tag.id,
                'name': tag.name,
                'color_index': tag.color or 0,
            }
            for tag in self.production_tag_ids
        ]