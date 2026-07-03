import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

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

# --- LEITURA INTELIGENTE COM CORREÇÃO DE QUEBRA DE LINHA ---
try:
    # 1. Abre o arquivo como texto bruto e normaliza todas as quebras de linha estranhas (\r e \r\n) para \n
    with open("metas.csv", "r", encoding="utf-8", errors="ignore") as f:
        conteudo_limpo = f.read().replace('\r\n', '\n').replace('\r', '\n')
    
    # 2. Converte de volta para uma tabela usando o motor dinâmico do Pandas (detectando separador ; ou ,)
    try:
        df_raw = pd.read_csv(io.StringIO(conteudo_limpo), header=None, sep=';')
        if df_raw.shape[1] <= 1: raise ValueError
    except:
        df_raw = pd.read_csv(io.StringIO(conteudo_limpo), header=None, sep=',')

    mes_procurado = "julho" if "Julho" in competencia else "junho"
    
    # 3. Localiza a linha inicial do mês selecionado
    idx_inicio = None
    for idx, row in df_raw.iterrows():
        txt = str(row.iloc[0]).strip().lower()
        if mes_procurado in txt:
            idx_inicio = idx
            break

    if idx_inicio is None:
        st.error(f"Não localizamos o marcador '{mes_procurado}' na primeira coluna do arquivo metas.csv.")
    else:
        # 4. Varre verticalmente e captura o bloco de dados do mês
        linhas_validas = []
        for i in range(idx_inicio + 1, len(df_raw)):
            row = df_raw.iloc[i]
            val_primeiro = str(row.iloc[0]).strip()
            
            # Condição de parada: se achar outro mês abaixo ou fim de histórico, interrompe
            if i > (idx_inicio + 2) and (
                ("junho" in val_primeiro.lower() and mes_procurado == "julho") or 
                ("julho" in val_primeiro.lower() and mes_procurado == "junho") or 
                ("maio" in val_primeiro.lower()) or
                ("↓" in val_primeiro) or 
                ("HISTÓRICO" in val_primeiro.upper())
            ):
                break
                
            if val_primeiro == "nan" or val_primeiro == "":
                continue
                
            linhas_validas.append(row)

        if len(linhas_validas) == 0:
            st.error(f"O bloco '{mes_procurado}' foi achado na linha {idx_inicio}, mas a formatação interna impede a leitura.")
        else:
            # 5. Formatação do mini DataFrame recortado
            df_mes = pd.DataFrame(linhas_validas)
            df_mes = df_mes.dropna(how='all', axis=1)
            
            colunas_completas = ["INDICADOR", "RE", "CSF INTERNO", "CSF AJUDA", "CSF QUALITY"]
            qtd_cols_reais = df_mes.shape[1]
            
            df_mes.columns = [colunas_completas[i] if i < len(colunas_completas) else f"COL_{i}" for i in range(qtd_cols_reais)]

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
                
                if "METAS -" in indicador_upper or "PONDERAÇÃO" in indicador_upper or "FAIXAS" in indicador_upper or "CSF INTERNO" in indicador_upper or "INDICADOR" in indicador_upper:
                    continue
                
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
                    else: html_resumo += f'<td>{val}</td>'
                html_resumo += '</tr>'
            html_resumo += '</tbody></table>'
            st.html(html_resumo)
            st.divider()

            # ==============================================================================
            # GRÁFICO COMPARATIVO
            # ==============================================================================
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
    st.error(f"Erro ao processar o arquivo metas.csv: {e}")
