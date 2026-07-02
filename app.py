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
        font-size: 16px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros Estratégicos ---
st.sidebar.title("🎛️ Filtros Avançados")
competencia = st.sidebar.selectbox("Competência", ["Julho / 2026", "Junho / 2026", "Maio / 2026"])

st.sidebar.subheader("Filtrar por Macro-Grupo")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "CRC (MONO + MULTI)", "RE", "CSF (Interno, Ajuda, Quality)"]
)

# Regra de filtragem das linhas (Clusters)
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
st.caption(f"Visão Pivotada de Metas, Pesos e Dimensões • Competência: {competencia}")
st.divider()

# ==============================================================================
# QUADRO ÚNICO: MATRIZ DE INDICADORES E PESOS (CLUSTERS EM LINHAS)
# ==============================================================================
st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)

# Estruturação dos dados com as Clusters nas Linhas e Indicadores/Pesos nas Colunas
dados_matriz_unica = {
    "Cluster": ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    "CSAT (Meta)": ["84.0% (Q1: 91%)", "Fone: 88% / Dig: 80%", "Fone: 90% / Dig: 80%", "Inativo", "Inativo", "Inativo"],
    "CSAT (Peso)": ["35%", "35%", "30%", "0%", "0%", "0%"],
    "TMA/TMT (Meta)": ["Conforme dim.", "Conforme dim.", "Conforme dim.", "Conforme dim.", "Sem Meta", "Conforme dim."],
    "TMA/TMT (Peso)": ["30%", "30%", "30%", "30%", "0%", "30%"],
    "Improcedência (Meta)": ["≤ 2 Abs", "≤ 2 Abs", "≤ 2 Abs", "-", "1 Abs", "1 Abs"],
    "Improcedência (Peso)": ["10%", "10%", "10%", "0%", "30%", "10%"],
    "Monitoria Base (Meta)": ["90%", "90%", "90%", "75%", "75%", "75%"],
    "Monitoria Q1 (Meta)": ["95%", "95%", "95%", "83%", "83%", "83%"],
    "Monitoria (Peso)": ["25%", "25%", "15%", "45%", "50%", "45%"],
    "Aderência (Meta)": ["-", "-", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "-"],
    "Aderência (Peso)": ["0%", "0%", "15%", "25%", "20%", "0%"],
    "Evasão Pausas (Meta)": ["6 a 10 Abs", "≤ 5 Abs", "-", "-", "-", "15%"],
    "Evasão Pausas (Peso)": ["0%", "0%", "0%", "0%", "0%", "15%"],
    "Treinamento (Meta)": ["95%", "95%", "95%", "-", "-", "-"]
}

df_matriz = pd.DataFrame(dados_matriz_unica)

# Aplica o filtro de linhas dinamicamente
df_matriz_filtrada = df_matriz[df_matriz["Cluster"].isin(clusters_filtrados)]

# Exibe o grande quadro unificado na tela
st.dataframe(df_matriz_filtrada, use_container_width=True, hide_index=True)


# ==============================================================================
# QUADRO INFERIOR: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA
# ==============================================================================
st.markdown('<div class="macro-title">⚖️ RESUMO: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA</div>', unsafe_allow_html=True)

dados_soma_dimensoes = {
    "Cluster": ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    "🧠 Experiência do Cliente (CSAT)": ["35%", "35%", "30%", "0%", "0%", "0%"],
    "⚡ Eficiência Operacional (TMA + Improc.)": ["40%", "40%", "40%", "30%", "30%", "40%"],
    "📋 Disciplina e Qualidade (Monit. + Escala + Pausas)": ["25%", "25%", "30%", "70%", "70%", "60%"],
    "∑ TOTAL": ["100%", "100%", "100%", "100%", "100%", "100%"]
}

df_dimensoes = pd.DataFrame(dados_soma_dimensoes)
df_dimensoes_filtrada = df_dimensoes[df_dimensoes["Cluster"].isin(clusters_filtrados)]

st.dataframe(df_dimensoes_filtrada, use_container_width=True, hide_index=True)

st.divider()


# ==============================================================================
# GRÁFICO COMPARATIVO EXECUTIVO COM RÓTULOS DE DADOS
# ==============================================================================
st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")

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

# Inclusão de text e textposition para plotar os rótulos de dados diretamente nas barras
fig.add_trace(go.Bar(
    x=clusters_filtrados, y=valores_csat, 
    name='🧠 Experiência (CSAT)', 
    marker_color='#1e3a8a',
    text=[f"{v}%" if v > 0 else "" for v in valores_csat],
    textposition='inside',
    textfont=dict(color='white', weight='bold')
))

fig.add_trace(go.Bar(
    x=clusters_filtrados, y=valores_eficiencia, 
    name='⚡ Eficiência', 
    marker_color='#475569',
    text=[f"{v}%" if v > 0 else "" for v in valores_eficiencia],
    textposition='inside',
    textfont=dict(color='white', weight='bold')
))

fig.add_trace(go.Bar(
    x=clusters_filtrados, y=valores_disciplina, 
    name='📋 Disciplina e Qualidade', 
    marker_color='#0f766e',
    text=[f"{v}%" if v > 0 else "" for v in valores_disciplina],
    textposition='inside',
    textfont=dict(color='white', weight='bold')
))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400,
    margin=dict(l=20, r=20, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0")
)

st.plotly_chart(fig, use_container_width=True)
