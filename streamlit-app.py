import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Streamlit Demo App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Barra lateral
st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Escolha uma página:",
    ["Dashboard", "Análise de Dados", "Sobre"]
)

# Função para gerar dados aleatórios
@st.cache_data
def gerar_dados():
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'data': dates,
        'vendas': np.random.randint(100, 1000, size=100),
        'clientes': np.random.randint(10, 100, size=100),
        'categoria': np.random.choice(['A', 'B', 'C'], size=100)
    })
    return df

# Carregar dados
df = gerar_dados()

# Página do Dashboard
if opcao == "Dashboard":
    st.title("📊 Dashboard de Vendas")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Vendas", f"R$ {df['vendas'].sum():,}")
    with col2:
        st.metric("Média Diária", f"R$ {df['vendas'].mean():.2f}")
    with col3:
        st.metric("Total de Clientes", f"{df['clientes'].sum():,}")
    
    # Gráfico de vendas por tempo
    st.subheader("Vendas ao Longo do Tempo")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['data'], df['vendas'])
    ax.set_xlabel('Data')
    ax.set_ylabel('Vendas (R$)')
    ax.grid(True)
    st.pyplot(fig)
    
    # Gráfico de categoria
    st.subheader("Vendas por Categoria")
    cat_data = df.groupby('categoria')['vendas'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(cat_data['categoria'], cat_data['vendas'])
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Vendas Totais (R$)')
    st.pyplot(fig)

# Página de Análise de Dados
elif opcao == "Análise de Dados":
    st.title("🔍 Análise de Dados")
    
    # Filtros
    st.sidebar.header("Filtros")
    categorias = st.sidebar.multiselect(
        "Selecione as categorias:",
        options=df['categoria'].unique(),
        default=df['categoria'].unique()
    )
    
    min_date, max_date = st.sidebar.date_input(
        "Intervalo de datas:",
        [df['data'].min(), df['data'].max()],
        df['data'].min(),
        df['data'].max()
    )
    
    # Aplicar filtros
    filtered_df = df[
        (df['categoria'].isin(categorias)) &
        (df['data'] >= pd.Timestamp(min_date)) &
        (df['data'] <= pd.Timestamp(max_date))
    ]
    
    # Exibir dados filtrados
    st.subheader("Dados Filtrados")
    st.dataframe(filtered_df)
    
    # Estatísticas descritivas
    st.subheader("Estatísticas Descritivas")
    st.write(filtered_df.describe())
    
    # Download dos dados
    st.download_button(
        label="Download dos dados em CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='dados_filtrados.csv',
        mime='text/csv',
    )

# Página Sobre
else:
    st.title("ℹ️ Sobre este App")
    st.write("""
    # Streamlit Demo App
    
    Este é um aplicativo de demonstração desenvolvido com Streamlit para mostrar algumas das principais funcionalidades da biblioteca.
    
    ## Recursos demonstrados:
    
    * Navegação entre páginas
    * Visualização de dados com gráficos
    * Filtros interativos
    * Download de dados
    * Layout responsivo
    
    ## Como usar:
    
    1. Navegue entre as diferentes páginas usando o menu na barra lateral
    2. Experimente os filtros na página de Análise de Dados
    3. Faça o download dos dados filtrados
    
    ## Integrando com GitHub:
    
    Para integrar este app com GitHub e implementar com Streamlit Cloud:
    
    1. Crie um repositório no GitHub
    2. Faça upload deste arquivo e crie um arquivo `requirements.txt` 
    3. Conecte-se ao Streamlit Cloud e implante o app
    """)
    
    # Mostrar requisitos
    st.subheader("Requirements.txt")
    st.code("""
    streamlit==1.24.0
    pandas==2.0.3
    numpy==1.24.3
    matplotlib==3.7.2
    """)
