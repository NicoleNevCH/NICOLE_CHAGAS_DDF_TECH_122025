-- QUERY 1: ANÁLISE DE SÉRIE TEMPORAL (Vendas por Mês)
-- Objetivo: Entender a sazonalidade e tendência de crescimento.
SELECT 
    d.year,
    d.month_name,
    SUM(f.total_amount) as total_revenue,
    COUNT(DISTINCT f.transaction_id) as total_transactions
FROM DW.Fact_Sales f
JOIN DW.Dim_Date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year DESC, d.month DESC;

-- QUERY 2: ANÁLISE POR CATEGORIA DE PRODUTO
-- Objetivo: Identificar quais nichos trazem maior receita.
SELECT 
    p.category,
    SUM(f.quantity) as items_sold,
    SUM(f.total_amount) as revenue,
    AVG(f.discount_amount) as avg_discount_given
FROM DW.Fact_Sales f
JOIN DW.Dim_Product p ON f.prod_sk = p.prod_sk
GROUP BY p.category
ORDER BY revenue DESC;

-- QUERY 3: RANKING DE PROFISSIONAIS (Top Performers)
-- Objetivo: Avaliação de desempenho para bonificação.
SELECT TOP 10
    prof.name,
    prof.role,
    prof.region,
    SUM(f.total_amount) as generated_revenue
FROM DW.Fact_Sales f
JOIN DW.Dim_Professional prof ON f.prof_sk = prof.prof_sk
GROUP BY prof.name, prof.role, prof.region
ORDER BY generated_revenue DESC;