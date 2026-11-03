# Modelo de datos - Pipeline de costos

## 1. Objetivo

Diseñar un modelo de datos para administrar y analizar información financiera y operativa de proyectos.

El modelo permitirá analizar:

- Presupuesto vs. costo real.
- Costos por proyecto.
- Costos por categoría.
- Horas trabajadas.
- Facturación.
- Variaciones financieras.
- Efectos de los tipos de cambio.

## 2. Tablas principales

El modelo estará compuesto inicialmente por seis tablas:

1. projects
2. wbs_tasks
3. cost_transactions
4. timesheets
5. invoices
6. fx_rates

---

## 3. Definición de tablas

### 3.1 projects

**Objetivo:** almacenar la información general de cada proyecto.

**Granularidad:** un registro por proyecto.

**Llave primaria:** project_id.

| Campo | Descripción |
|---|---|
| project_id | Identificador único del proyecto. |
| project_name | Nombre del proyecto. |
| project_type | Tipo de proyecto: Data Center, Solar o Wind. |
| contract_type | Tipo de contrato: Fixed Price o T&M. |
| customer | Nombre del cliente. |
| start_date | Fecha de inicio. |
| end_date | Fecha de finalización estimada. |
| budget | Presupuesto inicial. |
| currency | Moneda del proyecto. |
| status | Estado del proyecto. |

### 3.2 wbs_tasks

**Objetivo:** almacenar las actividades y estructuras de trabajo de cada proyecto.

**Granularidad:** un registro por actividad o tarea WBS.

**Llave primaria:** task_id.

**Llave foránea:** project_id.

| Campo | Descripción |
|---|---|
| task_id | Identificador único de la tarea. |
| project_id | Proyecto al que pertenece. |
| task_code | Código de la actividad WBS. |
| task_name | Nombre de la actividad. |
| parent_task_id | Identificador de la actividad padre, si existe. |
| budgeted_cost | Costo presupuestado de la actividad. |
| start_date | Fecha de inicio. |
| end_date | Fecha de finalización. |
| status | Estado de la actividad. |

### 3.3 cost_transactions

**Objetivo:** registrar los costos reales asociados a los proyectos.

**Granularidad:** un registro por línea de transacción de costo.

**Llave primaria:** transaction_id.

**Llaves foráneas:** project_id y task_id.

| Campo | Descripción |
|---|---|
| transaction_id | Identificador único de la transacción. |
| project_id | Proyecto asociado. |
| task_id | Actividad WBS asociada. |
| transaction_date | Fecha de registro del costo. |
| cost_type | Labor, Materials, Subcontracts u Other. |
| description | Descripción del costo. |
| vendor | Proveedor, si aplica. |
| amount | Importe de la transacción. |
| currency | Moneda de la transacción. |

### 3.4 timesheets

**Objetivo:** registrar las horas trabajadas por los recursos en los proyectos.

**Granularidad:** un registro por recurso, proyecto, tarea y día.

**Llaves primarias:** timesheet_id.

**Llaves foráneas:** project_id y task_id.

| Campo | Descripción |
|---|---|
| timesheet_id | Identificador único del registro. |
| employee_id | Identificador del empleado. |
| project_id | Proyecto asociado. |
| task_id | Actividad WBS asociada. |
| work_date | Fecha de trabajo. |
| hours_worked | Horas trabajadas. |
| hourly_rate | Tarifa por hora. |
| currency | Moneda de la tarifa. |

### 3.5 invoices

**Objetivo:** registrar las facturas emitidas a los clientes.

**Granularidad:** un registro por factura o hito de facturación.

**Llave primaria:** invoice_id.

**Llave foránea:** project_id.

| Campo | Descripción |
|---|---|
| invoice_id | Identificador único de factura. |
| project_id | Proyecto asociado. |
| invoice_date | Fecha de emisión. |
| due_date | Fecha de vencimiento. |
| invoice_amount | Importe facturado. |
| currency | Moneda de facturación. |
| invoice_status | Estado de la factura. |
| payment_date | Fecha de pago, si aplica. |

### 3.6 fx_rates

**Objetivo:** almacenar los tipos de cambio para convertir importes entre monedas.

**Granularidad:** un registro por fecha y par de monedas.

**Llave primaria:** rate_date + base_currency + quote_currency.

| Campo | Descripción |
|---|---|
| rate_date | Fecha del tipo de cambio. |
| base_currency | Moneda de origen. |
| quote_currency | Moneda de destino. |
| exchange_rate | Tipo de cambio. |

---

## 4. Relaciones entre tablas

- projects tiene una relación de uno a muchos con wbs_tasks.
- projects tiene una relación de uno a muchos con cost_transactions.
- projects tiene una relación de uno a muchos con timesheets.
- projects tiene una relación de uno a muchos con invoices.
- wbs_tasks tiene una relación de uno a muchos con cost_transactions.
- wbs_tasks tiene una relación de uno a muchos con timesheets.

fx_rates se utilizará como referencia para convertir importes según la fecha y el par de monedas.

---

## 5. Reglas de negocio iniciales

1. Los proyectos podrán manejarse en USD o MXN.
2. Los tipos de proyecto serán Data Center, Solar y Wind.
3. Los contratos podrán ser Fixed Price o T&M.
4. Las categorías de costos serán Labor, Materials, Subcontracts y Other.
5. Cada transacción deberá estar asociada a un proyecto.
6. Los importes deberán conservar su moneda original.
7. Las conversiones de moneda deberán utilizar el tipo de cambio correspondiente.
8. Los registros originales deberán conservarse sin modificaciones durante la extracción y carga inicial.

---

## 6. Indicadores financieros que queremos construir

- Total Budget.
- Actual Cost.
- Budget Variance.
- Budget Consumption %.
- Labor Cost.
- Material Cost.
- Subcontract Cost.
- Total Hours Worked.
- Revenue.
- Project Gross Margin.
- Gross Margin %.

---

## 7. Consideraciones de diseño

- Definir la granularidad antes de desarrollar las tablas.
- Evitar registros duplicados.
- Mantener identificadores únicos.
- Documentar las relaciones entre tablas.
- Conservar los importes originales y sus monedas.
- Mantener los datos originales sin alteraciones.