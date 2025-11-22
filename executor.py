# src/executor.py
import os
import pandas as pd
import matplotlib.pyplot as plt

from src.db import SessionLocal, Producto, Compra


# ============================================================
# 1. ANALIZAR DATASET CSV
# ============================================================
def analyze_dataset(path):
    """Lee un CSV y genera estadísticas básicas."""
    df = pd.read_csv(path)
    summary = df.describe(include="all").to_string()
    return summary


# ============================================================
# 2. OPERACIONES SOBRE LA BASE DE DATOS DEL AGENTE
# ============================================================
class ExecutorDB:

    def __init__(self, report_folder="reports"):
        self.report_folder = report_folder
        self.graphs_folder = os.path.join(report_folder, "graphs")
        os.makedirs(self.graphs_folder, exist_ok=True)

    # ---------- GUARDAR RESULTADOS DEL AGENTE ----------
    def save_analysis(self, instruccion, resumen):
        """Guarda en la tabla análisis del agente."""
        session = SessionLocal()
        try:
            session.execute(
                """
                INSERT INTO analisis (instruccion, resumen)
                VALUES (:instr, :res)
                """,
                {"instr": instruccion, "res": resumen}
            )
            session.commit()
        finally:
            session.close()


    # ---------- CONSULTAR PRODUCTOS (STOCK ALTO) ----------
    def top_products_by_stock(self, top_n=10):
        session = SessionLocal()
        rows = session.query(Producto).order_by(Producto.stock.desc()).limit(top_n).all()
        session.close()
        return [{"id": r.id, "nombre": r.nombre, "stock": r.stock, "precio": float(r.precio)} for r in rows]


    # ---------- CONSULTAR PRODUCTOS (STOCK BAJO) ----------
    def low_stock(self, threshold=10):
        session = SessionLocal()
        rows = session.query(Producto).filter(Producto.stock < threshold).all()
        session.close()
        return [{"id": r.id, "nombre": r.nombre, "stock": r.stock} for r in rows]


    # ---------- GENERAR GRÁFICO DE STOCK ----------
    def generate_stock_graph(self, out_name="stock_por_producto.png"):
        session = SessionLocal()
        rows = session.query(Producto).all()
        session.close()

        if not rows:
            return None

        df = pd.DataFrame([{"producto": r.nombre, "stock": r.stock} for r in rows])
        df = df.sort_values("stock", ascending=False)

        plt.figure(figsize=(10, 5))
        df.set_index("producto")["stock"].plot(kind="bar")

        output_path = os.path.join(self.graphs_folder, out_name)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return output_path
    # ---------- CONSULTAR COMPRAS POR PROVEEDOR ----------