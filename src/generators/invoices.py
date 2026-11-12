import random
from datetime import timedelta

import pandas as pd

SEED = 42

MILESTONES = [
    ('Design', 0.20),
    ('Engineering', 0.30),
    ('Construction', 0.30),
    ('Delivery', 0.20),
]


def build_fixed_price_invoices(projects):
    rng = random.Random(SEED)

    filas = []

    proyectos = projects[
        projects['billing_type'] == 'Fixed Price'
    ]

    for _, proyecto in proyectos.iterrows():
        contract_multiplier = rng.uniform(1.10, 1.25)

        contract_value = round(
            proyecto['budget_usd'] * contract_multiplier, 2
        )

        duration_days = (
            proyecto['end_date'] - proyecto['start_date']
        ).days

        for i, (milestone, percentage) in enumerate(MILESTONES):
            invoice_date = proyecto['start_date'] + timedelta(
                days=int(duration_days * (i + 1) / 4)
            )

            amount = round(contract_value * percentage, 2)

            filas.append({
                'project_id': proyecto['project_id'],
                'billing_type': 'Fixed Price',
                'invoice_date': invoice_date,
                'invoice_description': milestone,
                'amount_usd': amount,
            })

    return pd.DataFrame(filas)

def build_tm_invoices(timesheets):
    datos = timesheets.copy()

    datos['work_date'] = pd.to_datetime(datos['work_date'])

    datos['period_start'] = (
        datos['work_date']
        .dt.to_period('M')
        .dt.to_timestamp()
    )

    facturas = (
        datos.groupby(['project_id', 'period_start'], as_index=False)
        .agg(
            period_end=('work_date', 'max'),
            amount_usd=('labor_cost_usd', 'sum'),
            total_hours=('hours', 'sum'),
        )
    )

    facturas['billing_type'] = 'T&M'

    facturas['invoice_date'] = (
        facturas['period_start'] + pd.offsets.MonthEnd(1)
    )

    facturas['invoice_description'] = (
        'Monthly billing - '
        + facturas['period_start'].dt.strftime('%Y-%m')
    )

    return facturas

def build_invoices(projects, timesheets):
    fixed_price = build_fixed_price_invoices(projects)
    tm = build_tm_invoices(timesheets)

    facturas = pd.concat(
        [fixed_price, tm],
        ignore_index=True
    )

    columnas = [
        'project_id',
        'billing_type',
        'invoice_date',
        'period_start',
        'period_end',
        'invoice_description',
        'total_hours',
        'amount_usd',
    ]

    return facturas[columnas]