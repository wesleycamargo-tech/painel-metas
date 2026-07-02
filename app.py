import streamlit as st
import pandas as pd

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
    .quadrant-box {
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        color: white;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros ---
st.sidebar.title("Filtros Estratégicos")
competencia = st.sidebar.selectbox("Competência", ["Julho / 2026", "Junho / 2026", "Maio / 2026"])
cluster_selecionado = st.sidebar.multiselect(
    "Filtrar por Cluster", 
    ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    default=["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
)

# --- TÍTULO PRINCIPAL ---
st.title("📊 Painel Executivo de Metas do Quadrante")
st.caption(f"Visualização dinâmica de indicadores e metas operacionais • Competência: {competencia}")
st.divider()

# --- SEÇÃO 1: STATUS E QUADRANTES ---
st.subheader("🎯 Enquadramento de Performance")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="quadrant-box" style="background-color: #28a745;">Q1 - Tudo mais que beleza!<br>&gt; 110%</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="quadrant-box" style="background-color: #17a2b8;">Q2 - Tudo beleza<br>&ge; 100%</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="quadrant-box" style="background-color: #ffc107; color: #212529;">Q3 - Beleza em construção<br>80% a 99%</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="quadrant-box" style="background-color: #dc3545;">Q4 - Resgatando a essência<br>&lt; 80%</div>', unsafe_allow_html=True)

st.divider()

# --- SEÇÃO 2: MATRIZ DE METAS DINÂMICA ---
st.subheader("📋 Matriz de Metas Homologadas")

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

# Filtragem dinâmica de Metas via sidebar
if cluster_selecionado:
    df_metas = df_metas[df_metas["Cluster"].isin(cluster_selecionado)]

# hide_index=True remove a primeira coluna numérica automática
st.dataframe(df_metas, use_container_width=True, hide_index=True)

st.divider()

# --- SEÇÃO 3: NOVA MATRIZ DE PESOS POR CLUSTER ---
st.subheader("⚖️ Ponderação e Pesos dos Indicadores por Cluster")
st.markdown("Detalhamento da distribuição de peso de cada indicador na nota final do Quadrante.")

data_pesos = {
    "Cluster": ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    "CSAT": ["35%", "35%", "30%", "0% (Inativo)", "0% (Inativo)", "0% (Inativo)"],
    "TMA / TMT": ["30%", "30%", "30%", "30%", "0% (Sem Meta)", "30%"],
    "Nota de Monitoria": ["25%", "25%", "15%", "45%", "50%", "45%"],
    "Improcedência Devida": ["10%", "10%", "10%", "0% (Inativo)", "30%", "10%"],
    "Aderência a Escala": ["0%", "0%", "15%", "25%", "20%", "0%"],
    "Evasão de Pausas": ["0%", "0%", "0%", "0%", "0%", "15%"]
}
df_pesos = pd.DataFrame(data_pesos)

# Filtragem dinâmica de Pesos via sidebar
if cluster_selecionado:
    df_pesos = df_pesos[df_pesos["Cluster"].isin(cluster_selecionado)]

# hide_index=True aplicado também na tabela de pesos
st.dataframe(df_pesos, use_container_width=True, hide_index=True)

st.divider()

# --- SEÇÃO 4: ALERTAS OPERACIONAIS ---
st.markdown("#### ⚠️ Alertas e Direcionamentos Críticos")
st.markdown(
    """
    * 🎯 **Impacto do TMA:** Nos clusters onde o **CSAT está Inativo (CSFs)**, o peso operacional migra severamente para a eficiência de tempo e Monitoria técnica.
    * 🕒 **Gargalo de Escala:** Os clusters **MULTI, CSF Interno e CSF Ajuda** possuem forte impacto de *Aderência a Escala* na nota final, variando de 15% a 25% do peso total.
    * 🛑 **Atenção à Evasão:** O indicador de *Evasão de Pausas* agora impacta diretamente com **15% de peso** o resultado do cluster **CSF Quality**.
    """
)
