import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class Executor:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def analyze_dataset(self, dataset_path):
        """Analiza el dataset y genera gráficos y análisis detallados"""
        try:
            # Cargar datos
            df = pd.read_csv(dataset_path)
            
            # Convertir fecha si existe
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'])
            
            # Análisis básico
            analysis = {
                'resumen_estadistico': df.describe(include='all').to_string(),
                'estructura_datos': f"Filas: {len(df)}, Columnas: {len(df.columns)}",
                'columnas': list(df.columns),
                'productos_unicos': df['producto'].nunique() if 'producto' in df.columns else 'N/A'
            }
            
            # Generar gráficos
            self._generate_charts(df)
            
            # Análisis por producto
            if 'producto' in df.columns and 'cantidad' in df.columns:
                ventas_por_producto = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
                analysis['top_productos'] = ventas_por_producto.head(10).to_string()
            
            # Análisis temporal si hay fecha
            if 'fecha' in df.columns and 'cantidad' in df.columns:
                ventas_por_fecha = df.groupby('fecha')['cantidad'].sum()
                analysis['tendencia_ventas'] = f"Período: {df['fecha'].min()} a {df['fecha'].max()}"
            
            return analysis
            
        except Exception as e:
            return f"Error en análisis: {str(e)}"
    
    def _generate_charts(self, df):
        """Genera gráficos de análisis"""
        plt.style.use('seaborn-v0_8')
        
        # Gráfico 1: Ventas por producto
        if 'producto' in df.columns and 'cantidad' in df.columns:
            plt.figure(figsize=(12, 6))
            ventas_producto = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
            ventas_producto.head(10).plot(kind='bar', color='skyblue')
            plt.title('Top 10 Productos por Cantidad Vendida')
            plt.xlabel('Producto')
            plt.ylabel('Cantidad Total Vendida')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{self.reports_dir}/ventas_por_producto.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Gráfico 2: Distribución de precios
        if 'precio' in df.columns:
            plt.figure(figsize=(10, 6))
            plt.hist(df['precio'], bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
            plt.title('Distribución de Precios de Productos')
            plt.xlabel('Precio')
            plt.ylabel('Frecuencia')
            plt.tight_layout()
            plt.savefig(f'{self.reports_dir}/distribucion_precios.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Gráfico 3: Tendencia temporal si hay fecha
        if 'fecha' in df.columns and 'cantidad' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'])
            ventas_diarias = df.groupby('fecha')['cantidad'].sum()
            
            plt.figure(figsize=(12, 6))
            ventas_diarias.plot(kind='line', color='green', marker='o')
            plt.title('Tendencia de Ventas Diarias')
            plt.xlabel('Fecha')
            plt.ylabel('Cantidad Total Vendida')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{self.reports_dir}/tendencia_ventas.png', dpi=300, bbox_inches='tight')
            plt.close()

class ExecutorDB:
    def save_analysis(self, instruction, summary):
        """Guardar análisis en base de datos (versión simplificada)"""
        # Por ahora solo imprime, después puedes conectar a BD
        print("💾 Análisis guardado (simulado)")
        return True