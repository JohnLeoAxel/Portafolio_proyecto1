import random

import pandas as pd

SEED = 42


RESOURCES = {
    'R001': {'role': 'Project Manager', 'hourly_rate_usd': 85},
    'R002': {'role': 'Project Engineer', 'hourly_rate_usd': 65},
    'R003': {'role': 'Project Engineer', 'hourly_rate_usd': 65},
    'R004': {'role': 'Cost Analyst', 'hourly_rate_usd': 55},
    'R005': {'role': 'Cost Analyst', 'hourly_rate_usd': 55},
    'R006': {'role': 'Field Engineer', 'hourly_rate_usd': 60},
    'R007': {'role': 'Field Engineer', 'hourly_rate_usd': 60},
    'R008': {'role': 'Technician', 'hourly_rate_usd': 35},
    'R009': {'role': 'Technician', 'hourly_rate_usd': 35},
    'R010': {'role': 'Technician', 'hourly_rate_usd': 35}
}


def build_timesheets(projects):

    rng = random.Random(SEED)
    filas = []

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        inicio = proyecto['start_date']
        fin = proyecto['end_date']

        for fecha in pd.date_range(inicio, fin, freq='B'):
            recursos_dia = rng.sample(
                list(RESOURCES.keys()),
                k=rng.randint(2, 5)
)

            for resource_id in recursos_dia:
                horas = rng.choice([4, 5, 6, 7, 8])
                role = RESOURCES[resource_id]['role']
                hourly_rate = RESOURCES[resource_id]['hourly_rate_usd']
                week_start = fecha - pd.Timedelta(days=fecha.weekday())

                filas.append({
                    'project_id': project_id,
                    'resource_id': resource_id,
                    'role': role,
                    'work_date': fecha,
                    'week_start': week_start,
                    'hours': horas,
                    'hourly_rate_usd': hourly_rate,
                    'labor_cost_usd': round(horas * hourly_rate, 2)
                })

    return pd.DataFrame(filas)