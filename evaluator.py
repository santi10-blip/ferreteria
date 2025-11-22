def validate_report(report_text):
    if len(report_text) < 100:
        print("Advertencia: reporte muy corto, posible error en ejecución")
    else:
        print("Reporte validado correctamente")
