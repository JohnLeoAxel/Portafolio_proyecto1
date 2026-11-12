# Bitácora del proyecto - Financial BI Portfolio

## Día 1 - Configuración inicial

### Objetivo

Configurar el entorno de desarrollo y establecer la estructura inicial del proyecto de análisis financiero y control de costos.

### Actividades realizadas

- [x] Crear entorno virtual (`.venv`).
- [x] Configurar Visual Studio Code.
- [x] Crear estructura de carpetas del proyecto.
- [x] Crear `README.md`.
- [x] Verificar dependencias de Python.
- [x] Documentar el modelo de datos.
- [x] Configurar Git y realizar el primer commit.

### Problemas encontrados

- Se realizaron ajustes iniciales en la configuración del entorno de desarrollo.
- Se estableció el uso de un entorno virtual para aislar las dependencias del proyecto.

### Aprendizajes

- Comprender la función de los entornos virtuales.
- Comprender la estructura básica de un proyecto Python.
- Entender la importancia de separar los datos, el código y la documentación.
- Conocer los fundamentos del control de versiones mediante Git.

### Resultado

- Entorno virtual configurado y funcional.
- Estructura del proyecto creada.
- Dependencias verificadas.
- Modelo de datos documentado.
- Repositorio Git configurado.
- Primer commit realizado.

**Estado:** Día 1 completado.

---

## Día 2 - Generación de datos sintéticos y calidad de datos

### Objetivo

Construir un conjunto reproducible de datos sintéticos para simular el control financiero de proyectos de ingeniería, incorporando presupuestos, costos, recursos, avance y métricas de desempeño.

### Actividades realizadas

- [x] Generar 25 proyectos con presupuestos, fechas y factores de sobrecosto.
- [x] Implementar semillas aleatorias independientes para cada generador.
- [x] Crear funciones de curva S para distribuir costos a lo largo del proyecto.
- [x] Generar 100 tareas WBS con presupuesto y avance planificado y real.
- [x] Generar 48,136 transacciones de costos en USD y MXN.
- [x] Generar 29,922 registros de timesheets.
- [x] Incorporar roles, tarifas por hora y costos laborales.
- [x] Agregar fecha de inicio de semana para análisis semanal.
- [x] Implementar el parámetro `--as-of` para generar avances a distintas fechas de corte.
- [x] Implementar cálculos iniciales de Earned Value Management (EVM).
- [x] Crear validaciones de integridad, conciliación financiera y horas laborales.
- [x] Comprobar reproducibilidad mediante hashes SHA256.

### Resultados financieros del portafolio sintético

| Indicador | Resultado |
|---|---:|
| Proyectos | 25 |
| Proyectos con ahorros | 12 |
| Proyectos con sobrecostos | 9 |
| Proyectos en presupuesto | 4 |
| Sobrecostos acumulados | $40,801,480.68 USD |
| Ahorros acumulados | $21,111,686.99 USD |

### Calidad de datos

Las validaciones de calidad e integridad implementadas finalizaron sin anomalías:

- Duplicados.
- Integridad referencial.
- Presupuestos y costos negativos.
- Conciliación de costos por proyecto.
- Horas diarias fuera de rango.
- Cálculo de costos laborales.
- Horas semanales superiores a 40.
- Correspondencia de fechas de inicio de semana.

### Fundamentos de Earned Value Management

Se implementaron las siguientes métricas:

| Indicador | Descripción |
|---|---|
| BAC | Budget at Completion |
| PV | Planned Value |
| EV | Earned Value |
| AC | Actual Cost |
| SV | Schedule Variance |
| CV | Cost Variance |
| SPI | Schedule Performance Index |
| CPI | Cost Performance Index |
| EAC | Estimate at Completion |
| VAC | Variance at Completion |

### Aprendizajes

- Uso de semillas independientes para reproducibilidad.
- Generación de datos sintéticos con Python.
- Manipulación y agregación de datos con Pandas.
- Uso de curvas S para distribuir costos.
- Relación entre `groupby()` de Pandas y `GROUP BY` de SQL.
- Diferencia entre presupuesto, costo real y desviación.
- Fundamentos de BAC, PV, EV, AC, CPI, SPI, EAC y VAC.
- Importancia de validar la calidad antes de cargar datos a un sistema analítico.

### Limitaciones del modelo

- Los datos son sintéticos y no representan información real de una empresa.
- Los costos laborales de timesheets son independientes de la categoría Labor de las transacciones; no deben sumarse sin una conciliación adicional.
- El avance real de las tareas y la curva de costos se generan independientemente.
- El tipo de cambio utilizado es fijo en 18 MXN/USD.
- El parámetro `--as-of` modifica el avance de tareas, mientras que transacciones y timesheets conservan el ciclo completo del proyecto.

### Resultado

Se construyó un conjunto de datos sintéticos reproducible, con relaciones entre proyectos, tareas, transacciones y recursos. También se implementaron validaciones de integridad y métricas iniciales de desempeño financiero.

**Estado:** Día 2 completado.

---

## Día 3 - Calidad de datos, Excel sucio y facturación

### Objetivo

Simular procesos de facturación y exportaciones de ERP con defectos controlados, preparando los datos para su posterior limpieza, transformación y análisis financiero.

### Actividades realizadas

#### Generación de facturas

