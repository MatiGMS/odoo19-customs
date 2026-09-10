from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_global_timer_active = fields.Boolean(
        string='Temporizador Activo Global',
        compute='_compute_global_timer_active',
        store=True,
        help='Indica si cualquier usuario tiene un cronómetro activo en esta tarea.'
    )

    @api.depends('timesheet_ids')
    def _compute_global_timer_active(self):
        for task in self:
            timer_count = self.env['timer.timer'].search_count([
                ('res_model', '=', 'project.task'),
                ('res_id', '=', task.id)
            ])
            task.x_global_timer_active = bool(timer_count)

    def action_timer_start(self):
        res = super(ProjectTask, self).action_timer_start()
        self._compute_global_timer_active()
        return res

    def action_timer_stop(self):
        res = super(ProjectTask, self).action_timer_stop()
        self._compute_global_timer_active()
        return res