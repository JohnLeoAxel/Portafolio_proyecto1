import random
from datetime import date

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

SEED = 42

COLUMNAS_REPORTE = [
    'project_id',
    'project_name',
    'billing_type',
    'invoice_date',
    'period_start',
    'period_end',
    'invoice_description',
    'total_hours',
    'amount_usd',
]

MESES = [
    'ene', 'feb', 'mar', 'abr',
    'may', 'jun', 'jul', 'ago',
    'sep', 'oct', 'nov', 'dic'
]


def fecha_sucia(d, rng):
    formato = rng.choice(['iso', 'dmy', 'texto'])

    if formato == 'iso':
        return d.strftime('%Y-%m-%d')

    if formato == 'dmy':
        return d.strftime('%d/%m/%Y')

    return f'{d.day}-{MESES[d.month - 1]}-{str(d.year)[2:]}'


def monto_sucio(x):
    if x < 0:
        return f'(${abs(x):,.2f})'

    return f'${x:,.2f}'

def preparar_datos_reporte(facturas, projects):
    reporte = facturas.merge(
        projects[['project_id', 'project_name']],
        on='project_id',
        how='left',
        validate='many_to_one'
    )

    return reporte[COLUMNAS_REPORTE]

def nombre_sucio(nombre, rng, permitir_normal=True):
    variaciones = [
        'mayusculas',
        'minusculas',
        'espacios',
    ]

    if permitir_normal:
        variaciones.append('normal')

    variacion = rng.choice(variaciones)

    if variacion == 'mayusculas':
        return nombre.upper()

    if variacion == 'minusculas':
        return nombre.lower()

    if variacion == 'espacios':
        return nombre + '   '

    return nombre

def ensuciar_nombres(reporte, rng):
    datos = reporte.copy()

    proyectos = (
        datos['project_id']
        .drop_duplicates()
        .tolist()
    )

    seleccionados = rng.sample(proyectos, 2)

    for project_id in seleccionados:
        mascara = datos['project_id'] == project_id
        nombre = datos.loc[mascara, 'project_name'].iloc[0]

        datos.loc[mascara, 'project_name'] = nombre_sucio(
            nombre,
            rng,
            permitir_normal=False
        )

    return datos

def inyectar_duplicados(reporte, rng):
    cantidad = round(len(reporte) * 0.015)

    duplicados = reporte.sample(
        n=cantidad,
        random_state=rng.randint(0, 100000)
    )

    datos = pd.concat(
        [reporte, duplicados],
        ignore_index=True
    )

    return datos

def inyectar_nulos(reporte, rng):
    datos = reporte.copy()

    cantidad = round(len(datos) * 0.01)

    indices = rng.sample(
        list(datos.index),
        cantidad
    )

    datos.loc[indices, 'project_id'] = None

    return datos

def generar_reporte_sucio(facturas, projects, rng):
    datos = preparar_datos_reporte(facturas, projects)
    datos = ensuciar_nombres(datos, rng)
    datos = inyectar_duplicados(datos, rng)

    datos['_project_group'] = datos['project_id']
    datos = inyectar_nulos(datos, rng)

    return datos

def convertir_fila_sucia(fila, rng):
    datos = fila.copy()

    for columna in ['invoice_date', 'period_start', 'period_end']:
        if pd.notna(datos[columna]):
            datos[columna] = fecha_sucia(datos[columna], rng)

    if pd.notna(datos['amount_usd']):
        datos['amount_usd'] = monto_sucio(datos['amount_usd'])

    return datos

def escribir_reporte_oracle(datos, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Oracle Report'

    ws['A1'] = 'ORACLE - PROJECT BILLING REPORT'
    ws['A2'] = 'Synthetic Data - USD'
    ws['A3'] = 'Generated Report'

    ws.append(COLUMNAS_REPORTE)

    for celda in ws[4]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = PatternFill(
            fill_type='solid',
            fgColor='1F4E78'
        )

    ws.freeze_panes = 'A5'
    ws.auto_filter.ref = f'A4:I{len(datos) + 4}'

    wb.save(output_path)

def escribir_reporte_oracle(datos, output_path, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Oracle Report'

    ws['A1'] = 'ORACLE - PROJECT BILLING REPORT'
    ws['A2'] = 'Synthetic Data - USD'
    ws['A3'] = 'Generated Report'

    ws.append(COLUMNAS_REPORTE)

    for celda in ws[4]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = PatternFill(
            fill_type='solid',
            fgColor='1F4E78'
        )

    ws.freeze_panes = 'A5'

    contador = 0

    for project_id, grupo in datos.groupby(
        '_project_group',
        sort=False
    ):
        for _, fila in grupo.iterrows():
            sucia = convertir_fila_sucia(fila, rng)

            ws.append([
                None if pd.isna(sucia[columna]) else sucia[columna]
                for columna in COLUMNAS_REPORTE
            ])

            contador += 1

            if contador % 50 == 0:
                ws.append(COLUMNAS_REPORTE)

        subtotal = grupo['amount_usd'].sum()

        ws.append([
            f'Total Proyecto {project_id}',
            None, None, None, None, None,
            'Subtotal',
            None,
            monto_sucio(subtotal)
        ])

    ws.auto_filter.ref = f'A4:I{ws.max_row}'

    wb.save(output_path)