import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# Configuração da página Lumia / Streamlit
st.set_page_config(
    page_title="Painel de Metas & Pesos CEX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Executiva Premium + Correção de Espaço no Topo
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    .main { background-color: #f8f9fa; }
    
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 5px;
    }
    .brand-logo {
        height: 45px;
        object-fit: contain;
    }
    .brand-title {
        font-family: sans-serif;
        color: #0f172a;
        margin: 0 !important;
        font-size: 32px;
        font-weight: 700;
    }
    
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
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }
    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }

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
        color: #0f172a !important;
    }
    .meta-muted-gray {
        color: #94a3b8 !important;
        font-weight: normal !important;
    }
    .meta-tma-gray {
        color: #64748b !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA PLANILHA (OPÇÃO SEM CREDENCIAIS) ---
# Substitua o link abaixo pelo link de compartilhamento da sua planilha do Sheets
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1e51a-1HihL2iWx-uqYRt_pZidS2jSD9T8IPtNlqbNsg/edit?usp=sharing"

# Criamos a conexão passando apenas a URL pública/link compartilhado da empresa
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR ---
st.sidebar.markdown("## 📊 Filtros Corporativos")
st.sidebar.markdown("---")

competencia = st.sidebar.selectbox(
    "Selecione a Competência:", 
    ["Julho / 2026", "Junho / 2026", "Maio / 2026"]
)

# Transforma "Julho / 2026" em "Julho_2026" para buscar o nome exato da aba no Sheets
nome_aba = competencia.replace(" / ", "_")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Segmentação Operacional")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "CRC (MONO + MULTI)", "RE", "CSF (Interno, Ajuda, Quality)"]
)

clusters_totais = ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
if filtro_macro == "CRC (MONO + MULTI)":
    clusters_filtrados = ["MONO", "MULTI"]
elif filtro_macro == "RE":
    clusters_filtrados = ["RE"]
elif filtro_macro == "CSF (Interno, Ajuda, Quality)":
    clusters_filtrados = ["CSF Interno", "CSF Ajuda", "CSF Quality"]
else:
    clusters_filtrados = clusters_totais

# --- TÍTULO DO PAINEL ---
st.markdown("""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/pt/e/e9/Logotipo_Grupo_Botic%C3%A1rio.png" class="brand-logo">
        <h1 class="brand-title">Painel de Metas & Pesos CEX</h1>
    </div>
""", unsafe_allow_html=True)

st.caption(f"Visão Dinâmica de Metas, Pesos e Dimensões Estratégicas • **Competência Vigente: {competencia}**")
st.divider()

