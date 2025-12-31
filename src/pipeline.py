import sys
import os

# Adiciona o diretório atual ao path para imports funcionarem
sys.path.append(os.getcwd())

from src.data_generator import DataGenerator
from src.quality_manager import QualityManager
from src.llm_processor import FeatureExtractor
import pandas as pd

class DataPipeline:
    """
    Pipeline Orchestrator.
    Simula um DAG do Airflow ou um Pipeline da Dadosfera.
    Etapas: Ingest -> Quality -> Process/Enrich -> Load
    """
    
    def __init__(self):
        self.generator = DataGenerator()
        self.quality = QualityManager()
        self.enricher = FeatureExtractor() # Item 5
        
    def run(self):
        print(">>> INICIANDO PIPELINE DE DADOS (ETL + IA) <<<")
        
        # Step 1: Ingestão (Geração de Sintéticos)
        print("\n[Step 1] Ingestão de Dados...")
        df_profs = self.generator.generate_professionals()
        df_prods = self.generator.generate_products()
        df_sales = self.generator.generate_sales(n_rows=100100) # >100k
        
        # Step 2: Data Quality
        print("\n[Step 2] Verificação de Qualidade...")
        checks = [
            self.quality.run_expectations(df_profs, "Professionals"),
            self.quality.run_expectations(df_prods, "Products"),
            self.quality.run_expectations(df_sales, "Sales")
        ]
        
        if not all(checks):
            print(">>> PIPELINE INTERROMPIDO POR FALHA DE QUALIDADE <<<")
            return
            
        # Step 3: Enriquecimento com IA (GenAI)
        print("\n[Step 3] Enriquecimento com GenAI (Extração de Features)...")
        # Processamos apenas uma amostra para não demorar muito na demo
        df_prods_enriched = self.enricher.process_dataframe(df_prods.head(50), text_column='description_raw')
        
        # Salvando resultado enriquecido
        df_prods_enriched.to_csv("data/products_enriched.csv", index=False)
        print("Dados enriquecidos salvos em 'data/products_enriched.csv'")
        
        print("\n>>> PIPELINE FINALIZADO COM SUCESSO <<<")
        print("Próximo passo: Execute 'streamlit run app/app.py' para visualizar.")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()