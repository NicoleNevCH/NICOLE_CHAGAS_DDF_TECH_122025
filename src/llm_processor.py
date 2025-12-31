import json
import pandas as pd

class FeatureExtractor:
    """
    Item 5: Transforma dados desestruturados em Features JSON.
    Utiliza uma lógica de simulação de IA para o Case.
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def extract_features_mock(self, description: str) -> str:
        """
        Extração simulada de entidades.
        """
        features = {
            "material": "Premium" if "premium" in description.lower() else "Standard",
            "warranty_months": 0,
            "dimensions": "Unknown"
        }
        
        # Correção da Sintaxe do Bloco Try/Except
        words = description.split()
        for i, word in enumerate(words):
            if "Garantia" in word:
                try:
                    # Tenta pegar o número que vem 2 palavras depois de 'Garantia'
                    features["warranty_months"] = int(words[i+2])
                except (IndexError, ValueError):
                    # Se não encontrar ou não for número, ignora
                    pass
            
        return json.dumps(features)

    def process_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        print("Iniciando enriquecimento com GenAI (Simulado)...")
        # Aplica a função em cada linha
        df['extracted_features'] = df[text_column].apply(self.extract_features_mock)
        return df