import streamlit as st
from scipy.stats import poisson

# Configuração simples
st.set_page_config(page_title="IA Analisador", layout="wide")

st.title("⚽ Analisador de Probabilidades")

# Criando campos de entrada
col1, col2 = st.columns(2)

with col1:
    st.subheader("Entrada de Dados")
    time_casa = st.text_input("Time da Casa", "Time A")
    # Use value=1.5 para garantir que nunca seja zero no início
    m_gols_casa = st.number_input(f"Média Gols {time_casa}", value=1.5, step=0.1)
    m_cantos_casa = st.number_input(f"Média Cantos {time_casa}", value=5.0, step=0.5)

with col2:
    st.subheader("Dados do Visitante")
    time_fora = st.text_input("Time Visitante", "Time B")
    m_gols_fora = st.number_input(f"Média Gols {time_fora}", value=1.0, step=0.1)
    m_cantos_fora = st.number_input(f"Média Cantos {time_fora}", value=4.0, step=0.5)

# O CÁLCULO - Agora fora de qualquer função para rodar sempre
st.divider()
st.subheader("📊 Resultado da Análise")

# Cálculo de Gols (Poisson)
prob_casa, prob_empate, prob_fora = 0, 0, 0
for i in range(10):
    for j in range(10):
        p = poisson.pmf(i, m_gols_casa) * poisson.pmf(j, m_gols_fora)
        if i > j: prob_casa += p
        elif i < j: prob_fora += p
        else: prob_empate += p

# Cálculo de Cantos
prob_cantos = 1 - poisson.cdf(9, m_cantos_casa + m_cantos_fora)

# Exibição Direta
c1, c2, c3 = st.columns(3)
c1.metric(f"Vitória {time_casa}", f"{prob_casa:.1%}")
c2.metric("Empate", f"{prob_empate:.1%}")
c3.metric(f"Vitória {time_fora}", f"{prob_fora:.1%}")

st.info(f"🎯 Probabilidade de Over 9.5 Escanteios: **{prob_cantos:.1%}**")

# Se os números não mudarem, o log abaixo vai nos dizer o porquê
if m_gols_casa == 0 and m_gols_fora == 0:
    st.warning("Aguardando inserção de médias maiores que zero...")