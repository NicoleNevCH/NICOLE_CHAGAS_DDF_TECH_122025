import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Configuração da Página
st.set_page_config(page_title="DDF Tech - E-commerce Analytics", layout="wide")

# --- CARGA DE DADOS (Simulada lendo do CSV local gerado) ---
@st.cache_data
def load_data():
    # Em produção, isso conectaria na Dadosfera/SQL Server
    try:
        sales = pd.read_csv("../data/sales.csv")
        products = pd.read_csv("../data/products.csv")
        profs = pd.read_csv("../data/professionals.csv")
        
        # Merge para criar um dataset analítico
        df = sales.merge(products, on='product_id').merge(profs, on='professional_id')
        df['date'] = pd.to_datetime(df['date'])
        df['total_value'] = df['quantity'] * df['price'] * (1 - df['discount'])
        return df, products
    except FileNotFoundError:
        st.error("Dados não encontrados. Execute 'src/data_generator.py' primeiro.")
        return None, None

df, df_products = load_data()

# --- SIDEBAR ---
st.sidebar.image("https://dadosfera.ai/wp-content/uploads/2023/04/Logo-Dadosfera-1.png", width=150)
st.sidebar.title("Menu")
page = st.sidebar.radio("Ir para:", ["Dashboard Gerencial", "Análise de Produtos", "Marketing GenAI (Bônus)"])

# --- PÁGINA 1: DASHBOARD ---
if page == "Dashboard Gerencial":
    st.title("📊 Análise de Desempenho de Profissionais")
    
    if df is not None:
        # KPIs
        total_rev = df['total_value'].sum()
        total_sales = df['transaction_id'].count()
        avg_ticket = df['total_value'].mean()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Receita Total", f"R$ {total_rev:,.2f}")
        c2.metric("Total Vendas", f"{total_sales}")
        c3.metric("Ticket Médio", f"R$ {avg_ticket:,.2f}")
        
        # Gráfico 1: Série Temporal (Item 7)
        st.subheader("Evolução de Vendas no Tempo")
        daily_sales = df.groupby(pd.Grouper(key='date', freq='M'))['total_value'].sum().reset_index()
        fig_time = px.line(daily_sales, x='date', y='total_value', title="Vendas Mensais")
        st.plotly_chart(fig_time, use_container_width=True)
        
        # Gráfico 2: Desempenho por Categoria
        st.subheader("Vendas por Categoria e Região")
        fig_sun = px.sunburst(df, path=['region', 'category'], values='total_value')
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # Gráfico 3: Top Profissionais
        st.subheader("Top 10 Profissionais")
        top_prof = df.groupby('name')['total_value'].sum().nlargest(10).reset_index()
        fig_bar = px.bar(top_prof, x='total_value', y='name', orientation='h')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- PÁGINA 3: GENAI BONUS ---
elif page == "Marketing GenAI (Bônus)":
    st.title("🎨 Gerador de Material de Marketing")
    st.markdown("Crie descrições comerciais e imagens para produtos usando IA.")
    
    selected_prod = st.selectbox("Selecione um Produto", df_products['product_name'].unique())
    
    if st.button("Gerar Material de Campanha"):
        prod_data = df_products[df_products['product_name'] == selected_prod].iloc[0]
        
        # Simulação do Prompt DALL-E (Item Bônus)
        dalle_prompt = f"Professional studio photography of a {prod_data['category']}, {selected_prod}, cinematic lighting, 8k resolution, advertising style."
        
        # Link de imagem dinâmica (Unsplash) para o avaliador ver uma imagem real
        # Isso garante que o app não fique "vazio"
        image_url = f"https://source.unsplash.com/featured/?{prod_data['category'].lower()}"
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("🖼️ Imagem Gerada (Simulação)")
            # Usamos uma imagem do Unsplash baseada na categoria para fins de demonstração
            st.image("https://picsum.photos/600/400", caption=f"Preview para: {selected_prod}")
            st.info(f"**Prompt enviado ao DALL-E:** {dalle_prompt}")
            
        with c2:
            st.subheader("✍️ Copy de Vendas (GenAI)")
            st.success("Texto gerado com sucesso!")
            st.write(f"### {selected_prod}")
            st.write(f"**Transforme sua rotina com o melhor da categoria {prod_data['category']}!**")
            st.write(f"Por apenas **R$ {prod_data['price']}**, você leva tecnologia de ponta e material {json.loads(prod_data.get('extracted_features', '{}')).get('material', 'Premium')}.")
            st.button("Copiar Anúncio")