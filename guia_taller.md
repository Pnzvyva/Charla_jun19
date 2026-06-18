# Taller de ciencia de datos: programa de subsidios educativos (principiantes)

## Objetivo del taller

Practicar un flujo básico de analítica de datos —carga, limpieza simple,
cálculo de indicadores, evaluación de impacto y segmentación— sobre un caso
realista: una empresa que gestiona subsidios educativos (becas, computadores,
planes móviles, internet y bibliotecas digitales) para el Estado colombiano.

El dataset es **sintético** pero reproduce problemas reales: los datos de
texto llegan con errores de codificación y mayúsculas inconsistentes, y la
comparación simple entre beneficiarios y no beneficiarios requiere un análisis
cuidadoso.

## Archivos incluidos

| Archivo | Contenido |
|---|---|
| `subsidios_educativos.csv` | Dataset de 2.500 solicitudes simuladas |
| `taller_subsidios_principiantes.py` | Script principiante: carga, limpieza básica, KPIs, SROI, segmentación y 3 gráficos |
| `guia_taller_avanzado.md` | Versión extendida del taller (con SROI, PSM, 6 gráficos, etc.) |
| `guia_taller.md` | Este documento |

## Instalación y ejecución

```bash
pip install pandas matplotlib scikit-learn
python taller_subsidios_principiantes.py
```

El script debe ejecutarse en la misma carpeta donde está el archivo
`subsidios_educativos.csv`. Al correrlo se imprimen los resultados en la
consola y se muestran 3 gráficos en pantalla.

## Diccionario de datos

| Columna | Descripción |
|---|---|
| `id_solicitud` | Identificador único de la solicitud |
| `fecha_solicitud` | Fecha en que se radicó la solicitud |
| `departamento` | Departamento de residencia del solicitante. **Llega "sucio" a propósito**: mezcla errores de codificación, tildes perdidas, mayúsculas inconsistentes |
| `zona` | Urbano o rural |
| `tipo_beneficio` | Beca, Computador, Plan_movil, Internet o Biblioteca_digital |
| `canal` | Presencial o Digital |
| `nivel_educativo_tutor` | Nivel educativo del tutor legal |
| `num_personas_hogar` | Número de personas en el hogar |
| `ingreso_hogar` | Ingreso mensual del hogar (COP) |
| `puntaje_focalizacion` | Índice de vulnerabilidad (0-100, mayor = más vulnerable) |
| `estado_solicitud` | Aprobada o Rechazada |
| `gestor_asignado` | Gestor que procesó la solicitud |
| `tiempo_ciclo_dias` | Días entre la solicitud y la decisión |
| `fecha_decision` | Fecha de aprobación o rechazo |
| `fecha_entrega` | Fecha de entrega efectiva del beneficio (solo aprobadas) |
| `costo_atencion` | Costo administrativo de procesar la solicitud (COP) |
| `costo_beneficio` | Costo del beneficio entregado (COP, solo aprobadas) |
| `permanencia_escolar` | 1 si el estudiante continúa escolarizado en el seguimiento, 0 si no (puede haber nulos) |
| `transito_educacion_superior` | 1 si transitó a educación superior, 0 si no (puede haber nulos) |
| `ingreso_hogar_posterior` | Ingreso del hogar en el seguimiento, ~12-18 meses después (puede haber nulos) |
| `satisfaccion_servicio` | Satisfacción reportada, escala 1-5 (solo aprobadas) |

## Estructura del análisis (script)

1. **Carga y exploración inicial**: lectura del CSV, conteo de registros y
   vista de las primeras filas.
2. **Calidad de datos**: limpieza básica de la columna `departamento`
   (minúsculas + eliminación de espacios) y comparación de valores antes y
   después.
3. **KPIs del programa**: tasa de aprobación, costo total del programa y
   costo por beneficiario.
4. **Gráfica 1**: solicitudes por tipo de beneficio (gráfico de barras).
5. **Evaluación de impacto**: comparación de la permanencia escolar promedio
   entre solicitudes aprobadas y rechazadas.
6. **SROI simplificado**: estimación del retorno social de la inversión a
   partir de la diferencia en permanencia escolar, con un valor social
   asumido de $5.000.000 COP por estudiante retenido y un ajuste por
   deadweight del 15 %.
7. **Gráfica 2**: permanencia escolar por estado (gráfico de barras).
8. **Segmentación**: K-Means con 3 clústeres sobre ingreso del hogar, puntaje
   de focalización y tamaño del hogar (datos estandarizados).
9. **Gráfica 3**: dispersión de puntaje de focalización vs. ingreso del hogar
   coloreada por segmento.
10. **Conclusiones**: cinco ideas clave extraídas del análisis.

## Preguntas guía para la discusión en grupo

- ¿Qué problemas de calidad encontraste en la columna `departamento` al
  inicio? ¿La limpieza con `lower()` y `strip()` resuelve todos los problemas?
  ¿Qué otros pasos harían falta?
- ¿Cuál es la tasa de aprobación del programa? ¿Te parece alta o baja?
- ¿Cuánto cuesta en promedio cada beneficiario? ¿Cómo se compara ese valor
  con el contexto educativo colombiano?
- ¿Los aprobados tienen mayor permanencia escolar que los rechazados? ¿Podemos
  concluir que el programa *causó* esa diferencia? ¿Qué otros factores
  podrían explicarla?
- ¿Qué SROI obtuviste? ¿Qué significa que por cada $1 invertido se generen
  $X en valor social? ¿Por qué se descuenta un 15 % de deadweight?
- ¿Cuántos segmentos encontró K-Means? ¿Qué perfil tiene cada uno? ¿Cuál
  sería el segmento prioritario si hubiera que asignar recursos limitados?
- ¿Qué otros KPIs agregarías para tener una visión más completa del programa?
