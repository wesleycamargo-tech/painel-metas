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

# Estilização para o padrão executivo e caixas de categorias
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .category-header {
        background-color: #007bff;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    .total-box {
        background-color: #e2e8f0;
        padding: 8px;
        border-radius: 4px;
        font-weight: bold;
        color: #1e293b;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Filtros ---
st.sidebar.title("Filtros Estratégicos")
competencia = st.sidebar.selectbox("Competência", ["Julho / 2026", "Junho / 2026", "Maio / 2026"])
cluster_selecionado = st.sidebar.selectbox(
    "Visualizar Detalhes do Cluster:", 
    ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
)

# --- TÍTULO PRINCIPAL ---
st.title("📊 Painel Executivo de Metas do Quadrante")
st.caption(f"Visualização por Dimensões Estratégicas • Competência: {competencia}")
st.divider()

st.subheader(f"🔍 Matriz de Performance: Cluster {cluster_selecionado}")

# --- BANCO DE DADOS COMPLETO (METAS E PESOS VIGENTES POR CLUSTER) ---
# Dicionário estruturado para buscar dados dinamicamente com base no cluster selecionado
dados_operacionais = {
    "RE": {
        "csat_meta": "84.0% (Q1: 91%)", "csat_peso": 35,
        "tma_meta": "Conforme dimensionado", "tma_peso": 30,
        "improc_meta": "≤ 2 Abs", "improc_peso": 10,
        "ader_meta": "-", "ader_peso": 0,
        "monit_meta": "90% (Q1: 95%)", "monit_peso": 25,
        "trein_meta": "95%", "trein_peso": 0,
        "evasao_meta": "6 a 10 Abs", "evasao_peso": 0
    },
    "MONO": {
        "csat_meta": "Fone: 88% / Dig: 80%", "csat_peso": 35,
        "tma_meta": "Conforme dimensionado", "tma_peso": 30,
        "improc_meta": "≤ 2 Abs", "improc_peso": 10,
        "ader_meta": "-", "ader_peso": 0,
        "monit_meta": "90% (Q1: 95%)", "monit_peso": 25,
        "trein_meta": "95%", "trein_peso": 0,
        "evasao_meta": "≤ 5 Abs", "evasao_peso": 0
    },
    "MULTI": {
        "csat_meta": "Fone: 90% / Dig: 80%", "csat_peso": 30,
        "tma_meta": "Conforme dimensionado", "tma_peso": 30,
        "improc_meta": "≤ 2 Abs", "improc_peso": 10,
        "ader_meta": "88% (Q1: 93.5%)", "ader_peso": 15,
        "monit_meta": "90% (Q1: 95%)", "monit_peso": 15,
        "trein_meta": "95%", "trein_peso": 0,
        "evasao_meta": "-", "evasao_peso": 0
    },
    "CSF Interno": {
        "csat_meta": "Inativo", "csat_peso": 0,
        "tma_meta": "Conforme dimensionado", "tma_peso": 30,
        "improc_meta": "-", "improc_peso": 0,
        "ader_meta": "88% (Q1: 93.5%)", "ader_peso": 25,
        "monit_meta": "75% (Q1: 83%)", "monit_peso": 45,
        "trein_meta": "-", "trein_peso": 0,
        "evasao_meta": "-", "evasao_peso": 0
    },
    "CSF Ajuda": {
        "csat_meta": "Inativo", "csat_peso": 0,
        "tma_meta": "Sem Meta", "tma_peso": 0,
        "improc_meta": "1 Abs", "improc_peso": 30,
        "ader_meta": "88% (Q1: 93.5%)", "ader_peso": 20,
        "monit_meta": "75% (Q1: 83%)", "monit_peso": 50,
        "trein_meta": "-", "trein_peso": 0,
        "evasao_meta": "-", "evasao_peso": 0
    },
    "CSF Quality": {
        "csat_meta": "Inativo", "csat_peso": 0,
        "tma_meta": "Conforme dimensionado", "tma_peso": 30,
        "improc_meta": "1 Abs", "improc_peso": 10,
        "ader_meta": "-", "ader_peso": 0,
        "monit_meta": "75% (Q1: 83%)", "monit_peso": 45,
        "trein_meta": "-", "trein_peso": 0,
        "evasao_meta": "15%", "evasao_peso": 15
    }
}

cluster = dados_operacionais[cluster_selecionado]

# --- CATEGORIA 1: EXPERIÊNCIA DO CLIENTE ---
st.markdown('<div class="category-header">🧠 Experiência do Cliente (CSAT)</div>', unsafe_allow_html=True)
df_exp = pd.DataFrame({
    "Indicador": ["💻 CSAT Geral / Canais"],
    "Meta Homologada": [cluster["csat_meta"]],
    "Peso na Nota": [f"{cluster['csat_peso']}%"]
})
st.dataframe(df_exp, use_container_width=True, hide_index=True)
st.markdown(f'<div class="total-box">Subtotal Peso Experiência: {cluster["csat_peso"]}%</div>', unsafe_allow_html=True)

# --- CATEGORIA 2: EFICIÊNCIA ---
st.markdown('<div class="category-header">⚡ Eficiência Operacional</div>', unsafe_allow_html=True)
df_efi = pd.DataFrame({
    "Indicador": ["⏱️ TMA / TMT (Tempo Médio)", "🚫 Improcedência Devida"],
    "Meta Homologada": [cluster["tma_meta"], cluster["improc_meta"]],
    "Peso na Nota": [f"{cluster['tma_peso']}%", f"{cluster['improc_peso']}%"]
})
st.dataframe(df_efi, use_container_width=True, hide_index=True)
peso_efi = cluster["tma_peso"] + cluster["improc_peso"]
st.markdown(f'<div class="total-box">Subtotal Peso Eficiência: {peso_efi}%</div>', unsafe_allow_html=True)

# --- CATEGORIA 3: DISCIPLINA OPERACIONAL ---
st.markdown('<div class="category-header">📋 Disciplina e Qualidade</div>', unsafe_allow_html=True)
df_dis = pd.DataFrame({
    "Indicador": ["📅 Aderência à Escala", "🎧 Nota de Monitoria", "🧠 Treinamento Regulamentar", "🛑 Evasão de Pausas"],
    "Meta Homologada": [cluster["ader_meta"], cluster["monit_meta"], cluster["trein_meta"], cluster["evasao_meta"]],
    "Peso na Nota": [f"{cluster['ader_peso']}%", f"{cluster['monit_peso']}%", f"{cluster['trein_meta']}", f"{cluster['evasao_weight'] if 'evasao_weight' in cluster else str(cluster['evasao_peso'])}%"]
})
# Ajustando para ler a chave certa do peso da evasão
df_dis.at[3, "Peso na Nota"] = f"{cluster['evasao_peso']}%"

st.dataframe(df_dis, use_container_width=True, hide_index=True)
peso_dis = cluster["ader_peso"] + cluster["monit_peso"] + cluster["evasao_peso"]
st.markdown(f'<div class="total-box">Subtotal Peso Disciplina: {peso_dis}%</div>', unsafe_allow_html=True)

st.divider()

# --- SEÇÃO GRAFICA (ÚLTIMO CAMPO) ---
st.subheader("📊 Campo Comparativo: Distribuição de Pesos entre Clusters")
st.markdown("Veja como a estratégia e os pesos mudam drasticamente de acordo com o perfil de cada cluster.")

clusters_lista = ["RE", "MONO", "MULTI", "CSF Interno", "CSF Ajuda", "CSF Quality"]
pesos_csat = [35, 35, 30, 0, 0, 0]
pesos_eficiencia = [40, 40, 40, 30, 30, 40] # Soma de TMA + Improcedência
pesos_disciplina = [25, 25, 30, 70, 70, 60] # Soma de Monitoria + Aderência + Evasão

fig = go.Figure()
fig.add_trace(go.Bar(x=clusters_lista, y=pesos_csat, name='🧠 Experiência (CSAT)', marker_color='#007bff'))
fig.add_trace(go.Bar(x=clusters_lista, y=pesos_eficiencia, name='⚡ Eficiência (TMA/Improc)', marker_color='#ffc107'))
fig.add_trace(go.Bar(x=clusters_lista, y=pesos_disciplina, name='📋 Disciplina (Monit/Escala/Pausas)', marker_color='#28a745'))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=350,
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)
st.plotly_chart(fig, use_container_width=True)
