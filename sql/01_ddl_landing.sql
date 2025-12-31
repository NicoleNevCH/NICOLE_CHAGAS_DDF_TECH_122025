-- Criação do Banco de Dados (opcional, dependendo do ambiente)
-- CREATE DATABASE DADOSFERA_CASE;
-- GO

USE DADOSFERA_CASE;
GO

CREATE SCHEMA RAW;
GO

-- Tabela de Vendas Bruta
IF OBJECT_ID('RAW.Sales', 'U') IS NOT NULL DROP TABLE RAW.Sales;
CREATE TABLE RAW.Sales (
    transaction_id VARCHAR(50) NOT NULL,
    date DATETIME,
    product_id VARCHAR(50),
    professional_id VARCHAR(50),
    quantity INT,
    discount DECIMAL(10,4)
);

-- Tabela de Produtos Bruta
IF OBJECT_ID('RAW.Products', 'U') IS NOT NULL DROP TABLE RAW.Products;
CREATE TABLE RAW.Products (
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2),
    description_raw NVARCHAR(MAX)
);

-- Tabela de Profissionais Bruta
IF OBJECT_ID('RAW.Professionals', 'U') IS NOT NULL DROP TABLE RAW.Professionals;
CREATE TABLE RAW.Professionals (
    professional_id VARCHAR(50),
    name VARCHAR(255),
    email VARCHAR(150),
    role VARCHAR(50),
    hire_date DATE,
    region VARCHAR(50)
);