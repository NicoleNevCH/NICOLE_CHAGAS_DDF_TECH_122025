import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from typing import List, Dict
from datetime import datetime, timedelta

# Configurações iniciais
fake = Faker('pt_BR')
Faker.seed(42)

class DataGenerator:
    """
    Classe responsável pela geração de dados sintéticos para o case de E-commerce.
    Segue princípios SOLID, focando em responsabilidade única de geração.
    """
    
    def __init__(self, output_path: str = "data"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
        self.products: List[Dict] = []
        self.professionals: List[Dict] = []
        self.transactions: List[Dict] = []

    def generate_professionals(self, n: int = 50) -> pd.DataFrame:
        """Gera dados de profissionais (Vendedores/Gerentes)."""
        print(f"Gerando {n} profissionais...")
        roles = ['Vendedor Júnior', 'Vendedor Pleno', 'Vendedor Sênior', 'Gerente de Contas']
        
        data = []
        for _ in range(n):
            item = {
                'professional_id': fake.uuid4(),
                'name': fake.name(),
                'email': fake.company_email(),
                'role': random.choice(roles),
                'hire_date': fake.date_between(start_date='-5y', end_date='today'),
                'region': fake.state_abbr()
            }
            data.append(item)
        
        self.professionals = data
        df = pd.DataFrame(data)
        df.to_csv(f"{self.output_path}/professionals.csv", index=False)
        return df

    def generate_products(self, n: int = 200) -> pd.DataFrame:
        """Gera dados de produtos com descrições ricas para uso de LLM posteriormente."""
        print(f"Gerando {n} produtos...")
        categories = ['Eletrônicos', 'Móveis', 'Roupas', 'Beleza', 'Esportes']
        
        data = []
        for _ in range(n):
            cat = random.choice(categories)
            item = {
                'product_id': fake.uuid4(),
                'product_name': f"{cat} - {fake.word().capitalize()} {fake.color_name()}",
                'category': cat,
                'price': round(random.uniform(50.0, 5000.0), 2),
                # Descrição não estruturada propositalmente para o Item 5
                'description_raw': f"Incrível {fake.word()} feito de material premium. Ideal para {fake.job()}. Cores disponíveis: {fake.color_name()}. Garantia de {random.randint(1,12)} meses. Dimensões: {random.randint(10,100)}cm. Peso: {random.randint(1,10)}kg."
            }
            data.append(item)
        
        self.products = data
        df = pd.DataFrame(data)
        df.to_csv(f"{self.output_path}/products.csv", index=False)
        return df

    def generate_sales(self, n_rows: int = 100500) -> pd.DataFrame:
        """
        Gera tabela de fatos de vendas.
        Requisito: > 100.000 registros.
        """
        print(f"Gerando {n_rows} transações de vendas (Isso pode levar um momento)...")
        
        if not self.products or not self.professionals:
            raise ValueError("Gere produtos e profissionais antes das vendas.")

        prod_ids = [p['product_id'] for p in self.products]
        prof_ids = [p['professional_id'] for p in self.professionals]
        
        # Otimização: Gerar em batch usando numpy para performance
        dates = [fake.date_time_between(start_date='-2y', end_date='now') for _ in range(n_rows)]
        
        data = {
            'transaction_id': [fake.uuid4() for _ in range(n_rows)],
            'date': dates,
            'product_id': np.random.choice(prod_ids, n_rows),
            'professional_id': np.random.choice(prof_ids, n_rows),
            'quantity': np.random.randint(1, 10, n_rows),
            'discount': np.round(np.random.uniform(0, 0.2, n_rows), 2)
        }
        
        df = pd.DataFrame(data)
        # Salva em CSV
        df.to_csv(f"{self.output_path}/sales.csv", index=False)
        print("Geração concluída.")
        return df

if __name__ == "__main__":
    gen = DataGenerator()
    gen.generate_professionals(50)
    gen.generate_products(200)
    gen.generate_sales(105000) # > 100k registros conforme solicitado