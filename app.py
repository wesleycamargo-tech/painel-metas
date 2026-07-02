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
    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }

    /* Estilização e Centralização Absoluta das Tabelas HTML */
    .table-executiva {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 14px;
        margin-bottom: 20px;
        background-color: white;
        border-radius: 4px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .table-executiva th {
        background-color: #f1f5f9;
        color: #1e293b;
        font-weight: 600;
        padding: 10px;
        border: 1px solid #e2e8f0;
        text-align: center !important;
    }
    .table-executiva td {
        padding: 12px 10px;
        border: 1px solid #e2e8f0;
        text-align: center !important;
        color: #0f172a; /* Garante fonte preta padrão para dados ativos e pesos */
    }
    /* Estilo exclusivo para metas zeradas/ausentes (cinza claro) */
    .meta-muted-gray {
        color: #94a3b8 !important;
        font-weight: normal !important;
    }
    /* Estilo para a linha do TMA (texto cinza corporativo) */
    .linha-tma td {
        color: #64748b !important;
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

# Regra de filtragem das frentes (Colunas)
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
# LÓGICA DE ALTERAÇÃO DE DADOS POR MÊS
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
# QUADRO 1: MATRIZ DE INDICADORES (HTML DINÂMICO COM TRATAMENTO DE CORES SELETIVAS)
# ==============================================================================
st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)

# Base de dados estruturada com as metas e pesos
dados_base = {
    "CSAT": {
        "RE": ("84.0% (Q1: 91%)", "35%"), "MONO": (meta_csat_mono, peso_csat_mono), "MULTI": ("Fone: 90% / Dig: 80%", peso_csat_multi),
        "CSF Interno": ("Inativo", "0%"), "CSF Ajuda": ("Inativo", "0%"), "CSF Quality": ("Inativo", "0%")
    },
    "TMA / TMT": {
        "RE": ("Conforme dim.", "30%"), "MONO": ("Conforme dim.", "30%"), "MULTI": ("Conforme dim.", "30%"),
        "CSF Interno": ("Conforme dim.", "30%"), "CSF Ajuda": ("-", "0%"), "CSF Quality": ("Conforme dim.", "30%")
    },
    "Improcedência Devida": {
        "RE": ("≤ 2 Abs", "10%"), "MONO": ("≤ 2 Abs", "10%"), "MULTI": ("≤ 2 Abs", "10%"),
        "CSF Interno": ("-", "0%"), "CSF Ajuda": ("1 Abs", "30%"), "CSF Quality": ("1 Abs", "10%")
    },
    "Nota de Monitoria": {
        "RE": ("90% (Q1: 95%)", "25%"), "MONO": ("90% (Q1: 95%)", "25%"), "MULTI": ("90% (Q1: 95%)", "15%"),
        "CSF Interno": ("75% (Q1: 83%)", "45%"), "CSF Ajuda": ("75% (Q1: 83%)", "50%"), "CSF Quality": ("75% (Q1: 83%)", "45%")
    },
    "Aderência à Escala": {
        "RE": ("-", "0%"), "MONO": ("-", "0%"), "MULTI": ("88% (Q1: 93.5%)", "15%"),
        "CSF Interno": ("88% (Q1: 93.5%)", "25%"), "CSF Ajuda": ("88% (Q1: 93.5%)", "20%"), "CSF Quality": ("-", "0%")
    },
    "Evasão de Pausas": {
        "RE": ("6 a 10 Abs", "0%"), "MONO": ("≤ 5 Abs", "0%"), "MULTI": ("-", "0%"),
        "CSF Interno": ("-", "0%"), "CSF Ajuda": ("-", "0%"), "CSF Quality": ("15%", "15%")
    },
    "Treinamento": {
        "RE": ("95%", "-"), "MONO": ("95%", "-"), "MULTI": ("95%", "-"),
        "CSF Interno": ("-", "-"), "CSF Ajuda": ("-", "-"), "CSF Quality": ("-", "-")
    }
}

# Criando a montagem do cabeçalho HTML multinível
html_tabela = '<table class="table-executiva"><thead>'
html_tabela += '<tr><th rowspan="2">Métrica / Indicador</th>'
for cluster in clusters_filtrados:
    html_tabela += f'<th colspan="2">{cluster}</th>'
html_tabela += '</tr><tr>'
for cluster in clusters_filtrados:
    html_tabela += '<th>Meta</th><th>Peso</th>'
html_tabela += '</tr></thead><tbody>'

icones = {"CSAT": "💻 ", "TMA / TMT": "⏱️ ", "Improcedência Devida": "🚫 ", "Nota de Monitoria": "🎧 ", "Aderência à Escala": "📅 ", "Evasão de Pausas": "🛑 ", "Treinamento": "🧠 "}

for indicador, valores in dados_base.items():
    classe_linha = ' class="linha-tma"' if indicador == "TMA / TMT" else ''
    html_tabela += f'<tr{classe_linha}><td><b>{icones[indicador]}{indicador}</b></td>'
    
    for cluster in clusters_filtrados:
        meta_val, peso_val = valores[cluster]
        
        # Regra do Peso: Sempre se mantém com cor padrão (Preto ou cinza da linha do TMA)
        celula_peso = f'<td>{peso_val}</td>'
        
        # Regra da Meta: Se estiver zerada/vazia/inativa, ganha a classe cinza claro
        if meta_val in ["-", "Inativo", "Sem Meta"]:
            celula_meta = f'<td class="meta-muted-gray">{meta_val}</td>'
        else:
            celula_meta = f'<td>{meta_val}</td>'
            
        html_tabela += celula_meta + celula_peso

html_tabela += '</tr>'
html_tabela += '</tbody></table>'
st.html(html_tabela)


# ==============================================================================
# QUADRO 2: RESUMO INVERTIDO (SOMA DOS PILARES)
# ==============================================================================
st.markdown('<div class="macro-title">⚖️ RESUMO: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA</div>', unsafe_allow_html=True)

dados_resumo = [
    ("🧠 Experiência do Cliente", [resumo_dimensoes[c][0] for c in clusters_filtrados]),
    ("⚡ Eficiência Operacional (TMA + Improc.)", [resumo_dimensoes[c][1] for c in clusters_filtrados]),
    ("📋 Disciplina e Qualidade (Monit. + Escala + Pausas)", [resumo_dimensoes[c][2] for c in clusters_filtrados])
]

html_resumo = '<table class="table-executiva"><thead><tr><th>Dimensão Estratégica / Pilar</th>'
for cluster in clusters_filtrados:
    html_resumo += f'<th>{cluster}</th>'
html_resumo += '</tr></thead><tbody>'

for pilar, valores in dados_resumo:
    html_resumo += f'<tr><td style="text-align: left !important; font-weight: bold;">{pilar}</td>'
    for val in valores:
        if val in ["0%", "-"]:
            html_resumo += f'<td class="meta-muted-gray">{val}</td>'
        else:
            html_resumo += f'<td>{val}</td>'
    html_resumo += '</tr>'

html_resumo += '</tbody></table>'
st.html(html_resumo)
st.divider()


# ==============================================================================
# GRÁFICO COMPARATIVO EXECUTIVO COM LEGENDAS AJUSTADAS
# ==============================================================================
st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")

valores_csat = [grafico_pesos[c][0] for c in clusters_filtrados]
valores_eficiencia = [grafico_pesos[c][1] for c in clusters_filtrados]
valores_disciplina = [grafico_pesos[c][2] for c in clusters_filtrados]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=clusters_filtrados, y=valores_csat, 
    name='🧠 Experiência', 
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
