def generate_plan(instruction):
    """
    Genera un plan de pasos basado en la instrucción.
    """
    plan = [
        "Interpretar instrucción",
        "Identificar datos y documentos necesarios",
        "Recuperar información relevante del manual",
        "Analizar dataset",
        "Fusionar resultados con evidencia",
        "Generar reporte final",
        "Validar coherencia y trazabilidad"
    ]
    print("Plan generado:")
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")
    return plan
