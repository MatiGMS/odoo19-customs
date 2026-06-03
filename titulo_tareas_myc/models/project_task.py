# -*- coding: utf-8 -*-

from odoo import api, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id') or self.env.context.get('default_partner_id')
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            nombre_fantasia = getattr(partner, 'x_studio_nombre_fantasa', False)
            if nombre_fantasia:
                vals['name'] = nombre_fantasia
        return super().create(vals)