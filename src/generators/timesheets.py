import random
from datetime import timedelta

import pandas as pd

RESOURCES = [
    'R001',
    'R002',
    'R003',
    'R004',
    'R005',
    'R006',
    'R007',
    'R008',
    'R009',
    'R010'
]


def build_timesheets(projects):
    filas = []

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        inicio = proyecto['start_date']
        fin = proyecto['end_date']

        for fecha in pd.date_range(inicio, fin, freq='B'):
            recursos_dia = random.sample(
                RESOURCES,
                k=random.randint(2, 5)
            )

            for resource_id in recursos_dia:
                horas = random.choice([4, 5, 6, 7, 8])

                filas.append({
                    'project_id': project_id,
                    'resource_id': resource_id,
                    'work_date': fecha,
                    'hours': horas
                })

    return pd.DataFrame(filas)