- [x] Crear facturas Fixed Price mediante hitos contractuales.
- [x] Generar contratos Fixed Price con un valor entre 110% y 125% del presupuesto del proyecto.
- [x] Distribuir la facturación Fixed Price en cuatro hitos:
  - Design: 20%.
  - Engineering: 30%.
  - Construction: 30%.
  - Delivery: 20%.
- [x] Generar facturas T&M agrupadas por proyecto y periodo mensual.
- [x] Calcular las facturas T&M utilizando las horas y los costos laborales registrados.
- [x] Conciliar la facturación T&M con los costos laborales sintéticos.
- [x] Validar reproducibilidad de las transformaciones con semilla 42.
- [x] Confirmar 7 duplicados y 5 valores nulos en project_id.
- [x] Confirmar alteraciones de nombres en P009 y P018.
- [x] Validar los tres formatos de fecha en el Excel.
- [x] Validar formato monetario en los 463 registros de facturas.
- [x] Probar representación de importes negativos entre paréntesis.


#### Resultados de facturación

| Indicador | Resultado |
|---|---:|
| Facturas Fixed Price | 36 |
| Facturas T&M | 420 |
| Total de facturas originales | 456 |
| Importe Fixed Price | $288,099,608.46 USD |
| Importe T&M | $9,892,735.00 USD |
| Facturación total | $297,992,343.46 USD |

La facturación T&M presenta una diferencia de conciliación de $0.00 USD respecto al costo laboral generado por los timesheets.

#### Construcción del reporte Oracle

- [x] Crear un reporte Excel con tres filas iniciales de título.
- [x] Incorporar encabezados en la cuarta fila.
- [x] Agregar encabezados repetidos cada 50 registros.
- [x] Incorporar subtotales por proyecto.
- [x] Introducir formatos mixtos de fechas.
- [x] Representar importes monetarios como texto.
- [x] Crear variaciones de nombres de proyectos mediante mayúsculas, minúsculas y espacios adicionales.
- [x] Inyectar duplicados controlados.
- [x] Introducir valores nulos en la clave `project_id`.
- [x] Implementar funciones para generar formatos de fechas e importes inconsistentes.
- [x] Utilizar un generador aleatorio controlado para reproducibilidad.

#### Lectura del reporte

- [x] Leer el Excel mediante `pandas.read_excel()`.
- [x] Utilizar `skiprows=3` para omitir las filas iniciales de título.
- [x] Utilizar `dtype=str` para importar las columnas como texto.
- [x] Comprobar la presencia de encabezados repetidos.
- [x] Identificar las filas de subtotal.
- [x] Verificar los registros con valores nulos.

### Defectos controlados del reporte Oracle

| Defecto o elemento | Cantidad |
|---|---:|
| Facturas originales | 456 |
| Filas duplicadas agregadas | 7 |
| Nulos en `project_id` | 5 |
| Proyectos con nombres alterados | 2 |
| Filas de subtotal | 25 |
| Encabezados repetidos | 9 |
| Filas de título | 3 |
| Total de filas físicas en Excel | 501 |

**Archivo generado:** `data/raw_files/reporte_oracle_20261112.xlsx`

**Semilla de reproducibilidad:** 42.

**Validación estructural:**

- 501 filas físicas en el archivo Excel.
- 497 filas leídas después de omitir las tres filas iniciales.
- 463 registros de facturas, incluyendo duplicados y registros con claves nulas.
- 9 encabezados repetidos.
- 25 filas de subtotal.
- 5 valores nulos en `project_id`.
- 7 duplicados exactos.

**Nota:** Los duplicados y nulos son defectos intencionales. Los subtotales y encabezados repetidos son elementos estructurales del reporte, no facturas.

### Aprendizajes

- Diferencia entre archivos CSV, Excel, JSON y Parquet.
- Importancia de controlar los tipos de datos durante la importación.
- Uso de `read_excel()` con `skiprows` y `dtype`.
- Diferencia entre datos originales y datos transformados.
- Identificación de problemas de completitud, unicidad, validez, consistencia, exactitud y oportunidad.
- Importancia de conservar los datos originales sin modificaciones.
- Diferencia entre facturación Fixed Price y T&M.
- Fundamentos de facturación por hitos contractuales.
- Diferencia entre facturación y reconocimiento de ingresos.
- Representación de importes negativos mediante paréntesis en reportes financieros.

### Limitaciones del modelo

- Los datos continúan siendo sintéticos.
- La facturación Fixed Price utiliza hitos y porcentajes predeterminados; no representa necesariamente las condiciones de un contrato real.
- La facturación T&M utiliza los costos laborales como aproximación didáctica al importe facturado. No representa las tarifas contractuales reales ni el margen comercial.
- La facturación y el reconocimiento de ingresos son conceptos distintos y todavía no se implementa un modelo completo de reconocimiento de ingresos.
- Los defectos del reporte Oracle son intencionales y tienen cantidades controladas para evaluar posteriormente el proceso de limpieza.

### Próximos pasos

- [ ] Validar el tratamiento de importes negativos representados entre paréntesis.
- [ ] Documentar los conteos exactos de defectos como referencia para las siguientes etapas.
- [ ] Implementar el proceso de limpieza de encabezados, subtotales y registros duplicados.
- [ ] Normalizar nombres de proyectos, fechas e importes.
- [ ] Validar que los datos limpios concilien con los registros originales.
- [ ] Completar las actividades restantes de la guía del Día 3.

**Estado:** Día 3 en progreso.