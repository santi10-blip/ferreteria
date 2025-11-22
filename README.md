# Agente Cognitivo para Ferretería

## Descripción

Este proyecto implementa un **agente cognitivo autónomo** para una ferretería.
El agente es capaz de:

* Interpretar instrucciones en lenguaje natural.
* Recuperar información relevante de documentos (PDF/DOCX) usando RAG (Retrieval-Augmented Generation).
* Analizar datasets de ventas o inventario (CSV/JSON).
* Generar reportes con evidencia citada y gráficos.
* Validar la coherencia y trazabilidad del análisis.

El objetivo es integrar **IA, análisis de datos y documentación** en un flujo reproducible.

---

## Arquitectura Modular

1. **Planner**: genera un plan de acción basado en la instrucción.
2. **Retriever**: indexa y recupera fragmentos de documentos relevantes.
3. **Executor**: analiza el dataset y genera estadísticas y gráficos.
4. **Reasoner**: combina resultados del análisis con evidencia documental.
5. **Reporter**: genera un reporte en Markdown.
6. **Evaluator**: valida coherencia y trazabilidad del reporte.

---

## Estructura de Carpetas

```
agent_ferreteria/
│
├─ data/               # CSV y PDFs/DOCX de ejemplo
├─ reports/            # Reportes generados por el agente
├─ docs_index/         # Índice para RAG
├─ src/                # Código fuente modular
│  ├─ main.py
│  ├─ planner.py
│  ├─ retriever.py
│  ├─ executor.py
│  ├─ reasoner.py
│  ├─ reporter.py
│  └─ evaluator.py
├─ requirements.txt
└─ README.md
```

---

## Requisitos

* Python 3.10 o superior
* Librerías (instalables vía `pip`):

```bash
pip install -r requirements.txt
```

---

## Ejecución

1. Activar el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

2. Generar datos de ejemplo (opcional):

```powershell
python create_demo.py
```

3. Ejecutar el agente:

```powershell
python -m src.main "Analiza data/ventas.csv y sustenta con ManualInventario.pdf" --dataset data/ventas.csv
```

4. Revisar el reporte generado:

```
reports/report.md
reports/cantidad_por_producto.png
```

---

## Personalización

* Sustituye `data/ventas.csv` por tus propios datos de ventas o inventario.
* Sustituye `data/ManualInventario.pdf` por manuales o documentos reales de la ferretería.
* Modifica `executor.py` para agregar más gráficos o análisis estadísticos según tus necesidades.

---

## Licencia

Este proyecto es educativo y puede ser usado libremente para fines de aprendizaje y desarrollo de prototipos.
