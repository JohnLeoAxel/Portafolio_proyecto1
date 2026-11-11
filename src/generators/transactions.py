import random
from datetime import timedelta

import pandas as pd

from src.generators.curves import curva_s

SEED = 42
random.seed(SEED)

COST_DISTRIBUTION = {
    'Labor': 0.45,
    'Materials': 0.30,
    'Subcontracts': 0.20,
    'Other': 0.05
}


def build_transactions(projects):
    filas = []

    for _, proyecto in projects.iterrows():
        project_id = proyecto['project_id']
        presupuesto = proyecto['budget_usd']
        factor = proyecto['overrun_factor']

        costo_final = presupuesto * factor

        for cost_type, porcentaje in COST_DISTRIBUTION.items():
            costo_categoria = costo_final * porcentaje

            filas.append({
                'project_id': project_id,
                'cost_type': cost_type,
                'amount_usd': round(costo_categoria, 2)
})

    return pd.DataFrame(filas)