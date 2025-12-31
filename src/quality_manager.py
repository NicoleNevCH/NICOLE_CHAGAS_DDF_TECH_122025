import pandas as pd

class QualityManager:
    """
    Responsável pela validação e qualidade de dados (Data Quality).
    Pode ser expandida para usar Great Expectations.
    """
    
    def __init__(self):
        self.logs = []

    def log(self, message: str):
        print(f"[Quality Log] {message}")
        self.logs.append(message)

    def run_expectations(self, df: pd.DataFrame, dataset_name: str) -> bool:
        """
        Roda bateria de testes básicos de qualidade.
        Retorna True se passar nos critérios críticos.
        """
        self.log(f"Iniciando validação para: {dataset_name}")
        
        # 1. Check de Completude (Completeness)
        if df.empty:
            self.log(f"ERRO: Dataset {dataset_name} está vazio.")
            return False
            
        # 2. Check de Nulos (Nullity)
        null_counts = df.isnull().sum().sum()
        if null_counts > 0:
            self.log(f"ALERTA: Encontrados {null_counts} valores nulos em {dataset_name}.")
            
        # 3. Check de Unicidade (Uniqueness) - Exemplo genérico para IDs
        for col in df.columns:
            if 'id' in col.lower() and 'transaction' in col.lower():
                if df[col].duplicated().any():
                    self.log(f"ERRO CRÍTICO: IDs duplicados encontrados na coluna {col}")
                    return False

        self.log(f"Validação de {dataset_name} concluída com sucesso.")
        return True