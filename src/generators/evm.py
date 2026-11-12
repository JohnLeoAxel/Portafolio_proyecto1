import pandas as pd


def calculate_evm(tasks, transactions, project_id, as_of):
    as_of = pd.Timestamp(as_of)

    tareas = tasks[tasks['project_id'] == project_id]
    costos = transactions[
        (transactions['project_id'] == project_id) &
        (transactions['transaction_date'] <= as_of)
    ]

    if tareas.empty:
        raise ValueError(f'No existen tareas para {project_id}')

    bac = tareas['task_budget_usd'].sum()

    pv = (
        tareas['task_budget_usd'] *
        tareas['planned_percent_complete'] / 100
    ).sum()

    ev = (
        tareas['task_budget_usd'] *
        tareas['percent_complete'] / 100
    ).sum()

    ac = costos['amount_usd'].sum()

    sv = ev - pv
    cv = ev - ac

    spi = ev / pv if pv != 0 else None
    cpi = ev / ac if ac != 0 else None

    eac = bac / cpi if cpi else None
    vac = bac - eac if eac is not None else None

    return {
        'project_id': project_id,
        'as_of': as_of,
        'BAC': bac,
        'PV': pv,
        'EV': ev,
        'AC': ac,
        'SV': sv,
        'CV': cv,
        'SPI': spi,
        'CPI': cpi,
        'EAC': eac,
        'VAC': vac
    }