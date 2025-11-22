import os

def generate_text(summary, evidence):
    text = "## Análisis de Ventas\n\n"
    text += str(summary) + "\n\n"
    text += "## Evidencia Documental\n\n"
    for i, e in enumerate(evidence, 1):
        text += f"{i}. {e[:300]}...\n\n"
    return text
