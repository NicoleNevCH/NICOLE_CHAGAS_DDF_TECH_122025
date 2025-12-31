-- Script T-SQL para SQL Server
-- Criação do Schema e Tabelas

CREATE SCHEMA RAW;
GO
CREATE SCHEMA DW;
GO

-----------------------------------------------------------
-- 1. CAMADA LANDING (RAW) - Onde os CSVs seriam carregados
-----------------------------------------------------------

CREATE TABLE RAW.Professionals (
    professional_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(100),
    hire_date DATE,
    region VARCHAR(50)
);

CREATE TABLE RAW.Products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    description_raw NVARCHAR(MAX) -- Texto desestruturado
);

CREATE TABLE RAW.Sales (
    transaction_id VARCHAR(50) PRIMARY KEY,
    date DATETIME,
    product_id VARCHAR(50),
    professional_id VARCHAR(50),
    quantity INT,
    discount DECIMAL(5, 2)
);
GO

-----------------------------------------------------------
-- 2. CAMADA DW (MODELAGEM DIMENSIONAL / KIMBALL)
-- Item 6: Modelagem Star Schema para análise de performance
-----------------------------------------------------------

-- Dimensão Profissional (SCD Tipo 1 para simplificação do case)
CREATE TABLE DW.Dim_Professional (
    prof_sk INT IDENTITY(1,1) PRIMARY KEY,
    professional_id VARCHAR(50),
    name VARCHAR(255),
    role VARCHAR(100),
    region VARCHAR(50)
);

-- Dimensão Produto
CREATE TABLE DW.Dim_Product (
    prod_sk INT IDENTITY(1,1) PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    current_price DECIMAL(10, 2),
    features_json NVARCHAR(MAX) -- Campo para armazenar features da IA (Item 5)
);

-- Dimensão Tempo
CREATE TABLE DW.Dim_Date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    quarter INT,
    month_name VARCHAR(20)
);

-- Fato Vendas
CREATE TABLE DW.Fact_Sales (
    sale_sk BIGINT IDENTITY(1,1) PRIMARY KEY,
    transaction_id VARCHAR(50),
    date_key INT,
    prof_sk INT,
    prod_sk INT,
    quantity INT,
    unit_price DECIMAL(10, 2),
    discount_amount DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (date_key) REFERENCES DW.Dim_Date(date_key),
    FOREIGN KEY (prof_sk) REFERENCES DW.Dim_Professional(prof_sk),
    FOREIGN KEY (prod_sk) REFERENCES DW.Dim_Product(prod_sk)
);
GO

-- Exemplo de Procedure de Carga (ETL Simples em T-SQL)
CREATE PROCEDURE DW.sp_Load_Fact_Sales
AS
BEGIN
    INSERT INTO DW.Fact_Sales (transaction_id, date_key, prof_sk, prod_sk, quantity, unit_price, discount_amount, total_amount)
    SELECT 
        s.transaction_id,
        CAST(FORMAT(s.date, 'yyyyMMdd') AS INT) as date_key,
        p.prof_sk,
        pr.prod_sk,
        s.quantity,
        raw_p.price,
        (s.quantity * raw_p.price * s.discount),
        (s.quantity * raw_p.price * (1 - s.discount))
    FROM RAW.Sales s
    JOIN RAW.Products raw_p ON s.product_id = raw_p.product_id
    LEFT JOIN DW.Dim_Professional p ON s.professional_id = p.professional_id
    LEFT JOIN DW.Dim_Product pr ON s.product_id = pr.product_id;
END;
GO