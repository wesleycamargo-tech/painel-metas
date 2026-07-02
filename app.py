import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página Lumia / Streamlit
st.set_page_config(
    page_title="Painel Executivo de Metas - Competência Julho 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização customizada para visual executivo (Clean & Modern)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #007bff;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 14px; color: #6c757d; font-weight: bold; }
    .metric-value { font-size: 24px; color: #212529; font-weight: bold; }
    .quadrant-box {
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros e Navegação ---
st.sidebar.image("https://img.icons8.com/fluent/96/000000/dashboard.png", width=60)
st.sidebar.title("Filtros Estratégicos")
competencia = st.sidebar.selectbox("Competência", ["Julho / 2026", "Junho / 2026", "Maio / 2026"])
cluster_selecionado = st.sidebar.multiselect(
    "Filtrar por Cluster", 
    ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    default=["RE", "MONO", "MULTI"]
)

# --- TÍTULO PRINCIPAL ---
st.title("📊 Painel Executivo de Metas do Quadrante")
st.caption(f"Visualização dinâmica de indicadores e metas operacionais • Competência: {competencia}")
st.hr()

# --- SEÇÃO 1: STATUS E QUADRANTES ---
st.subheader("🎯 Metas e Enquadramento de Performance")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="quadrant-box" style="background-color: #28a745;">Q1 - Tudo mais que beleza!<br>&gt; 110%</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="quadrant-box" style="background-color: #17a2b8;">Q2 - Tudo beleza<br>&ge; 100%</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="quadrant-box" style="background-color: #ffc107; color: #212529;">Q3 - Beleza em construção<br>80% a 99%</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="quadrant-box" style="background-color: #dc3545;">Q4 - Resgatando a essência<br>&lt; 80%</div>', unsafe_allow_html=True)

st.write("")

# --- SEÇÃO 2: MATRIZ DE METAS DINÂMICA ---
data_metas = {
    "Cluster": ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    "CSAT (Meta Base)": ["84.0%", "Fone: 88% / Dig: 80%", "Fone: 90% / Dig: 80%", "Inativo", "Inativo", "Inativo"],
    "CSAT (Q1)": ["91.0%", "Fone: 94% / Dig: 88%", "Fone: 94% / Dig: 84%", "-", "-", "-"],
    "Monitoria (Base)": ["90%", "90%", "90%", "75%", "75%", "75%"],
    "Monitoria (Q1)": ["95%", "95%", "95%", "83%", "83%", "83%"],
    "Improcedência Max": ["≤ 2 Abs", "≤ 2 Abs", "≤ 2 Abs", "-", "1 Abs", "1 Abs"],
    "Aderência Escala": ["-", "-", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "-"],
    "Evasão de Pausas": ["6 a 10 Abs", "≤ 5 Abs", "-", "-", "-", "-"]
}
df_metas = pd.DataFrame(data_metas)

# Filtragem dinâmica via sidebar
if cluster_selecionado:
    df_metas = df_metas[df_metas["Cluster"].isin(cluster_selecionado)]

st.markdown("### 📋 Matriz de Metas Homologadas")
st.dataframe(df_metas, use_container_width=True)

st.hr()

# --- SEÇÃO 3: TRANSIÇÃO DE PESOS (GRÁFICO INTERATIVO) ---
st.subheader("🔄 Impacto da Redução de Peso do CSAT")

col_graph, col_insights = st.columns([2, 1])

with col_graph:
    # Dados de transição
    indicadores = ['CSAT', 'TMA / TMT', 'Monitoria', 'Improcedência']
    pesos_base = [35, 30, 25, 10]
    pesos_sem_csat = [0, 46, 38, 15]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=indicadores, y=pesos_base,
        name='Peso Base (Com CSAT)',
        marker_color='#cbd5e1'
    ))
    fig.add_trace(go.Bar(
        x=indicadores, y=pesos_sem_csat,
        name='Proporção Sem CSAT (Atual)',
        marker_color='#007bff'
    ))

    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_insights:
    st.markdown("#### ⚠️ Alertas da Liderança")
    st.markdown(
        """
        * 🎯 **Volumetria do TMA/TMT:** Sem o CSAT, o peso do TMA saltou para **46%**. É o indicador mais crítico do mês.
        * 🕒 **Aderência à Escala:** Patamar de **93,5%** necessário para atingir a faixa ouro (Q1).
        * 🛑 **Evasão de Pausas:** RE e MONO possuem teto rígido de **5 ocorrências** para sustentar a nota máxima.
        """
    )
