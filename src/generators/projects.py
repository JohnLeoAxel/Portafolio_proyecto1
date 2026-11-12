import random
from datetime import date, timedelta

import pandas as pd
from faker import Faker

SEED = 42



def build_projects(n=25):
    rng = random.Random(SEED)

    fake = Faker('es_MX')
    fake.seed_instance(SEED)

    filas = []

    for i in range(1, n + 1):
        tipo = rng.choice(['Solar', 'Eólico', 'Data Center'])

        inicio = date(2025, 1, 1) + timedelta(
            days=rng.randint(0, 240)
        )

        duracion = rng.randint(300, 720)

        filas.append({
            'project_id': f'P{i:03d}',
            'project_name': f'{tipo} {fake.city()}',
            'project_type': tipo,
            'billing_type': rng.choice(['Fixed Price', 'T&M']),
            'budget_usd': round(rng.uniform(2e6, 40e6), 2),
            'start_date': inicio,
            'end_date': inicio + timedelta(days=duracion),
            'overrun_factor': rng.choice([0.9, 0.97, 1.0, 1.05, 1.15, 1.3]),
        })

    df = pd.DataFrame(filas)

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    return df