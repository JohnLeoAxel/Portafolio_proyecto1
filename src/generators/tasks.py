
import pandas as pd


TASK_TEMPLATES = {
    'Solar': [
        'Engineering',
        'Procurement',
        'Construction',
        'Commissioning'
    ],
    'Eólico': [
        'Engineering',
        'Procurement',
        'Installation',
        'Commissioning'
    ],
    'Data Center': [
        'Design',
        'Procurement',
        'Construction',
        'Testing'
    ]
}

def build_tasks(projects):
    filas = []

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        project_type = proyecto['project_type']
        tareas = TASK_TEMPLATES[project_type]

        for i, task_name in enumerate(tareas, start=1):
            filas.append({
                'project_id': project_id,
                'task_id': f'{project_id}-T{i:02d}',
                'task_name': task_name
            })

    return pd.DataFrame(filas)