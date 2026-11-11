from src.generators.projects import build_projects
from src.generators.tasks import build_tasks
from src.generators.transactions import build_transactions
from src.generators.timesheets import build_timesheets
from pathlib import Path

N_PROJECTS = 25
DATA_DIR = Path('data/raw_files')

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    projects = build_projects(N_PROJECTS)
    tasks = build_tasks(projects)
    transactions = build_transactions(projects)
    timesheets = build_timesheets(projects)
    projects.to_csv(DATA_DIR / 'projects.csv', index=False)
    tasks.to_csv(DATA_DIR / 'tasks.csv', index=False)
    transactions.to_csv(DATA_DIR / 'transactions.csv', index=False)
    timesheets.to_csv(DATA_DIR / 'timesheets.csv', index=False)
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