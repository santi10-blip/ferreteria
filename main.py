import os
import sys

from src.planner import generate_plan
from src.retriever import Retriever
from src.executor import analyze_dataset, ExecutorDB
from src.reasoner import generate_text
from src.reporter import save_report
from src.evaluator import validate_report
from src.db import init_db



def main():

    # ================================
    # 1. Validación de argumentos
    # ================================
    if len(sys.argv) < 2:
        print("Uso: python -m src.main \"Instrucción para el agente\" --dataset data/ventas.csv")
        return

    instruction = sys.argv[1]
    dataset_path = "data/ventas.csv" if "--dataset" not in sys.argv else sys.argv[sys.argv.index("--dataset")+1]

    print("\n=== AGENTE FERRETERÍA ===\n")

    # ================================
    # 2. Inicializar Base de Datos
    # ================================
    print("📦 Inicializando base de datos...")
    ## init_db()

    executor_db = ExecutorDB()  # ← conexión lista

    # ================================
    # 3. Plan del agente
    # ================================
    print("🧠 Generando plan...")
    plan = generate_plan(instruction)
    for step in plan:
        print(" -", step)

    # ================================
    # 4. Recuperación de documentos (RAG)
    # ================================
    print("\n📄 Recuperando evidencia documental...")

    retriever = Retriever()

    if not retriever.index_path or not os.path.exists(retriever.index_path):
        print("🔧 Creando índice de documentos...")
        retriever.index_documents(doc_folder="data")

    evidence = retriever.retrieve(instruction)
    print(f"✔ Evidencia encontrada: {len(evidence)} fragmentos")

    # ================================
    # 5. Análisis del dataset
    # ================================
    print("\n📊 Analizando dataset:", dataset_path)
    summary = analyze_dataset(dataset_path)
    print("✔ Resumen:", summary[:120], "...")  # muestra solo un pedazo

    # ================================
    # 6. Guardar análisis en la Base de Datos
    # ================================
    print("\n🗄 Guardando el análisis en la base de datos...")
    ## executor_db.save_analysis(instruction, summary)

    # ================================
    # 7. Generar reporte final
    # ================================
    print("\n📝 Generando reporte final...")
    report_text = generate_text(summary, evidence)

    save_report(report_text)
    validate_report(report_text)

    print("\n📁 Reporte generado correctamente.")
    print("\n=== FIN DEL AGENTE ===\n")


if __name__ == "__main__":
    main()
