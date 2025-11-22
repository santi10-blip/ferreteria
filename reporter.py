import os
from datetime import datetime

class Reporter:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_report(self, instruction, analysis, evidence, reasoning):
        """Genera un reporte completo en Markdown"""
        
        report_content = f"""# Reporte de Análisis - Ferretería

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Instrucción:** {instruction}

## 📊 Resumen Ejecutivo

Análisis completo del dataset con evidencia documental relevante.

## 📈 Análisis Estadístico
