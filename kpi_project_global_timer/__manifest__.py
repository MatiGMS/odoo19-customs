{
    'name': 'KPI+ Global Task Timer Indicator',
    'version': '18.0.1.0.0',
    'category': 'Services/Project',
    'summary': 'Muestra un indicador en el Kanban cuando cualquier usuario inicia un temporizador.',
    'author': 'KPI+',
    'depends': ['project', 'hr_timesheet', 'industry_fsm', 'timer'],
    'data': [
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}