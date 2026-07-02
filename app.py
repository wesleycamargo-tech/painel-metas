import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .main { background-color: #f8f9fa; }
    .header-container { display: flex; align-items: center; gap: 15px; margin-bottom: 5px; }
    .brand-logo { height: 45px; object-fit: contain; }
    .brand-title { font-family: sans-serif; color: #0f172a; margin: 0 !important; font-size: 32px; font-weight: 700; }
    .macro-title { background-color: #1e293b; color: white; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; margin-top: 15px; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; color: #f8fafc !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p { color: #f8fafc !important; }
    div[data-testid="stRadio"] label { color: #cbd5e1 !important; font-weight: 500; }
    .table-executiva { width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; margin-bottom: 20px; background-color: white; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .table-executiva th { background-color: #f1f5f9; color: #1e293b; font-weight: 600; padding: 10px; border: 1px solid #e2e8f0; text-align: center !important; }
    .table-executiva td { padding: 12px 10px; border: 1px solid #e2e8f0; text-align: center !important; color: #0f172a !important; }
    .meta-muted-gray { color: #94a3b8 !important; font-weight: normal !important; }
    .meta-tma-gray { color: #64748b !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("## 📊 Filtros Corporativos")
st.sidebar.markdown("---")

competencia = st.sidebar.selectbox(
    "Selecione a Competência:", 
    ["Julho / 2026", "Junho / 2026"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Segmentação Operacional")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "RE", "CSF (Interno, Ajuda, Quality)"]
)

# Definição dos clusters alvo
clusters_totais = ["RE", "CSF INTERNO", "CSF AJUDA", "CSF QUALITY"]
if filtro_macro == "RE":
    clusters_filtrados = ["RE"]
elif filtro_macro == "CSF (Interno, Ajuda, Quality)":
    clusters_filtrados = ["CSF INTERNO", "CSF AJUDA", "CSF QUALITY"]
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

# --- LEITURA E PROCESSO DO CSV ---
try:
    df_raw = pd.read_csv("metas.csv", header=None)
    
    # Busca apenas a palavra-chave principal (julho ou junho) de forma flexível
    mes_procurado = "julho" if "Julho" in competencia else "junho"
    
    linha_inicio = None
    for idx, row in df_raw.iterrows():
        val_celula = str(row.iloc[0]).strip().lower()
        if mes_procurado in val_celula:
            linha_inicio = idx
            break

    if linha_inicio is None:
        st.error(f"Não foi possível localizar o bloco para o mês de '{mes_procurado}' no arquivo metas.csv.")
    else:
        linhas_bloco = []
        colunas_cabecalho = []
        
        for idx in range(linha_inicio + 1, len(df_raw)):
            row = df_raw.iloc[idx]
            primeira_celula = str(row.iloc[0]).strip()
            row_str = [str(c).strip().upper() for c in row if pd.notna(c)]
            
            # Condição de parada flexível: se achar outro mês abaixo ou fim de histórico, para
            if idx > (linha_inicio + 2) and (
                ("junho" in primeira_celula.lower() and mes_procurado == "julho") or 
                ("julho" in primeira_celula.lower() and mes_procurado == "junho") or 
                ("maio" in primeira_celula.lower()) or
                ("↓" in primeira_celula) or 
                ("HISTÓRICO" in primeira_celula.upper())
            ):
                break
                
            # Identificação do cabeçalho procurando os termos reais das colunas
            if "CSF INTERNO" in row_str or "RE" in row_str or "CSF QUALITY" in row_str:
                colunas_cabecalho = [str(c).strip().upper() if pd.notna(c) and str(c).strip() != "" else f"COL_{i}" for i, c in enumerate(row)]
                colunas_cabecalho[0] = "INDICADOR"
                continue
                
            # Captura a linha de dados se não for vazia ou de ponderação
            if primeira_celula != "nan" and primeira_celula != "":
                if "PONDERAÇÃO" in primeira_celula.upper() or "FAIXAS" in primeira_celula.upper() or "METAS" in primeira_celula.upper():
                    continue
                linhas_bloco.append(row)

        if len(linhas_bloco) == 0:
            st.warning(f"Buscando estrutura de dados... O bloco '{mes_procurado}' foi localizado, mas suas linhas internas estão em formato de leitura incompatível.")
            st.info("Dica: Certifique-se de que a palavra 'RE' ou 'CSF INTERNO' está escrita logo acima dos indicadores desse mês.")
        else:
            # Caso o cabeçalho não tenha sido detectado automaticamente, força o padrão
            if len(colunas_cabecalho) == 0:
                colunas_cabecalho = ["INDICADOR", "RE", "CSF INTERNO", "CSF AJUDA", "CSF QUALITY"]
            
            df_mes = pd.DataFrame(linhas_bloco)
            df_mes = df_mes.iloc[:, :len(colunas_cabecalho)]
            df_mes.columns = colunas_cabecalho

            # ==============================================================================
            # QUADRO 1: MATRIZ DE INDICADORES
            # ==============================================================================
            st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)
            
            html_tabela = '<table class="table-executiva"><thead><tr><th rowspan="2">Métrica / Indicador</th>'
            for cluster in clusters_filtrados:
                html_tabela += f'<th colspan="2">{cluster}</th>'
            html_tabela += '</tr><tr>'
            for cluster in clusters_filtrados:
                html_tabela += '<th>Meta</th><th>Peso</th>'
            html_tabela += '</tr></thead><tbody>'

            if "julho" in mes_procurado:
                grafico_pesos = {"RE": [35, 40, 25], "CSF INTERNO": [0, 30, 70], "CSF AJUDA": [0, 30, 70], "CSF QUALITY": [0, 40, 60]}
                resumo_dimensoes = {"RE": ["35%", "40%", "25%"], "CSF INTERNO": ["0%", "30%", "70%"], "CSF AJUDA": ["0%", "30%", "70%"], "CSF QUALITY": ["0%", "40%", "60%"]}
            else:
                grafico_pesos = {"RE": [35, 45, 20], "CSF INTERNO": [0, 35, 65], "CSF AJUDA": [0, 25, 75], "CSF QUALITY": [0, 45, 55]}
                resumo_dimensoes = {"RE": ["35%", "45%", "20%"], "CSF INTERNO": ["0%", "35%", "65%"], "CSF AJUDA": ["0%", "25%", "75%"], "CSF QUALITY": ["0%", "45%", "55%"]}

            icones = {"CSAT": "💻 ", "TMA": "⏱️ ", "IMPROCEDÊNCIA": "🚫 ", "MONITORIA": "🎧 ", "ADERÊNCIA": "📅 ", "EVASÃO": "🛑 "}

            for _, row in df_mes.iterrows():
                indicador_nome = str(row.iloc[0]).strip()
                indicador_upper = indicador_nome.upper()
                
                icone = "🔹 "
                for k, v in icones.items():
                    if k in indicador_upper:
                        icone = v
                        break
                        
                html_tabela += f'<tr><td style="text-align: left !important; padding-left: 15px;"><b>{icone}{indicador_nome}</b></td>'
                
                for cluster in clusters_filtrados:
                    meta_val = str(row.get(cluster, "-")).strip() if cluster in df_mes.columns else "-"
                    
                    peso_val = "-"
                    if cluster in resumo_dimensoes:
                        if "CSAT" in indicador_upper: peso_val = "35%" if cluster == "RE" else "0%"
                        elif "TMA" in indicador_upper: peso_val = "30%"
                        elif "IMPROCEDÊNCIA" in indicador_upper: peso_val = "10%" if cluster != "CSF AJUDA" else "30%"
                        elif "MONITORIA" in indicador_upper: peso_val = "25%" if cluster == "RE" else ("45%" if cluster == "CSF INTERNO" else "50%")
                        elif "ADERÊNCIA" in indicador_upper: peso_val = "25%" if cluster == "CSF INTERNO" else ("20%" if cluster == "CSF AJUDA" else "0%")
                        elif "EVASÃO" in indicador_upper: peso_val = "15%" if cluster == "CSF QUALITY" else "0%"

                    if meta_val in ["-", "nan", "*** Não seguirá com o indicador", "Sem meta"] or meta_val == "":
                        meta_val = "-"
                        celula_meta = f'<td class="meta-muted-gray">{meta_val}</td>'
                    elif "TMA" in indicador_upper:
                        celula_meta = f'<td class="meta-tma-gray">{meta_val}</td>'
                    else:
                        celula_meta = f'<td>{meta_val}</td>'
                        
                    html_tabela += celula_meta + f'<td>{peso_val}</td>'
                html_tabela += '</tr>'
                
            html_tabela += '</tbody></table>'
            st.html(html_tabela)

            # ==============================================================================
            # QUADRO 2: RESUMO INVERTIDO
            # ==============================================================================
            st.markdown('<div class="macro-title">⚖️ RESUMO: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA</div>', unsafe_allow_html=True)
            html_resumo = '<table class="table-executiva"><thead><tr><th>Dimensão Estratégica / Pilar</th>'
            for cluster in clusters_filtrados:
                html_resumo += f'<th>{cluster}</th>'
            html_resumo += '</tr></thead><tbody>'

            dados_resumo = [
                ("🧠 Experiência do Cliente", [resumo_dimensoes.get(c, ["-"])[0] for c in clusters_filtrados]),
                ("⚡ Eficiência Operacional (TMA + Improc.)", [resumo_dimensoes.get(c, ["-"])[1] for c in clusters_filtrados]),
                ("📋 Disciplina e Qualidade (Monit. + Escala + Pausas)", [resumo_dimensoes.get(c, ["-"])[2] for c in clusters_filtrados])
            ]
            for pilar, valores in dados_resumo:
                html_resumo += f'<tr><td style="text-align: left !important; font-weight: bold;">{pilar}</td>'
                for val in valores:
                    if val in ["0%", "-", "0"]: html_resumo += f'<td class="meta-muted-gray">{val}</td>'
                    else: html_res
