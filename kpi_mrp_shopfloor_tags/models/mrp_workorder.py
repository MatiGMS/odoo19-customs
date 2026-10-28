# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import html_escape

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    production_tag_ids = fields.Many2many(
        related='production_id.tag_ids',
        string='Etiquetas de Producción',
        readonly=True,
    )

    tag_badges_html = fields.Html(
        string='Etiquetas HTML',
        compute='_compute_tag_badges_html',
        sanitize=False,
    )

    @api.depends('production_id.tag_ids')
    def _compute_tag_badges_html(self):
        # Mapeo de paleta estándar de tags de Odoo (0 a 11)
        palette = {
            0: ('#6c757d', '#ffffff'),
            1: ('#dc3545', '#ffffff'), # Rojo
            2: ('#fd7e14', '#ffffff'), # Naranja
            3: ('#ffc107', '#000000'), # Amarillo
            4: ('#0dcaf0', '#000000'), # Celeste
            5: ('#6f42c1', '#ffffff'), # Púrpura (como Flex)
            6: ('#d63384', '#ffffff'), # Rosa
            7: ('#198754', '#ffffff'), # Verde
            8: ('#20c997', '#ffffff'), # Teal
            9: ('#0d6efd', '#ffffff'), # Azul
            10: ('#6610f2', '#ffffff'),
            11: ('#795548', '#ffffff'),
        }

        for wo in self:
            badges = []
            for tag in wo.production_id.tag_ids:
                color_idx = tag.color or 0
                bg_color, text_color = palette.get(color_idx, ('#6c757d', '#ffffff'))
                badges.append(
                    f'<span class="badge rounded-pill me-1" style="background-color: {bg_color} !important; color: {text_color} !important; font-size: 0.75rem; padding: 0.25rem 0.55rem; border: 1px solid rgba(255,255,255,0.2);">'
                    f'<i class="fa fa-tag me-1"></i>{html_escape(tag.name)}</span>'
                )
            
            first_color = palette.get(wo.production_id.tag_ids[:1].color or 0, ('transparent', ''))[0] if wo.production_id.tag_ids else 'transparent'
            
            wo.tag_badges_html = f"""
                <div class="o_shopfloor_custom_tags mb-2 d-flex flex-wrap align-items-center" data-border-color="{first_color}">
                    {''.join(badges)}
                </div>
            """ if badges else ""

    # Inyección en el serializador JSON que consume el Shop Floor
    def _get_workorder_data(self):
        data = super()._get_workorder_data()
        data['tag_badges_html'] = self.tag_badges_html or ""
        return data

    @api.model
    def get_workorders_data(self, domain=None):
        res = super().get_workorders_data(domain=domain)
        records = res if isinstance(res, list) else res.get('workorders', [])
        
        wo_ids = [w['id'] for w in records if isinstance(w, dict) and 'id' in w]
        workorders = {wo.id: wo for wo in self.browse(wo_ids)}

        for w in records:
            wo = workorders.get(w.get('id'))
            if wo:
                w['tag_badges_html'] = wo.tag_badges_html or ""
        return res