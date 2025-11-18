import streamlit as st
import mysql.connector
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import time

# --- CONFIGURAÇÕES (Igual aos scripts anteriores) ---
SQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  # <--- COLOQUE SUA SENHA AQUI
    'database': 'acompanhamento_pacientes_bd'
}

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "acompanhamento_pacientes_hibrido_db"

# --- FUNÇÕES DE CONEXÃO ---
def get_sql_connection():
    return mysql.connector.connect(**SQL_CONFIG)

def get_mongo_client():
    return MongoClient(MONGO_URI)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Monitoramento UTI - Híbrido",
    page_icon="🏥",
    layout="wide"
)

# --- CSS CUSTOMIZADO (Para dar cara de Hospital/Sistema Dark) ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .metric-card { background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #4da6ff; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL - BUSCA DE PACIENTES (SQL)
# ==============================================================================
st.sidebar.title("🏥 Central de Monitoramento")
st.sidebar.write("Sistema Híbrido SQL + NoSQL")

conn_sql = get_sql_connection()
cursor = conn_sql.cursor(dictionary=True)

# Buscar lista simples de pacientes para o SelectBox
cursor.execute("SELECT idPacientes, Nome FROM pacientes ORDER BY Nome")
pacientes_list = cursor.fetchall()
opcoes_pacientes = {p['Nome']: p['idPacientes'] for p in pacientes_list}

# Seletor
nome_selecionado = st.sidebar.selectbox(
    "Selecione o Paciente:",
    options=list(opcoes_pacientes.keys())
)
id_paciente_selecionado = opcoes_pacientes[nome_selecionado]

st.sidebar.divider()
st.sidebar.info(f"Monitorando ID: {id_paciente_selecionado}")

# ==============================================================================
# ÁREA PRINCIPAL
# ==============================================================================

# 1. DADOS CADASTRAIS (Vindos do SQL)
cursor.execute("""
    SELECT p.*, b.Nome_do_Bairro, c.Nome_da_Cidade 
    FROM pacientes p
    JOIN bairros b ON p.Bairros_idBairros = b.idBairros
    JOIN cidades c ON b.Cidades_idCidades = c.idCidades
    WHERE p.idPacientes = %s
""", (id_paciente_selecionado,))
dados_sql = cursor.fetchone()

col1, col2 = st.columns([3, 1])

with col1:
    st.title(f"🩺 {dados_sql['Nome']}")
    st.caption(f"CPF: {dados_sql['CPF']} | Data Nasc: {dados_sql['Data_de_Nascimento']} | Local: {dados_sql['Nome_da_Cidade']}")

with col2:
    # Badge de Status
    status = dados_sql['Status']
    cor = "green" if status == 'A' else "red"
    st.markdown(f"### Status: :{cor}[ATIVO]")

st.divider()

# 2. CONEXÃO COM NOSQL (MongoDB)
client = get_mongo_client()
db = client[MONGO_DB_NAME]

# Buscar leituras do equipamento (últimas 30 leituras para gráfico)
cursor_mongo = db.leituras_equipamentos.find(
    {"id_paciente_sql": id_paciente_selecionado}
).sort("timestamp", -1).limit(50)

dados_mongo = list(cursor_mongo)

if dados_mongo:
    # Converter para DataFrame do Pandas para facilitar gráficos
    df_leituras = pd.DataFrame([
        {
            "Hora": d['timestamp'],
            "BPM": d['dados'].get('bpm'),
            "Saturacao": d['dados'].get('saturacao_o2'),
            "Pressao": d['dados'].get('pressao_arterial')
        } 
        for d in dados_mongo
    ])
    
    # Ordenar por hora crescente para o gráfico fazer sentido (esquerda p/ direita)
    df_leituras = df_leituras.sort_values(by="Hora")

    # --- PAINEL DE MÉTRICAS EM TEMPO REAL (Última leitura) ---
    ultima_leitura = dados_mongo[0]['dados']
    
    st.subheader("📡 Sinais Vitais (Tempo Real)")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Batimentos (BPM)", f"{ultima_leitura.get('bpm')} ❤️", delta_color="inverse")
    m2.metric("Saturação O2", f"{ultima_leitura.get('saturacao_o2')}% 🌬️", delta_color="normal")
    m3.metric("Pressão", f"{ultima_leitura.get('pressao_arterial')}")
    m4.metric("Temp", f"{ultima_leitura.get('temp_pele')} °C")

    # --- GRÁFICOS DE EVOLUÇÃO ---
    st.subheader("📈 Evolução Clínica (Últimas Horas)")
    
    tab1, tab2 = st.tabs(["Batimentos Cardíacos", "Oxigenação Sanguínea"])
    
    with tab1:
        fig_bpm = px.line(df_leituras, x="Hora", y="BPM", markers=True, title="Histórico de BPM", line_shape="spline")
        fig_bpm.update_traces(line_color='#FF4B4B') # Vermelho
        st.plotly_chart(fig_bpm, use_container_width=True)
        
    with tab2:
        fig_o2 = px.area(df_leituras, x="Hora", y="Saturacao", markers=True, title="Saturação de Oxigênio (%)")
        fig_o2.update_traces(line_color='#00CC96') # Verde
        # Definir eixo Y para focar entre 80 e 100%
        fig_o2.update_layout(yaxis_range=[80, 100])
        st.plotly_chart(fig_o2, use_container_width=True)

else:
    st.warning("⚠️ Nenhum dado de equipamento encontrado para este paciente no MongoDB.")

# 3. LOGS E ALERTAS (Híbrido: Trazendo logs do Mongo vinculados ao SQL)
st.divider()
st.subheader("🚨 Histórico de Alertas e Logs")

logs_cursor = db.logs_alertas_disparados.find(
    {"id_paciente_sql": id_paciente_selecionado}
).sort("timestamp", -1)

logs = list(logs_cursor)

if logs:
    # Criar tabela visual
    logs_data = []
    for log in logs:
        logs_data.append({
            "Data/Hora": log['timestamp'],
            "Nível": log['nivel_critico'],
            "Mensagem": log['mensagem'],
            "Trigger (Valor)": log.get('dados_trigger', {}).get('valor_detectado', 'N/A')
        })
    
    df_logs = pd.DataFrame(logs_data)
    st.dataframe(df_logs, use_container_width=True)
else:
    st.info("Nenhum alerta crítico registrado para este paciente.")

# Rodapé
conn_sql.close()
client.close()