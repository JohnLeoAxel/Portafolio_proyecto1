
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data/raw_files')

KEYS = {
    'projects.csv': ['project_id'],
    'tasks.csv': ['task_id'],
    'transactions.csv': ['project_id', 'transaction_date', 'cost_type'],
    'timesheets.csv': ['project_id', 'resource_id', 'work_date']
}


def check_duplicates(df, columns):
    return df.duplicated(subset=columns).sum()


def check_project_references(df, projects):
    return (~df['project_id'].isin(projects['project_id'])).sum()


def check_negative_amounts(df, column):
    return (df[column] < 0).sum()


def check_hours_out_of_range(df):
    return ((df['hours'] < 4) | (df['hours'] > 8)).sum()

def check_labor_costs(df):
    expected = (
        df['hours'] * df['hourly_rate_usd']
    ).round(2)

    return (
        (df['labor_cost_usd'] - expected).abs() > 0.01
    ).sum()

def check_weekly_hours(df):
    weekly = (
        df.groupby(
            ['project_id', 'resource_id', 'week_start']
        )['hours']
        .sum()
    )

    return (weekly > 40).sum()

def check_week_start(df):
    expected = (
        pd.to_datetime(df['work_date'])
        - pd.to_timedelta(
            pd.to_datetime(df['work_date']).dt.day_of_week,
            unit='D'
        )
    ).dt.normalize()

    actual = pd.to_datetime(df['week_start'])

    return (actual != expected).sum()


def check_cost_reconciliation(projects, transactions):
    # 1. Calcular el costo esperado por proyecto
    expected = (
        projects.set_index('project_id')['budget_usd']
        * projects.set_index('project_id')['overrun_factor']
    )

    # 2. Calcular el costo registrado por proyecto
    actual = transactions.groupby('project_id')['amount_usd'].sum()

    # 3. Comparar ambas tablas
    comparison = pd.concat(
        [expected.rename('expected'), actual.rename('actual')],
        axis=1
    )

    # 4. Calcular las diferencias
    comparison['difference'] = (
        comparison['expected'] - comparison['actual']
    ).abs()

    # 5. Clasificar las anomalías
    comparison['status'] = 'OK'

    missing = comparison['actual'].isna()
    unexpected = comparison['expected'].isna()

    mismatches = (
        comparison['expected'].notna()
        & comparison['actual'].notna()
        & (comparison['difference'] > 0.02)
    )

    comparison.loc[missing, 'status'] = 'SIN_TRANSACCIONES'
    comparison.loc[unexpected, 'status'] = 'PROYECTO_INEXISTENTE'
    comparison.loc[mismatches, 'status'] = 'DIFERENCIA_COSTO'

    # 6. Devolver únicamente los proyectos con anomalías
    errors = comparison[comparison['status'] != 'OK']

    return errors




def validate_file(filename, columns):
    path = DATA_DIR / filename
    df = pd.read_csv(path)

    duplicates = check_duplicates(df, columns)

    print(f'{filename}: {duplicates} duplicados')


def main():
    # 1. Validar duplicados
    for filename, columns in KEYS.items():
        validate_file(filename, columns)

    # 2. Cargar tabla principal
    projects = pd.read_csv(DATA_DIR / 'projects.csv')

    # 3. Validar integridad referencial
    for filename in ['tasks.csv', 'transactions.csv', 'timesheets.csv']:
        df = pd.read_csv(DATA_DIR / filename)
        invalid = check_project_references(df, projects)
        print(f'{filename}: {invalid} referencias inválidas')

    # 4. Validar importes negativos
    negative_budgets = check_negative_amounts(projects, 'budget_usd')
    print(f'Projects: {negative_budgets} presupuestos negativos')

    transactions = pd.read_csv(DATA_DIR / 'transactions.csv')
    negative_costs = check_negative_amounts(transactions, 'amount_usd')
    print(f'Transactions: {negative_costs} importes negativos')

        # 6. Validar conciliación financiera
    reconciliation_errors = check_cost_reconciliation(
        projects,
        transactions
    )

    print(
        f'Conciliación: {len(reconciliation_errors)} proyectos con diferencias'
    )

    if not reconciliation_errors.empty:
        print('\nDETALLE DE ANOMALÍAS')
        print(reconciliation_errors)

    # 6. Validar horas de timesheets
    timesheets = pd.read_csv(DATA_DIR / 'timesheets.csv')
    invalid_hours = check_hours_out_of_range(timesheets)
    print(f'Timesheets: {invalid_hours} registros con horas fuera de rango')

    labor_errors = check_labor_costs(timesheets)
    print(f'Timesheets: {labor_errors} errores de costo laboral')

    weekly_errors = check_weekly_hours(timesheets)
    print(f'Timesheets: {weekly_errors} semanas sobre 40 horas')

    week_start_errors = check_week_start(timesheets)
    print(f'Timesheets: {week_start_errors} fechas de inicio de semana incorrectas')

if __name__ == '__main__':
    main()