# --- LEITURA LIVE DA PLANILHA ---
try:
    # Lendo o Sheets direto pelo link de compartilhamento (ttl="0" força atualização imediata sem cache)
    df_metas = conn.read(spreadsheet=URL_PLANILHA, worksheet=nome_aba, ttl="0")
    
    # Lógica estática para os gráficos baseada no mês para manter o visual executivo do rodapé
    if "Julho" in competencia:
        grafico_pesos = {"RE": [35, 40, 25], "MONO": [35, 40, 25], "MULTI": [30, 40, 30], "CSF Interno": [0, 30, 70], "CSF Ajuda": [0, 30, 70], "CSF Quality": [0, 40, 60]}
        resumo_dimensoes = {"RE": ["35%", "40%", "25%"], "MONO": ["35%", "40%", "25%"], "MULTI": ["30%", "40%", "30%"], "CSF Interno": ["0%", "30%", "70%"], "CSF Ajuda": ["0%", "30%", "70%"], "CSF Quality": ["0%", "40%", "60%"]}
    elif "Junho" in competencia:
        grafico_pesos = {"RE": [35, 45, 20], "MONO": [40, 40, 20], "MULTI": [35, 40, 25], "CSF Interno": [0, 35, 65], "CSF Ajuda": [0, 25, 75], "CSF Quality": [0, 45, 55]}
        resumo_dimensoes = {"RE": ["35%", "45%", "20%"], "MONO": ["40%", "40%", "20%"], "MULTI": ["35%", "40%", "25%"], "CSF Interno": ["0%", "35%", "65%"], "CSF Ajuda": ["0%", "25%", "75%"], "CSF Quality": ["0%", "45%", "55%"]}
    else:
        grafico_pesos = {"RE": [40, 40, 20], "MONO": [40, 40, 20], "MULTI": [40, 35, 25], "CSF Interno": [0, 40, 60], "CSF Ajuda": [0, 40, 60], "CSF Quality": [0, 50, 50]}
        resumo_dimensoes = {"RE": ["40%", "40%", "20%"], "MONO": ["40%", "40%", "20%"], "MULTI": ["40%", "35%", "25%"], "CSF Interno": ["0%", "40%", "60%"], "CSF Ajuda": ["0%", "40%", "60%"], "CSF Quality": ["0%", "50%", "50%"]}

    # ==============================================================================
    # QUADRO 1: MATRIZ DE INDICADORES (CONSTRUÍDA LIVE DO GOOGLE SHEETS)
    # ==============================================================================
    st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)
    
    html_tabela = '<table class="table-executiva"><thead>'
    html_tabela += '<tr><th rowspan="2">Métrica / Indicador</th>'
    for cluster in clusters_filtrados:
        html_tabela += f'<th colspan="2">{cluster}</th>'
    html_tabela += '</tr><tr>'
    for cluster in clusters_filtrados:
        html_tabela += '<th>Meta</th><th>Peso</th>'
    html_tabela += '</tr></thead><tbody>'

    icones = {"CSAT": "💻 ", "TMA / TMT": "⏱️ ", "Improcedência Devida": "🚫 ", "Nota de Monitoria": "🎧 ", "Aderência à Escala": "📅 ", "Evasão de Pausas": "🛑 ", "Treinamento": "🧠 "}

    # Varre as linhas da sua planilha viva do Sheets
    for _, row in df_metas.iterrows():
        indicador = str(row['Indicador'])
        icone = icones.get(indicador, "🔹 ")
        html_tabela += f'<tr><td><b>{icone}{indicador}</b></td>'
        
        for cluster in clusters_filtrados:
            meta_val = str(row[f'{cluster}_Meta'])
            peso_val = str(row[f'{cluster}_Peso'])
            
            celula_peso = f'<td>{peso_val}</td>'
            
            if meta_val in ["-", "Inativo", "Sem Meta", "nan"]:
                meta_val = "-" if meta_val == "nan" else meta_val
                celula_meta = f'<td class="meta-muted-gray">{meta_val}</td>'
            elif indicador == "TMA / TMT":
                celula_meta = f'<td class="meta-tma-gray">{meta_val}</td>'
            else:
                celula_meta = f'<td>{meta_val}</td>'
                
            html_tabela += celula_meta + celula_peso
        html_tabela += '</tr>'
        
    html_tabela += '</tbody></table>'
    st.html(html_tabela)

    # ==============================================================================
    # QUADRO 2: RESUMO INVERTIDO
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
    # GRÁFICO COMPARATIVO
    # ==============================================================================
    st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")

    valores_csat = [grafico_pesos[c][0] for c in clusters_filtrados]
    valores_eficiencia = [grafico_pesos[c][1] for c in clusters_filtrados]
    valores_disciplina = [grafico_pesos[c][2] for c in clusters_filtrados]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_csat, name='🧠 Experiência', marker_color='#1e3a8a', text=[f"{v}%" if v > 0 else "" for v in valores_csat], textposition='inside', textfont=dict(color='white', weight='bold')))
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_eficiencia, name='⚡ Eficiência', marker_color='#475569', text=[f"{v}%" if v > 0 else "" for v in valores_eficiencia], textposition='inside', textfont=dict(color='white', weight='bold')))
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_disciplina, name='📋 Disciplina e Qualidade', marker_color='#0f766e', text=[f"{v}%" if v > 0 else "" for v in valores_disciplina], textposition='inside', textfont=dict(color='white', weight='bold')))

    fig.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=20, r=20, t=10, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5), yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0"))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning("Aguardando configuração final do link do Sheets.")
    st.info("Substitua 'URL_DA_SUA_PLANILHA_AQUI' no código do GitHub pelo link real do seu Google Sheets.")
