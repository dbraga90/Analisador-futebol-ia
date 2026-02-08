import streamlit as st
import requests
import pandas as pd
from scipy.stats import poisson

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA Pro-Bet Analyzer", page_icon="⚽", layout="wide")

# Estilo CSS para melhorar o visual no telemóvel
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CÁLCULO (IA) ---
def calcular_poisson(media_casa, media_fora, media_cantos_casa, media_cantos_fora):
    # Probabilidades de Gols
    p_casa, p_empate, p_fora = 0, 0, 0
    for i in range(10):
        for j in range(10):
            p = poisson.pmf(i, media_casa) * poisson.pmf(j, media_fora)
            if i > j: p_casa += p
            elif i < j: p_fora += p
            else: p_empate += p
            
    # Probabilidade de Over 9.5 Escanteios (Cálculo acumulado)
    # 1 - probabilidade de ter entre 0 e 9 cantos
    prob_over_9_5_cantos = 1 - poisson.cdf(9, media_cantos_casa + media_cantos_fora)
    
    return p_casa, p_empate, p_fora, prob_over_9_5_cantos

# --- INTERFACE ---
st.title("⚽ IA Pro-Bet: Analisador de Apostas")
st.write("Introduz os dados dos últimos 5 jogos para obter a previsão estatística.")

# Layout em colunas
col_input, col_result = st.columns([1, 1])

with col_input:
    st.subheader("📝 Dados das Equipas")
    nome_casa = st.text_input("Equipa da Casa", "Mandante")
    nome_fora = st.text_input("Equipa Visitante", "Visitante")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        m_gols_casa = st.number_input(f"Média Gols {nome_casa}", min_value=0.0, value=1.5, step=0.1)
        m_cantos_casa = st.number_input(f"Média Cantos {nome_casa}", min_value=0.0, value=5.0, step=0.5)
    with c2:
        m_gols_fora = st.number_input(f"Média Gols {nome_fora}", min_value=0.0, value=1.0, step=0.1)
        m_cantos_fora = st.number_input(f"Média Cantos {nome_fora}", min_value=0.0, value=4.5, step=0.5)

    odd_casa = st.number_input(f"Odd p/ vitória {nome_casa} (Ex: 1.90)", min_value=1.01, value=2.0)

with col_result:
    st.subheader("📊 Previsão da IA")
    p_v_casa, p_e, p_v_fora, p_cantos = calcular_poisson(m_gols_casa, m_gols_fora, m_cantos_casa, m_cantos_fora)
    
    # Métricas Visuais
    st.metric(f"Vitória {nome_casa}", f"{p_v_casa:.1%}")
    st.metric("Empate", f"{p_e:.1%}")
    st.metric(f"Over 9.5 Cantos", f"{p_cantos:.1%}")

    # Lógica de Valor (Value Bet)
    st.markdown("---")
    prob_da_odd = 1 / odd_casa
    st.write(f"**Probabilidade da Casa (Odd):** {prob_da_odd:.1%}")
    
    if p_v_casa > prob_da_odd:
        ev = (p_v_casa * odd_casa) - 1
        st.success(f"✅ VALOR DETETADO! Expectativa: +{ev:.2f}")
        st.info("A probabilidade da IA é maior que a da casa. Sugestão: Entrada.")
    else:
        st.error("❌ SEM VALOR. A odd está demasiado baixa para o risco estatístico.")

# Rodapé
st.markdown("---")
st.caption("Aviso: Esta ferramenta utiliza modelos estatísticos. O futebol é imprevisível. Use com moderação.")