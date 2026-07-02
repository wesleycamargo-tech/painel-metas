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

# Estilização Executiva Premium + Correção de Espaço no Topo
st.markdown("""
    <style>
    /* Remove o espaço em branco gigante no topo da página */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    .main { background-color: #f8f9fa; }
    
    /* Títulos de seções elegantes */
    .macro-title {
        background-color: #1e293b;
        color: white;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 15px;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
    /* Customização para deixar a Sidebar Executiva */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important; /* Dark navy */
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }
    /* Deixar os botões de rádio mais elegantes na sidebar */
    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros Estratégicos Executivos ---
st.sidebar.markdown("## 📊 Filtros Corporativos")
st.sidebar.markdown("---")

competencia = st.sidebar.selectbox(
    "Selecione a Competência:", 
    ["Julho / 2026", "Junho / 2026", "Maio / 2026"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Segmentação Operacional")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "CRC (MONO + MULTI)", "RE", "CSF (Interno, Ajuda, Quality)"]
)

# Regra de filtragem das frentes
clusters_totais = ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
if filtro_macro == "CRC (MONO + MULTI)":
    clusters_filtrados = ["MONO", "MULTI"]
elif filtro_macro == "RE":
    clusters_filtrados = ["RE"]
elif filtro_macro == "CSF (Interno, Ajuda, Quality)":
    clusters_filtrados = ["CSF Interno", "CSF Ajuda", "CSF Quality"]
else:
    clusters_filtrados = clusters_totais

# --- TÍTULO PRINCIPAL (COLADO NO TOPO) ---
st.title("📊 Painel Executivo Unificado de Metas")
st.caption(f"Visão Dinâmica de Metas, Pesos e Dimensões Estratégicas • **Competência Vigente: {competencia}**")
st.divider()

# ==============================================================================
# LÓGICA DE ALTERAÇÃO DE DADOS POR MÊS (CORREÇÃO DO FILTRO)
# ==============================================================================
if "Julho" in competencia:
    peso_csat_mono, peso_csat_multi = "35%", "30%"
    meta_csat_mono = "Fone: 88% / Dig: 80%"
    grafico_pesos = {
        "RE": [35, 40, 25], "MONO": [35, 40, 25], "MULTI": [30, 40, 30],
        "CSF Interno": [0, 30, 70], "CSF Ajuda": [0, 30, 70], "CSF Quality": [0, 40, 60]
    }
    resumo_dimensoes = {
        "RE": ["35%", "40%", "25%"], "MONO": ["35%", "40%", "25%"], "MULTI": ["30%", "40%", "30%"],
        "CSF Interno": ["0%", "30%", "70%"], "CSF Ajuda": ["0%", "30%", "70%"], "CSF Quality": ["0%", "40%", "60%"]
    }
elif "Junho" in competencia:
    # Simulação de histórico de Junho
    peso_csat_mono, peso_csat_multi = "40%", "35%"
    meta_csat_mono = "Fone: 87% / Dig: 80%"
    grafico_pesos = {
        "RE": [35, 45, 20], "MONO": [40, 40, 20], "MULTI": [35, 40, 25],
        "CSF Interno": [0, 35, 65], "CSF Ajuda": [0, 25, 75], "CSF Quality": [0, 45, 55]
    }
    resumo_dimensoes = {
        "RE": ["35%", "45%", "20%"], "MONO": ["40%", "40%", "20%"], "MULTI": ["35%", "40%", "25%"],
        "CSF Interno": ["0%", "35%", "65%"], "CSF Ajuda": ["0%", "25%", "75%"], "CSF Quality": ["0%", "45%", "55%"]
    }
else:
    # Simulação de histórico de Maio
    peso_csat_mono, peso_csat_multi = "40%", "40%"
    meta_csat_mono = "Geral: 85%"
    grafico_pesos = {
        "RE": [40, 40, 20], "MONO": [40, 40, 20], "MULTI": [40, 35, 25],
        "CSF Interno": [0, 40, 60], "CSF Ajuda": [0, 40, 60], "CSF Quality": [0, 50, 50]
    }
    resumo_dimensoes = {
        "RE": ["40%", "40%", "20%"], "MONO": ["40%", "40%", "20%"], "MULTI": ["40%", "35%", "25%"],
        "CSF Interno": ["0%", "40%", "60%"], "CSF Ajuda": ["0%", "40%", "60%"], "CSF Quality": ["0%", "50%", "50%"]
    }

# ==============================================================================
# QUADRO 1: MATRIZ DE INDICADORES E PESOS (CABEÇALHOS SEPARADOS)
# ==============================================================================
st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)

dados_matriz_unica = {
    "Cluster": ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"],
    "CSAT_Meta": ["84.0% (Q1: 91%)", meta_csat_mono, "Fone: 90% / Dig: 80%", "Inativo", "Inativo", "Inativo"],
    "CSAT_Peso": ["35%", peso_csat_mono, peso_csat_multi, "0%", "0%", "0%"],
    "TMA_Meta": ["Conforme dim.", "Conforme dim.", "Conforme dim.", "Conforme dim.", "Sem Meta", "Conforme dim."],
    "TMA_Peso": ["30%", "30%", "30%", "30%", "0%", "30%"],
    "Improc_Meta": ["≤ 2 Abs", "≤ 2 Abs", "≤ 2 Abs", "-", "1 Abs", "1 Abs"],
    "Improc_Peso": ["10%", "10%", "10%", "0%", "30%", "10%"],
    "Monit_Base": ["90%", "90%", "90%", "75%", "75%", "75%"],
    "Monit_Q1": ["95%", "95%", "95%", "83%", "83%", "83%"],
    "Monit_Peso": ["25%", "25%", "15%", "45%", "50%", "45%"],
    "Ader_Meta": ["-", "-", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "88% (Q1: 93.5%)", "-"],
    "Ader_Peso": ["0%", "0%", "15%", "25%", "20%", "0%"],
    "Evasao_Meta": ["6 a 10 Abs", "≤ 5 Abs", "-", "-", "-", "15%"],
    "Evasao_Peso": ["0%", "0%", "0%", "0%", "0%", "15%"]
}

df_matriz = pd.DataFrame(dados_matriz_unica)
df_matriz_filtrada = df_matriz[df_matriz["Cluster"].isin(clusters_filtrados)]

# Renomeando colunas via column_config para criar o efeito "Indicador: Meta | Peso" separado por colunas limpas
st.dataframe(
    df_matriz_filtrada, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "CSAT_Meta": "CSAT: Meta", "CSAT_Peso": "CSAT: Peso",
        "TMA_Meta": "TMA/TMT: Meta", "TMA_Peso": "TMA/TMT: Peso",
        "Improc_Meta": "Improcedência: Meta", "Improc_Peso": "Improcedência: Peso",
        "Monit_Base": "Monitoria: Base", "Monit_Q1": "Monitoria: Q1", "Monit_Peso": "Monitoria: Peso",
        "Ader_Meta": "Aderência: Meta", "Ader_Peso": "Aderência: Peso",
        "Evasao_Meta": "Evasão: Meta", "Evasao_Peso": "Evasão: Peso"
    }
)

# ==============================================================================
# QUADRO 2: RESUMO INVERTIDO (PILARES EM LINHAS, CLUSTERS EM COLUNAS)
# ==============================================================================
st.markdown('<div class="macro-title">⚖️ RESUMO: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA</div>', unsafe_allow_html=True)

dados_soma_dimensoes = {
    "Dimensão Estratégica / Pilar": [
        "🧠 Experiência do Cliente (CSAT)",
        "⚡ Eficiência Operacional (TMA + Improc.)",
        "📋 Disciplina e Qualidade (Monit. + Escala + Pausas)",
        "∑ TOTAL"
    ],
    "RE": [resumo_dimensoes["RE"][0], resumo_dimensoes["RE"][1], resumo_dimensoes["RE"][2], "100%"],
    "MONO": [resumo_dimensoes["MONO"][0], resumo_dimensoes["MONO"][1], resumo_dimensoes["MONO"][2], "100%"],
    "MULTI": [resumo_dimensoes["MULTI"][0], resumo_dimensoes["MULTI"][1], resumo_dimensoes["MULTI"][2], "100%"],
    "CSF Interno": [resumo_dimensoes["CSF Interno"][0], resumo_dimensoes["CSF Interno"][1], resumo_dimensoes["CSF Interno"][2], "100%"],
    "CSF Ajuda": [resumo_dimensoes["CSF Ajuda"][0], resumo_dimensoes["CSF Ajuda"][1], resumo_dimensoes["CSF Ajuda"][2], "100%"],
    "CSF Quality": [resumo_dimensoes["CSF Quality"][0], resumo_dimensoes["CSF Quality"][1], resumo_dimensoes["CSF Quality"][2], "100%"]
}

colunas_dimensoes_exibicao = ["Dimensão Estratégica / Pilar"] + clusters_filtrados
df_dimensoes = pd.DataFrame(dados_soma_dimensoes)[colunas_dimensoes_exibicao]

st.dataframe(df_dimensoes, use_container_width=True, hide_index=True)
st.divider()

# ==============================================================================
# GRÁFICO COMPARATIVO EXECUTIVO COM RÓTULOS DINÂMICOS
# ==============================================================================
st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")

valores_csat = [grafico_pesos[c][0] for c in clusters_filtrados]
valores_eficiencia = [grafico_pesos[c][1] for c in clusters_filtrados]
valores_disciplina = [grafico_pesos[c][2] for c in clusters_filtrados]

fig = go.Figure()

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
    height=380,
    margin=dict(l=20, r=20, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0")
)

st.plotly_chart(fig, use_container_width=True)
