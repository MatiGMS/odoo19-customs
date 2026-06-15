from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    tag_ids = fields.Many2many(
        related="production_id.tag_ids",
        string="Etiquetas",
        readonly=False,
    )