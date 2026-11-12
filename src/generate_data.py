import argparse
from pathlib import Path

import pandas as pd

from src.generators.projects import build_projects
from src.generators.tasks import build_tasks
from src.generators.transactions import build_transactions
from src.generators.timesheets import build_timesheets

N_PROJECTS = 25
DATA_DIR = Path('data/raw_files')

def parse_date(value):
    try:
        return pd.to_datetime(value, format='%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(
            'La fecha debe tener el formato YYYY-MM-DD'
        )

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generador de datos de proyectos'
    )

    parser.add_argument(
        '--as-of',
        type=parse_date,
        default=pd.Timestamp('2026-11-11'),
        help='Fecha de corte en formato YYYY-MM-DD'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    as_of = args.as_of
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    projects = build_projects(N_PROJECTS)
    tasks = build_tasks(projects, as_of=as_of)
    transactions = build_transactions(projects)
    timesheets = build_timesheets(projects)
    projects.to_csv(DATA_DIR / 'projects.csv', index=False)
    tasks.to_csv(DATA_DIR / 'tasks.csv', index=False)
    transactions.to_csv(DATA_DIR / 'transactions.csv', index=False)
    timesheets.to_csv(DATA_DIR / 'timesheets.csv', index=False)

    print('RESUMEN DE DATOS GENERADOS')
    print(f'Proyectos: {len(projects)}')
    print(f'Tareas: {len(tasks)}')
    print(f'Transacciones: {len(transactions)}')
    print(f'Timesheets: {len(timesheets)}')


if __name__ == '__main__':
    main()