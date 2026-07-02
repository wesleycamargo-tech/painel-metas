import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página Lumia / Streamlit
st.set_page_config(
    page_title="Painel Executivo de Metas do Quadrante",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização para o padrão executivo premium
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .macro-title {
        background-color: #1e293b;
        color: white;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .badge-subtotal {
        background-color: #f1f5f9;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
        color: #475569;
        font-size: 13px;
        border-left: 4px solid #475569;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros Estratégicos e Seleções Rápidas ---
st.sidebar.title("🎛️ Filtros Avançados")
competencia = st.sidebar.selectbox("Competência", ["Julho / 2026", "Junho / 2026", "Maio / 2026"])

st.sidebar.subheader("Filtrar por Macro-Grupo")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "CRC (MONO + MULTI)", "RE", "CSF (Interno, Ajuda, Quality)"]
)

# Definição lógica dos mapeamentos com base no filtro selecionado
clusters_totais = ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
if filtro_macro == "CRC (MONO + MULTI)":
    clusters_filtrados = ["MONO", "MULTI"]
elif filtro_macro == "RE":
    clusters_filtrados = ["RE"]
elif filtro_macro == "CSF (Interno, Ajuda, Quality)":
    clusters_filtrados = ["CSF Interno", "CSF Ajuda", "CSF Quality"]
else:
    clusters_filtrados = clusters_totais

# --- TÍTULO PRINCIPAL ---
st.title("📊 Painel Executivo Unificado de Metas")
st.caption(f"Visão Consolidada de Metas, Pesos e Dimensões Operacionais • Competência: {competencia}")
st.divider()

# ==============================================================================
# BASE DE DADOS MATRIZ (Lado a lado por Cluster)
# ==============================================================================
colunas_exibicao = ["Dimensão", "Indicador"] + clusters_filtrados

# --- CATEGORIA 1: EXPERIÊNCIA DO CLIENTE ---
st.markdown('<div class="macro-title">🧠 DIMENSÃO: EXPERIÊNCIA DO CLIENTE (CSAT)</div>', unsafe_allow_html=True)

dados_csat = {
    "Dimensão": ["Experiência", "Experiência"],
    "Indicador": ["💻 CSAT Geral / Canais (Meta)", "⚖️ Peso CSAT"],
    "RE": ["84.0% (Q1: 91%)", "35%"],
    "MONO": ["Fone: 88% / Dig: 80%", "35%"],
    "MULTI": ["Fone: 90% / Dig: 80%", "30%"],
    "CSF Interno": ["Inativo", "0%"],
    "CSF Ajuda": ["Inativo", "0%"],
    "CSF Quality": ["Inativo", "0%"]
}
df_csat = pd.DataFrame(dados_csat)[colunas_exibicao]
st.dataframe(df_csat, use_container_width=True, hide_index=True)

# Pesos dinâmicos para exibir nos subtotais de resumo informativos
subtotais_csat = {"RE": 35, "MONO": 35, "MULTI": 30, "CSF Interno": 0, "CSF Ajuda": 0, "CSF Quality": 0}
texto_subtotal_csat = " | ".join([f"**{c}**: {subtotais_csat[c]}%" for c in clusters_filtrados])
st.markdown(f'<div class="badge-subtotal">∑ Subtotal de Peso da Dimensão Experiência ➜ {texto_subtotal_csat}</div>', unsafe_allow_html=True)


# --- CATEGORIA 2: EFICIÊNCIA OPERACIONAL ---
st.markdown('<div class="macro-title">⚡ DIMENSÃO: EFICIÊNCIA OPERACIONAL</div>', unsafe_allow_html=True)

dados_eficiencia = {
    "Dimensão": ["Eficiência", "Eficiência", "Eficiência", "Eficiência"],
    "Indicador": ["⏱️ TMA / TMT (Meta)", "⚖️ Peso TMA/TMT", "🚫 Improcedência Devida (Meta)", "⚖️ Peso Improcedência"],
    "RE": ["Conforme dimensionado", "30%", "≤ 2 Abs", "10%"],
    "MONO": ["Conforme dimensionado", "30%", "≤ 2 Abs", "10%"],
    "MULTI": ["Conforme dimensionado", "30%", "≤ 2 Abs", "10%"],
    "CSF Interno": ["Conforme dimensionado", "30%", "-", "0%"],
    "CSF Ajuda": ["Sem Meta", "0%", "1 Abs", "30%"],
    "CSF Quality": ["Conforme dimensionado", "30%", "1 Abs", "10%"]
}
df_efi = pd.DataFrame(dados_eficiencia)[colunas_exibicao]
st.dataframe(df_efi, use_container_width=True, hide_index=True)

subtotais_efi = {"RE": 40, "MONO": 40, "MULTI": 40, "CSF Interno": 30, "CSF Ajuda": 30, "CSF Quality": 40}
texto_subtotal_efi = " | ".join([f"**{c}**: {subtotais_efi[c]}%" for c in clusters_filtrados])
st.markdown(f'<div class="badge-subtotal">∑ Subtotal de Peso da Dimensão Eficiência ➜ {texto_subtotal_efi}</div>', unsafe_allow_html=True)


# --- CATEGORIA 3: DISCIPLINA E QUALIDADE ---
st.markdown('<div class="macro-title">📋 DIMENSÃO: DISCIPLINA E QUALIDADE</div>', unsafe_allow_html=True)

dados_disciplina = {
    "Dimensão": ["Disciplina", "Disciplina", "Disciplina", "Disciplina", "Disciplina", "Disciplina", "Disciplina", "Disciplina"],
    "Indicador": [
        "🎧 Nota de Monitoria (Meta Base)", "🎧 Nota de Monitoria (Meta Q1)", "⚖️ Peso Monitoria",
        "📅 Aderência à Escala (Meta)", "⚖️ Peso Aderência",
        "🛑 Evasão de Pausas (Meta)", "⚖️ Peso Evasão",
        "🧠 Treinamento Regulamentar"
    ],
    "RE": ["90%", "95%", "25%", "-", "0%", "6 a 10 Abs", "0%", "95%"],
    "MONO": ["90%", "95%", "25%", "-", "0%", "≤ 5 Abs", "0%", "95%"],
    "MULTI": ["90%", "95%", "15%", "88% (Q1: 93.5%)", "15%", "-", "0%", "95%"],
    "CSF Interno": ["75%", "83%", "45%", "88% (Q1: 93.5%)", "25%", "-", "0%", "-"],
    "CSF Ajuda": ["75%", "83%", "50%", "88% (Q1: 93.5%)", "20%", "-", "0%", "-"],
    "CSF Quality": ["75%", "83%", "45%", "-", "0%", "15%", "15%", "-"]
}
df_dis = pd.DataFrame(dados_disciplina)[colunas_exibicao]
st.dataframe(df_dis, use_container_width=True, hide_index=True)

subtotais_dis = {"RE": 25, "MONO": 25, "MULTI": 30, "CSF Interno": 70, "CSF Ajuda": 70, "CSF Quality": 60}
texto_subtotal_dis = " | ".join([f"**{c}**: {subtotais_dis[c]}%" for c in clusters_filtrados])
st.markdown(f'<div class="badge-subtotal">∑ Subtotal de Peso da Dimensão Disciplina ➜ {texto_subtotal_dis}</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# GRÁFICO COMPARATIVO EXECUTIVO PREMIUM (Último Campo)
# ==============================================================================
st.subheader("📊 Gráfico Comparativo: Arquitetura de Pesos por Macro-Grupo")
st.markdown("Análise de distribuição do peso total (100%) entre as frentes estratégicas de cada cluster.")

# Filtrando dados do gráfico dinamicamente com base nas colunas selecionadas
grafico_pesos = {
    "RE": [35, 40, 25],
    "MONO": [35, 40, 25],
    "MULTI": [30, 40, 30],
    "CSF Interno": [0, 30, 70],
    "CSF Ajuda": [0, 30, 70],
    "CSF Quality": [0, 40, 60]
}

valores_csat = [grafico_pesos[c][0] for c in clusters_filtrados]
valores_eficiencia = [grafico_pesos[c][1] for c in clusters_filtrados]
valores_disciplina = [grafico_pesos[c][2] for c in clusters_filtrados]

fig = go.Figure()

# Cores executivas sóbrias (Paleta Premium Navy Slate Green)
fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_csat, name='🧠 Experiência (CSAT)', marker_color='#1e3a8a'))
fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_eficiencia, name='⚡ Eficiência (TMA + Improcedência)', marker_color='#475569'))
fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_disciplina, name='📋 Disciplina (Monitoria + Escala + Pausas)', marker_color='#0f766e'))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=380,
    margin=dict(l=20, r=20, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0")
)

st.plotly_chart(fig, use_container_width=True)
