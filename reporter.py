import os

def save_report(content, filename="reports/report.md"):
    os.makedirs("reports", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Reporte guardado en {filename}")
