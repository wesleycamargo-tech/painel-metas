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

# Estilização Executiva Premium
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
    .meta-muted-gray { color: #94a3b8 !important; font-weight: normal !important; font-size: 12px; }
    .meta-tma-gray { color: #64748b !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("## 📊 Filtros Corporativos")
st.sidebar.markdown("---")

competencia = st.sidebar.selectbox(
    "Selecione a Competência:", 
    ["Julho / 2026", "Junho / 2026", "Maio / 2026", "Abril / 2026", "Março / 2026", "Fevereiro / 2026", "Janeiro / 2026"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Segmentação Operacional")
filtro_macro = st.sidebar.radio(
    "Exibir no Painel:",
    ["Ver Todas as Clusters", "CRC (MONO + MULTI)", "RE", "CSF (Interno, Ajuda, Quality)"]
)

clusters_totais = ["RE", "MONO", "MULTI", "CSF INTERNO", "CSF AJUDA", "CSF QUALITY"]
if filtro_macro == "CRC (MONO + MULTI)":
    clusters_filtrados = ["MONO", "MULTI"]
elif filtro_macro == "RE":
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

# --- ARQUITETURA DINÂMICA DE PESOS POR MÊS ---
mes_procurado = competencia.split(" / ")[0].lower()

# Dicionário mestre que controla os pesos de forma centralizada e reflete na tabela e gráficos
if "julho" in mes_procurado:
    pesos_ativos = {
        "CSAT": {"RE": "35%", "MONO": "35%", "MULTI": "30%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "0%"},
        "TMA / TMT": {"RE": "30%", "MONO": "30%", "MULTI": "30%", "CSF INTERNO": "30%", "CSF AJUDA": "0%", "CSF QUALITY": "30%"},
        "Improcedência Devida": {"RE": "10%", "MONO": "10%", "MULTI": "10%", "CSF INTERNO": "0%", "CSF AJUDA": "30%", "CSF QUALITY": "10%"},
        "Nota de Monitoria": {"RE": "25%", "MONO": "25%", "MULTI": "15%", "CSF INTERNO": "45%", "CSF AJUDA": "50%", "CSF QUALITY": "45%"},
        "Aderência à Escala": {"RE": "0%", "MONO": "0%", "MULTI": "15%", "CSF INTERNO": "25%", "CSF AJUDA": "20%", "CSF QUALITY": "0%"},
        "Evasão de Pausas": {"RE": "0%", "MONO": "0%", "MULTI": "0%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "15%"}
    }
else:
    # Pesos Históricos (Junho, Maio, etc.) - Você pode editar esses valores aqui e o painel atualizará sozinho!
    pesos_ativos = {
        "CSAT": {"RE": "35%", "MONO": "40%", "MULTI": "35%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "0%"},
        "TMA / TMT": {"RE": "35%", "MONO": "30%", "MULTI": "30%", "CSF INTERNO": "35%", "CSF AJUDA": "0%", "CSF QUALITY": "35%"},
        "Improcedência Devida": {"RE": "10%", "MONO": "10%", "MULTI": "10%", "CSF INTERNO": "0%", "CSF AJUDA": "25%", "CSF QUALITY": "10%"},
        "Nota de Monitoria": {"RE": "20%", "MONO": "20%", "MULTI": "10%", "CSF INTERNO": "40%", "CSF AJUDA": "55%", "CSF QUALITY": "40%"},
        "Aderência à Escala": {"RE": "0%", "MONO": "0%", "MULTI": "15%", "CSF INTERNO": "25%", "CSF AJUDA": "20%", "CSF QUALITY": "0%"},
        "Evasão de Pausas": {"RE": "0%", "MONO": "0%", "MULTI": "0%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "15%"}
    }

# Calculadora Automática para Gráficos e Resumos baseada no dicionário acima
resumo_dimensoes = {}
grafico_pesos = {}
for cl in clusters_totais:
    def p2int(v): return int(v.replace("%", "")) if v not in ["-", "", "0%"] else 0
    exp = p2int(pesos_ativos["CSAT"][cl])
    efi = p2int(pesos_ativos["TMA / TMT"][cl]) + p2int(pesos_ativos["Improcedência Devida"][cl])
    dis = p2int(pesos_ativos["Nota de Monitoria"][cl]) + p2int(pesos_ativos["Aderência à Escala"][cl]) + p2int(pesos_ativos["Evasão de Pausas"][cl])
    resumo_dimensoes[cl] = [f"{exp}%", f"{efi}%", f"{dis}%"]
    grafico_pesos[cl] = [exp, efi, dis]

# --- REVISÃO DA LEITURA DO CSV ---
try:
    try:
        df_raw = pd.read_csv("metas.csv", header=None, sep=';')
        if df_raw.shape[1] <= 1: raise ValueError
    except:
        df_raw = pd.read_csv("metas.csv", header=None, sep=',')

    # 1. Captura o bloco bruto do mês de forma agressiva nas colunas A e B
    linhas_bloco = []
    capturando = False
    
    for idx, row in df_raw.iterrows():
        col_a = str(row.iloc[0]).strip().lower() if pd.notna(row.iloc[0]) else ""
        col_b = str(row.iloc[1]).strip().lower() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        txt_verif = col_a + " " + col_b
        
        if mes_procurado in txt_verif:
            capturando = True
            continue
        elif capturando and (col_a != "" or col_b != ""):
            if any(m in txt_verif for m in ["julho", "junho", "maio", "abril", "março", "fevereiro", "janeiro", "histórico", "↓"]) and mes_procurado not in txt_verif:
                capturando = False
                break
                
        if capturando:
            linhas_bloco.append(row)

    # 2. RADAR DE COLUNAS ULTRA-FLEXÍVEL
    map_cols = {}
    for row in linhas_bloco:
        linha_upper = [str(x).upper().strip() if pd.notna(x) else "" for x in row]
        if "RE" in linha_upper or "MONO" in linha_upper or "MULTI" in linha_upper:
            for i, val in enumerate(linha_upper):
                if val == "RE": map_cols["RE"] = i
                elif "MONO" in val: map_cols["MONO"] = i
                elif "MULTI" in val: map_cols["MULTI"] = i
                elif "CSF INTERNO" in val: map_cols["CSF INTERNO"] = i
                elif "CSF AJUDA" in val: map_cols["CSF AJUDA"] = i
                elif "QUALITY" in val or "CSF QUALITY" in val: map_cols["CSF QUALITY"] = i
            break

    if not map_cols:
        map_cols = {"RE": 2, "MONO": 3, "MULTI": 4, "CSF INTERNO": 5, "CSF AJUDA": 6, "CSF QUALITY": 7}

    def pegar_val(r, idx_col):
        if len(r) > idx_col and pd.notna(r.iloc[idx_col]):
            v = str(r.iloc[idx_col]).strip()
            return "-" if v.lower() in ["nan", "", "sem meta"] else v
        return "-"

    # 3. Dicionário Multidimensional para Agregar Fone, Digital e Q1
    oficiais = ["CSAT", "TMA / TMT", "Improcedência Devida", "Nota de Monitoria", "Aderência à Escala", "Evasão de Pausas"]
    matriz_final = {ind: {cl: {"base": "-", "fone": "-", "dig": "-", "q1": "-"} for cl in clusters_totais} for ind in oficiais}

    current_pAI = None
    
    # 4. Varre os dados e organiza na estrutura
    for row in linhas_bloco:
        col_b = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        if col_b == "": col_b = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        nome_upper = col_b.upper()
        
        if "METAS" in nome_upper or "INDICADOR" in nome_upper or "PONDERAÇÃO" in nome_upper or "FAIXAS" in nome_upper:
            continue
            
        # Descobre quem é o "Indicador Pai"
        is_parent = False
        if "CSAT" in nome_upper and "Q1" not in nome_upper: current_pAI = "CSAT"; is_parent = True
        elif ("TMA" in nome_upper or "TMT" in nome_upper) and "Q1" not in nome_upper: current_pAI = "TMA / TMT"; is_parent = True
        elif "IMPROCEDÊNCIA" in nome_upper and "Q1" not in nome_upper: current_pAI = "Improcedência Devida"; is_parent = True
        elif "MONITORIA" in nome_upper and "Q1" not in nome_upper: current_pAI = "Nota de Monitoria"; is_parent = True
        elif ("ADERÊNCIA" in nome_upper or "ESCALA" in nome_upper) and "Q1" not in nome_upper: current_pAI = "Aderência à Escala"; is_parent = True
        elif ("EVASÃO" in nome_upper or "PAUSAS" in nome_upper) and "Q1" not in nome_upper: current_pAI = "Evasão de Pausas"; is_parent = True
        
        if not current_pAI:
            continue
            
        # Coleta a meta do cluster
        for cl, idx_col in map_cols.items():
            val = pegar_val(row, idx_col)
            if val == "-": continue
            
            if "Q1" in nome_upper:
                matriz_final[current_pAI][cl]["q1"] = val
            elif "FONE" in nome_upper:
                matriz_final[current_pAI][cl]["fone"] = val
            elif "DIGITAL" in nome_upper or "DIG" in nome_upper:
                matriz_final[current_pAI][cl]["dig"] = val
            elif is_parent:
                matriz_final[current_pAI][cl]["base"] = val

    # ==============================================================================
    # QUADRO 1: MATRIZ DE INDICADORES CONSOLIDADA
    # ==============================================================================
    st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)
    
    html_tabela = '<table class="table-executiva"><thead><tr><th rowspan="2">Métrica / Indicador</th>'
    for cluster in clusters_filtrados:
        html_tabela += f'<th colspan="2">{cluster}</th>'
    html_tabela += '</tr><tr>'
    for cluster in clusters_filtrados:
        html_tabela += '<th>Meta</th><th>Peso</th>'
    html_tabela += '</tr></thead><tbody>'

    icones = {"CSAT": "💻 ", "TMA / TMT": "⏱️ ", "Improcedência Devida": "🚫 ", "Nota de Monitoria": "🎧 ", "Aderência à Escala": "📅 ", "Evasão de Pausas": "🛑 "}

    for indicador in oficiais:
        html_tabela += f'<tr><td style="text-align: left !important; padding-left: 15px;"><b>{icones[indicador]}{indicador}</b></td>'
        
        for cluster in clusters_filtrados:
            dados_celula = matriz_final[indicador][cluster]
            
            # Concatenação inteligente da Meta
            meta_html = ""
            if dados_celula["fone"] != "-" or dados_celula["dig"] != "-":
                f_str = f"Fone: {dados_celula['fone']}" if dados_celula["fone"] != "-" else ""
                d_str = f"Dig: {dados_celula['dig']}" if dados_celula["dig"] != "-" else ""
                sep = " / " if f_str and d_str else ""
                meta_html = f"{f_str}{sep}{d_str}"
            else:
                meta_html = dados_celula["base"]
                
            if dados_celula["q1"] != "-":
                if meta_html == "-" or meta_html == "": 
                    meta_html = f"<small class='meta-muted-gray'>Q1: {dados_celula['q1']}</small>"
                else:
                    meta_html += f"<br><small class='meta-muted-gray'>Q1: {dados_celula['q1']}</small>"

            if meta_html == "" or "*** NÃO SEGUIRÁ" in meta_html.upper() or "INATIVO" in meta_html.upper():
                meta_html = "-"
            
            # Busca o peso DIRETAMENTE do dicionário mestre, garantindo a alteração no filtro
            peso_val = pesos_ativos[indicador].get(cluster, "-")
            if peso_val == "0%": peso_val = "-"

            if meta_html == "-":
                celula_meta = f'<td class="meta-muted-gray">{meta_html}</td>'
            elif "TMA" in indicador:
                celula_meta = f'<td class="meta-tma-gray">{meta_html}</td>'
            else:
                celula_meta = f'<td>{meta_html}</td>'
                
            html_tabela += celula_meta + f'<td>{peso_val}</td>'
        html_tabela += '</tr>'
        
    html_tabela += '</tbody></table>'
    st.html(html_tabela)

    # ==============================================================================
    # QUADRO 2 E GRÁFICOS (ALIMENTADOS PELO MOTOR AUTOMÁTICO)
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
            if val in ["0%", "-", "0", "0%"]: html_resumo += f'<td class="meta-muted-gray">{val}</td>'
            else: html_resumo += f'<td>{val}</td>'
        html_resumo += '</tr>'
    html_resumo += '</tbody></table>'
    st.html(html_resumo)
    st.divider()

    st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")
    valores_csat = [grafico_pesos.get(c, [0, 0, 0])[0] for c in clusters_filtrados]
    valores_eficiencia = [grafico_pesos.get(c, [0, 0, 0])[1] for c in clusters_filtrados]
    valores_disciplina = [grafico_pesos.get(c, [0, 0, 0])[2] for c in clusters_filtrados]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_csat, name='🧠 Experiência', marker_color='#1e3a8a', text=[f"{v}%" if v > 0 else "" for v in valores_csat], textposition='inside', textfont=dict(color='white', weight='bold')))
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_eficiencia, name='⚡ Eficiência', marker_color='#475569', text=[f"{v}%" if v > 0 else "" for v in valores_eficiencia], textposition='inside', textfont=dict(color='white', weight='bold')))
    fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_disciplina, name='📋 Disciplina e Qualidade', marker_color='#0f766e', text=[f"{v}%" if v > 0 else "" for v in valores_disciplina], textposition='inside', textfont=dict(color='white', weight='bold')))
    fig.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=20, r=20, t=10, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5), yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0"))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro de processamento no arquivo metas.csv: {e}")
