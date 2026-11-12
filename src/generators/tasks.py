
import random

import pandas as pd

SEED = 42
AS_OF_DATE = pd.Timestamp('2026-11-11')

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

BUDGET_WEIGHTS = [0.15, 0.25, 0.45, 0.15]


def calculate_progress(start, end, as_of):
    if as_of < start:
        return 0.0

    if as_of >= end:
        return 100.0

    elapsed = (as_of - start).days
    duration = (end - start).days + 1

    return round(elapsed / duration * 100, 2)


def build_tasks(projects, as_of=AS_OF_DATE):
    filas = []
    rng = random.Random(SEED)

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        project_type = proyecto['project_type']
        project_start = pd.Timestamp(proyecto['start_date'])
        project_end = pd.Timestamp(proyecto['end_date'])
        project_budget = proyecto['budget_usd']

        tareas = TASK_TEMPLATES[project_type]

        total_days = (project_end - project_start).days + 1

        for i, task_name in enumerate(tareas):
            task_start = project_start + pd.Timedelta(
                days=round(i * total_days / 4)
            )

            task_end = project_start + pd.Timedelta(
                days=round((i + 1) * total_days / 4) - 1
            )

            planned = calculate_progress(
                task_start,
                task_end,
                as_of
            )

            progress_factor = rng.uniform(0.85, 1.10)
            actual = min(100.0, round(planned * progress_factor, 2))

            filas.append({
                'project_id': project_id,
                'task_id': f'{project_id}-T{i + 1:02d}',
                'task_name': task_name,
                'planned_start_date': task_start,
                'planned_end_date': task_end,
                'budget_weight': BUDGET_WEIGHTS[i],
                'task_budget_usd': round(
                    project_budget * BUDGET_WEIGHTS[i], 2
                ),
                'planned_percent_complete': planned,
                'percent_complete': actual
            })

    return pd.DataFrame(filas)
