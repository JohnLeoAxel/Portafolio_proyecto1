
import random

import pandas as pd

from src.generators.curves import curva_s

SEED = 42

EXCHANGE_RATE = 18.00

COST_DISTRIBUTION = {
    'Labor': 0.45,
    'Materials': 0.30,
    'Subcontracts': 0.20,
    'Other': 0.05
}


def build_transactions(projects):
    rng = random.Random(SEED)
    filas = []

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        presupuesto = proyecto['budget_usd']
        factor = proyecto['overrun_factor']

        costo_final = presupuesto * factor

        fechas = pd.date_range(
            start=proyecto['start_date'],
            end=proyecto['end_date'],
            freq='D'
        )

        curva = curva_s(len(fechas))

        for cost_type, porcentaje in COST_DISTRIBUTION.items():
            costo_categoria = round(costo_final * porcentaje, 2)

            importes_diarios = [
                round(costo_categoria * fraccion, 2)
                for fraccion in curva
            ]

            # Ajustar el residuo de redondeo en el último día
            importes_diarios[-1] += round(
                costo_categoria - sum(importes_diarios), 2
            )

            for fecha, importe in zip(fechas, importes_diarios):
                currency = rng.choices(
                    ['USD', 'MXN'],
                    weights=[70, 30],
                    k=1
                )[0]

                amount_original = (
                    importe if currency == 'USD'
                    else round(importe * EXCHANGE_RATE, 2)
                )

                filas.append({
                    'project_id': project_id,
                    'transaction_date': fecha,
                    'cost_type': cost_type,
                    'currency': currency,
                    'amount_original': amount_original,
                    'exchange_rate_mxn_per_usd': EXCHANGE_RATE,
                    'amount_usd': importe
                })

    return pd.DataFrame(filas)
