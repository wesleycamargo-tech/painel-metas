import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

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
    .table-executiva { width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; margin-bottom: 20px; background-color: white; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); table-layout: fixed; }
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
    [
        "Julho / 2026", "Junho / 2026", "Maio / 2026", "Abril / 2026", "Março / 2026", "Fevereiro / 2026", "Janeiro / 2026",
        "Dezembro / 2025", "Novembro / 2025", "Outubro / 2025", "Setembro / 2025", "Agosto / 2025", "Julho / 2025", "Junho / 2025", "Maio / 2025", "Abril / 2025"
    ]
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
        <img src="https://upload.wikimedia.org/wikipedia/pt/e/e9/Logotipo_Grupo_Botic%C3%A1rio.png" onerror="this.style.display='none'" class="brand-logo">
        <h1 class="brand-title">Painel de Metas & Pesos CEX</h1>
    </div>
""", unsafe_allow_html=True)
st.caption(f"Visão Dinâmica de Metas, Pesos e Dimensões Estratégicas • **Competência Vigente: {competencia}**")
st.divider()

# --- DETERMINAÇÃO DAS ERAS DA OPERAÇÃO ---
mes_nome = competencia.split(" / ")[0].lower()
ano_nome = competencia.split(" / ")[1]

is_era_unificada_csf = (ano_nome == "2025") or (ano_nome == "2026" and mes_nome in ["janeiro", "fevereiro", "março", "marco"])
has_csf_ajuda = (ano_nome == "2026" and mes_nome in ["junho", "julho"])

pesos_padrao = {
    "CSAT": {"RE": "35%", "MONO": "35%", "MULTI": "30%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "0%"},
    "TMA / TMT": {"RE": "30%", "MONO": "30%", "MULTI": "30%", "CSF INTERNO": "30%", "CSF AJUDA": "0%", "CSF QUALITY": "30%"},
    "Improcedência Devida": {"RE": "10%", "MONO": "10%", "MULTI": "10%", "CSF INTERNO": "0%", "CSF AJUDA": "30%", "CSF QUALITY": "10%"},
    "Nota de Monitoria": {"RE": "25%", "MONO": "25%", "MULTI": "15%", "CSF INTERNO": "45%", "CSF AJUDA": "50%", "CSF QUALITY": "45%"},
    "Aderência à Escala": {"RE": "0%", "MONO": "0%", "MULTI": "15%", "CSF INTERNO": "25%", "CSF AJUDA": "20%", "CSF QUALITY": "0%"},
    "Evasão de Pausas": {"RE": "0%", "MONO": "0%", "MULTI": "0%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "15%"}
}

if not ("julho" in mes_nome and "2026" in ano_nome):
    pesos_padrao = {
        "CSAT": {"RE": "35%", "MONO": "40%", "MULTI": "35%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "0%"},
        "TMA / TMT": {"RE": "35%", "MONO": "30%", "MULTI": "30%", "CSF INTERNO": "35%", "CSF AJUDA": "0%", "CSF QUALITY": "35%"},
        "Improcedência Devida": {"RE": "10%", "MONO": "10%", "MULTI": "10%", "CSF INTERNO": "0%", "CSF AJUDA": "25%", "CSF QUALITY": "10%"},
        "Nota de Monitoria": {"RE": "20%", "MONO": "20%", "MULTI": "10%", "CSF INTERNO": "40%", "CSF AJUDA": "55%", "CSF QUALITY": "40%"},
        "Aderência à Escala": {"RE": "0%", "MONO": "0%", "MULTI": "15%", "CSF INTERNO": "25%", "CSF AJUDA": "20%", "CSF QUALITY": "15%"},
        "Evasão de Pausas": {"RE": "0%", "MONO": "0%", "MULTI": "0%", "CSF INTERNO": "0%", "CSF AJUDA": "0%", "CSF QUALITY": "0%"}
    }

if ano_nome == "2026" and mes_nome in ["abril", "maio", "junho", "julho"]:
    pesos_padrao["Aderência à Escala"]["CSF QUALITY"] = "0%"
    pesos_padrao["Evasão de Pausas"]["CSF QUALITY"] = "15%"

# --- LEITURA DO CSV ---
try:
    df_raw = pd.read_csv("metas.csv", header=None, sep=None, engine='python')

    # 1. LOCALIZADOR DE BLOCOS FLEXÍVEL
    idx_inicio = -1
    idx_fim = len(df_raw)
    
    target_token = mes_nome.replace("ç", "c").strip()
    
    for idx, row in df_raw.iterrows():
        c0_clean = str(row.iloc[0]).strip().lower().replace("ç", "c")
        if target_token in c0_clean and ano_nome in c0_clean:
            idx_inicio = idx
            break
            
    if idx_inicio != -1:
        for idx in range(idx_inicio + 1, len(df_raw)):
            c0_clean = str(df_raw.iloc[idx, 0]).strip().lower().replace("ç", "c")
            meses_stop = ["janeiro", "fevereiro", "março", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "histórico", "↓"]
            if any(m in c0_clean for m in meses_stop) and idx > idx_inicio + 2:
                idx_fim = idx
                break
                
    linhas_bloco = df_raw.iloc[idx_inicio:idx_fim] if idx_inicio != -1 else pd.DataFrame()

    # 2. RADAR DE MAPEAMENTO DE COLUNAS HISTÓRICAS
    map_cols = {}
    for idx, row in linhas_bloco.iterrows():
        row_str = [str(x).upper().strip() if pd.notna(x) else "" for x in row]
        if "METAS" in " ".join(row_str) or "RE" in row_str or "CAR" in row_str:
            for i, val in enumerate(row_str):
                if val in ["RE", "R.E", "CAR", "C.A.R.", "C.A.R"]: map_cols["RE"] = i
                elif "MONO" in val: map_cols["MONO"] = i
                elif "MULTI" in val: map_cols["MULTI"] = i
                elif "INTERNO" in val or "CSF INTERNO" in val: map_cols["CSF INTERNO"] = i
                elif "AJUDA" in val or "CSF AJUDA" in val: map_cols["CSF AJUDA"] = i
                elif "QUALITY" in val or "CSF QUALITY" in val: map_cols["CSF QUALITY"] = i
                elif val == "CSF" or "CSF E QUALITY" in val: map_cols["CSF_GENERICO"] = i
            break

    if is_era_unificada_csf and "CSF_GENERICO" in map_cols:
        map_cols["CSF INTERNO"] = map_cols["CSF_GENERICO"]
        map_cols["CSF QUALITY"] = map_cols["CSF_GENERICO"]
        del map_cols["CSF_GENERICO"]

    if not map_cols:
        map_cols = {"RE": 2, "CSF INTERNO": 3, "CSF AJUDA": 4, "CSF QUALITY": 5, "MONO": 6, "MULTI": 7}

    # 3. EXTRATOR DE METAS
    oficiais = ["CSAT", "TMA / TMT", "Improcedência Devida", "Nota de Monitoria", "Aderência à Escala", "Evasão de Pausas"]
    matriz_final = {ind: {cl: {"base": "-", "fone": "-", "dig": "-", "q1": "-"} for cl in clusters_totais} for ind in oficiais}
    current_pAI = None
    
    def pegar_val(r, cl):
        idx_col = map_cols.get(cl, -1)
        if idx_col != -1 and len(r) > idx_col and pd.notna(r.iloc[idx_col]):
            v = str(r.iloc[idx_col]).strip()
            return "-" if v.lower() in ["nan", "", "sem meta", "inativo", "-", "n/a"] else v
        return "-"

    for idx, row in linhas_bloco.iterrows():
        nome_linha = " ".join([str(x).upper().strip() for x in row.iloc[:3] if pd.notna(x)])
        
        if any(p in nome_linha for p in ["PONDERAÇÃO", "PONDERACAO", "FAIXAS", "PESOS"]):
            continue
            
        is_parent = False
        if ("CSAT" in nome_linha or "SATISFAÇÃO" in nome_linha or "SATISFACAO" in nome_linha) and "Q1" not in nome_linha: current_pAI = "CSAT"; is_parent = True
        elif ("TMA" in nome_linha or "TMT" in nome_linha or "TEMPO" in nome_linha) and "Q1" not in nome_linha: current_pAI = "TMA / TMT"; is_parent = True
        elif ("IMPROCEDÊNCIA" in nome_linha or "IMPROCEDENCIA" in nome_linha) and "Q1" not in nome_linha: current_pAI = "Improcedência Devida"; is_parent = True
        elif ("MONITORIA" in nome_linha or "NOTA DE" in nome_linha) and "Q1" not in nome_linha: current_pAI = "Nota de Monitoria"; is_parent = True
        elif ("ADERÊNCIA" in nome_linha or "ADERENCIA" in nome_linha or "ESCALA" in nome_linha) and "Q1" not in nome_linha: current_pAI = "Aderência à Escala"; is_parent = True
        elif ("EVASÃO" in nome_linha or "EVASAO" in nome_linha or "PAUSAS" in nome_linha) and "Q1" not in nome_linha: current_pAI = "Evasão de Pausas"; is_parent = True
        
        if not current_pAI:
            continue
            
        for cl in clusters_totais:
            if cl == "CSF AJUDA" and not has_csf_ajuda: continue
            if cl == "CSF QUALITY" and current_pAI == "Aderência à Escala" and not is_era_unificada_csf and mes_nome in ["abril", "maio", "junho", "julho"]: continue
            if cl == "CSF QUALITY" and current_pAI == "Evasão de Pausas" and is_era_unificada_csf: continue

            val = pegar_val(row, cl)
            if val == "-": continue
            
            if "Q1" in nome_linha: matriz_final[current_pAI][cl]["q1"] = val
            elif "FONE" in nome_linha: matriz_final[current_pAI][cl]["fone"] = val
            elif "DIGITAL" in nome_linha or "DIG" in nome_linha: matriz_final[current_pAI][cl]["dig"] = val
            else:
                if matriz_final[current_pAI][cl]["base"] == "-": matriz_final[current_pAI][cl]["base"] = val

    # ==============================================================================
    # QUADRO 1: MATRIZ DE INDICADORES
    # ==============================================================================
    st.markdown('<div class="macro-title">📋 MATRIZ INTEGRADA: METAS E PESOS POR CLUSTER</div>', unsafe_allow_html=True)
    
    # Determina o percentual de largura dinâmico de cada coluna operacional (para alinhamento cirúrgico)
    col_width_pct = 75 / (len(clusters_filtrados) * 2)

    html_tabela = f'<table class="table-executiva"><thead><tr><th rowspan="2" style="width: 25%;">Métrica / Indicador</th>'
    for cluster in clusters_filtrados:
        html_tabela += f'<th colspan="2" style="width: {col_width_pct * 2}%;">{cluster}</th>'
    html_tabela += '</tr><tr>'
    for cluster in clusters_filtrados:
        html_tabela += f'<th style="width: {col_width_pct}%;">Meta</th><th style="width: {col_width_pct}%;">Peso</th>'
    html_tabela += '</tr></thead><tbody>'

    icones = {"CSAT": "💻 ", "TMA / TMT": "⏱️ ", "Improcedência Devida": "🚫 ", "Nota de Monitoria": "🎧 ", "Aderência à Escala": "📅 ", "Evasão de Pausas": "🛑 "}
    pesos_sincronizados_grafico = {ind: {cl: 0 for cl in clusters_totais} for ind in oficiais}

    for indicador in oficiais:
        html_tabela += f'<tr><td style="text-align: left !important; padding-left: 15px; font-weight: bold; width: 25%;"> {icones[indicador]}{indicador}</td>'
        
        for cluster in clusters_filtrados:
            dados_celula = matriz_final[indicador][cluster]
            
            meta_html = ""
            if dados_celula["fone"] != "-" or dados_celula["dig"] != "-":
                f_str = f"Fone: {dados_celula['fone']}" if dados_celula["fone"] != "-" else ""
                d_str = f"Dig: {dados_celula['dig']}" if dados_celula["dig"] != "-" else ""
                sep = " / " if f_str and d_str else ""
                meta_html = f"{f_str}{sep}{d_str}"
            else:
                meta_html = dados_celula["base"]
                
            if dados_celula["q1"] != "-":
                if meta_html == "-" or meta_html == "": meta_html = f"<small class='meta-muted-gray'>Q1: {dados_celula['q1']}</small>"
                else: meta_html += f"<br><small class='meta-muted-gray'>Q1: {dados_celula['q1']}</small>"

            if meta_html == "" or "*** NÃO SEGUIRÁ" in meta_html.upper() or "INATIVO" in meta_html.upper() or "NÃO SEGUIRÁ" in meta_html.upper():
                meta_html = "-"

            peso_val = "-"
            if meta_html != "-":
                peso_val = pesos_padrao[indicador].get(cluster, "-")
            
            if peso_val == "0%": peso_val = "-"
            
            try: pesos_sincronizados_grafico[indicador][cluster] = int(peso_val.replace("%", "")) if peso_val != "-" else 0
            except: pesos_sincronizados_grafico[indicador][cluster] = 0

            if meta_html == "-":
                celula_html = f'<td class="meta-muted-gray" style="width: {col_width_pct}%;">{meta_html}</td>'
            elif "TMA" in indicador:
                celula_html = f'<td class="meta-tma-gray" style="width: {col_width_pct}%;">{meta_html}</td>'
            else:
                celula_html = f'<td style="width: {col_width_pct}%;">{meta_html}</td>'
                
            html_tabela += celula_html + f'<td style="width: {col_width_pct}%;">{peso_val}</td>'
        html_tabela += '</tr>'
        
    html_tabela += '</tbody></table>'
    
    if idx_inicio == -1:
        st.warning(f"Sincronizando a estrutura da planilha metas.csv para {competencia}...")
    else:
        st.html(html_tabela)

    # ==============================================================================
    # QUADRO 2: RESUMO DOS PILARES (PERFEITAMENTE ALINHADO COLUNA POR COLUNA)
    # ==============================================================================
    resumo_dimensoes = {}
    for cl in clusters_totais:
        exp = pesos_sincronizados_grafico["CSAT"][cl]
        efi = pesos_sincronizados_grafico["TMA / TMT"][cl] + pesos_sincronizados_grafico["Improcedência Devida"][cl]
        dis = pesos_sincronizados_grafico["Nota de Monitoria"][cl] + pesos_sincronizados_grafico["Aderência à Escala"][cl] + pesos_sincronizados_grafico["Evasão de Pausas"][cl]
        resumo_dimensoes[cl] = [f"{exp}%" if exp > 0 else "-", f"{efi}%" if efi > 0 else "-", f"{dis}%" if dis > 0 else "-"]

    if idx_inicio != -1 and len(linhas_bloco) > 0:
        st.markdown('<div class="macro-title">⚖️ RESUMO: SOMA DOS PESOS POR DIMENSÃO ESTRATÉGICA</div>', unsafe_allow_html=True)
        
        # Sincroniza a largura de colunas do resumo de pilares com o cabeçalho mestre de cima
        col_resumo_width_pct = 75 / len(clusters_filtrados)

        html_resumo = f'<table class="table-executiva"><thead><tr><th style="width: 25%; text-align: left !important; padding-left: 15px;">Dimensão Estratégica / Pilar</th>'
        for cluster in clusters_filtrados:
            html_resumo += f'<th style="width: {col_resumo_width_pct}%;">{cluster}</th>'
        html_resumo += '</tr></thead><tbody>'

        dados_resumo = [
            ("🧠 Experiência do Cliente", [resumo_dimensoes.get(c, ["-"])[0] for c in clusters_filtrados]),
            ("⚡ Eficiência Operacional (TMA + Improc.)", [resumo_dimensoes.get(c, ["-"])[1] for c in clusters_filtrados]),
            ("📋 Disciplina e Qualidade (Monit. + Escala + Pausas)", [resumo_dimensoes.get(c, ["-"])[2] for c in clusters_filtrados])
        ]
        for pilar, valores in dados_resumo:
            html_resumo += f'<tr><td style="text-align: left !important; font-weight: bold; width: 25%; padding-left: 15px;">{pilar}</td>'
            for val in valores:
                if val == "-": html_resumo += f'<td class="meta-muted-gray" style="width: {col_resumo_width_pct}%;">{val}</td>'
                else: html_resumo += f'<td style="width: {col_resumo_width_pct}%; font-weight: 600;">{val}</td>'
            html_resumo += '</tr>'
        html_resumo += '</tbody></table>'
        st.html(html_resumo)
        st.divider()

        # ==============================================================================
        # GRÁFICOS COMPLEMENTARES
        # ==============================================================================
        st.subheader("📊 Campo Comparativo: Visão Gráfica da Arquitetura de Pesos")
        valores_csat = [pesos_sincronizados_grafico["CSAT"][c] for c in clusters_filtrados]
        valores_eficiencia = [pesos_sincronizados_grafico["TMA / TMT"][c] + pesos_sincronizados_grafico["Improcedência Devida"][c] for c in clusters_filtrados]
        valores_disciplina = [pesos_sincronizados_grafico["Nota de Monitoria"][c] + pesos_sincronizados_grafico["Aderência à Escala"][c] + pesos_sincronizados_grafico["Evasão de Pausas"][c] for c in clusters_filtrados]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_csat, name='🧠 Experiência', marker_color='#1e3a8a', text=[f"{v}%" if v > 0 else "" for v in valores_csat], textposition='inside', textfont=dict(color='white', weight='bold')))
        fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_eficiencia, name='⚡ Eficiência', marker_color='#475569', text=[f"{v}%" if v > 0 else "" for v in valores_eficiencia], textposition='inside', textfont=dict(color='white', weight='bold')))
        fig.add_trace(go.Bar(x=clusters_filtrados, y=valores_disciplina, name='📋 Disciplina e Qualidade', marker_color='#0f766e', text=[f"{v}%" if v > 0 else "" for v in valores_disciplina], textposition='inside', textfont=dict(color='white', weight='bold')))
        fig.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=20, r=20, t=10, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5), yaxis=dict(title="Distribuição de Peso (%)", gridcolor="#e2e8f0"))
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro de processamento no arquivo metas.csv: {e}")
