# Bitácora del proyecto

## Día 1 - Configuración inicial

### Objetivo
Configurar el entorno de desarrollo y establecer la estructura inicial del proyecto de análisis de costos.

### Actividades realizadas
- [x] Crear entorno virtual (.venv).
- [x] Configurar Visual Studio Code.
- [x] Crear estructura de carpetas.
- [x] Crear README.md.
- [ ] Verificar dependencias de Python.
- [ ] Documentar el modelo de datos.
- [ ] Configurar Git y realizar el primer commit.

### Problemas encontrados
Pendiente de documentar.

### Aprendizajes
- Comprendí la función del entorno virtual.
- Comprendí la estructura básica de un proyecto Python.
- Comprendí la importancia de separar los datos, el código y la documentación.

### Próximos pasos
Completar la documentación del modelo de datos y preparar el repositorio para su primer commit.


## Día 2 - Generación de datos sintéticos y calidad de datos

### Objetivo
Construir un conjunto reproducible de datos sintéticos para simular el control financiero de proyectos de ingeniería.

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
Los nueve controles implementados finalizaron sin anomalías:
- Duplicados.
- Integridad referencial.
- Presupuestos y costos negativos.
- Conciliación de costos por proyecto.
- Horas diarias fuera de rango.
- Cálculo de costos laborales.
- Horas semanales superiores a 40.
- Correspondencia de fechas de inicio de semana.

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

### Próximos pasos
- Reforzar validaciones financieras y temporales.
- Completar el aprendizaje de tipos de datos y Pandas.
- Preparar la carga de datos hacia DuckDB y SQL.