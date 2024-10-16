import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats
import streamlit as st

# Variáveis globais
mean_a, dp_a, n_a = 600.0, 50.0, 10000
mean_b, dp_b, n_b = 600.0, 50.0, 300

def plot_hist(df_1, df_2, nbinsx):

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df_1,
        nbinsx=nbinsx,
        name='Amostra A',
        opacity=0.6,
        marker_color='blue',
        histnorm='probability density'
    ))

    fig.add_trace(go.Histogram(
        x=df_2,
        nbinsx=nbinsx,
        name='Amostra B',
        opacity=0.3,
        marker_color='red',
        histnorm='probability density'
    ))

    fig.update_layout(
        barmode='overlay',
        title="Comparação de Amostras A e B",
        xaxis_title="Valor",
        yaxis_title="Frequência",
        bargap=0.1
    )

    return fig

def generate_sample_normal(mean, dp, n):

    return np.random.normal(mean, dp, n)

def stats_test_t(df_1, df_2, equal_var):

    t_stat, p_value = scipy.stats.ttest_ind(df_1, df_2, alternative='two-sided', equal_var = equal_var)

    return t_stat, p_value

def stats_test_ks(df_1, df_2):

    result = scipy.stats.ks_2samp(df_1, df_2)
    
    return result 

def st_sidebar():

    global mean_a, dp_a, n_a, mean_b, dp_b, n_b, n_bins

    # Sidebar para entradas do usuário
    st.sidebar.header("Configurações da Amostra A")
    mean_a = st.sidebar.number_input("Média Amostra A", value=mean_a, step=1.0)
    dp_a = st.sidebar.number_input("Desvio Padrão Amostra A", value=dp_a, step=0.5)
    n_a = st.sidebar.number_input("Tamanho da Amostra A", value=n_a, min_value=1, step=25)

    st.sidebar.header("Configurações da Amostra B")
    mean_b = st.sidebar.number_input("Média Amostra B", value=mean_b, step=1.0)
    dp_b = st.sidebar.number_input("Desvio Padrão Amostra B", value=dp_b, step=0.5)
    n_b = st.sidebar.number_input("Tamanho da Amostra B", value=n_b, min_value=1, step=25)

    st.sidebar.header("Outros parâmetros")
    n_bins = st.sidebar.number_input("Número de Bins", value=0, step=5)

def st_body():

    with st.expander("Simulador teste T para 2 amostras indepententes", expanded=True):

        st.markdown("""      
        Hipóteses:
        - *Hipótese Nula (H0)*: As médias das duas amostras são iguais.
        - *Hipótese Alternativa (H1)*: As médias das duas amostras são diferentes.
                    
        Índice de significância: 5%
        """)

    # Gerar amostra A e B e plotar
    np.random.seed(999)
    sample_a = generate_sample_normal(mean_a, dp_a, n_a)
    sample_b = generate_sample_normal(mean_b, dp_b, n_b)

    st.plotly_chart(plot_hist(sample_a, sample_b, n_bins))

    if dp_a == dp_b:

        # Calcular p-valor pelo teste T com 2 amostras independentes (DP igual)
        t_stat, p_value = stats_test_t(sample_a, sample_b, equal_var = True)

    else:
        # Calcular p-valor pelo teste T com 2 amostras independentes (DP diferente)
        t_stat, p_value = stats_test_t(sample_a, sample_b, equal_var = False)

    with st.expander("Resultado Teste T (bilateral))", expanded=True):
    
        st.write(f"Estatística t: {t_stat:.4f}, Valor-p: {p_value:.4f}")
 
        if p_value < 0.05:

            st.markdown("*Resultado*: Rejeitamos a hipótese nula (H0). As médias são estatisticamente diferentes.")

        else:

            st.markdown("*Resultado*: Não rejeitamos a hipótese nula (H0). Não há evidências suficientes para afirmar que as médias são diferentes.")
    
    with st.expander("Resultado Teste Kolmogorov-Smirnov (KS)", expanded=True):

        result_ks = stats_test_ks(sample_a, sample_b)

        st.write(f"Estatística ks: {result_ks.statistic:.4f}, Valor-p: {result_ks.pvalue:.4f}")

        if result_ks.pvalue < 0.05:

            st.markdown("*Resultado*: Rejeitamos a hipótese nula (H0): as distribuições são diferentes.")

        else:

            st.markdown("*Resultado*: Não rejeitamos a hipótese nula (H0): não há evidência suficiente para dizer que as distribuições são diferentes.")

def main():

    st_sidebar()  
    st_body()

main()