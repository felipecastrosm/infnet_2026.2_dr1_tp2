import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk

def load_data():
    try:
        df1_2020 = pd.read_csv('dados/HIST_PAINEL_COVIDBR_2020_Parte1_05set2025.csv', sep=';')
        df2_2020 = pd.read_csv('dados/HIST_PAINEL_COVIDBR_2020_Parte2_05set2025.csv', sep=';')
        df = pd.concat([df1_2020, df2_2020], ignore_index=True)
        return df
    except FileNotFoundError:
        st.warning("Arquivo 'HIST_PAINEL_COVIDBR_2020_Parte1_05set2025.csv' não encontrado. Gerando dados simulados para demonstração.")

df = load_data()
st.title("Dashboard Epidemiológico - COVID-19 Brasil - 2020")
st.markdown("---")

# EXERCÍCIO 1: Importância da Visualização de Dados
st.header("1. Importância da Visualização de Dados")
st.write("A visualização de dados permite transformar grandes volumes de dados em informações relevantes e interpretáveis por humanos. No contexto da pandemia, tais informações podem auxiliar a encontrar padrões e identificar tendências, servindo como base para criação de medidas de contenção e prevenção, e informando decisões de gestão pública.")
st.markdown("---")

# EXERCÍCIO 2: Gráfico de Barras com Streamlit
st.header("2. Gráfico de Barras com Streamlit - Evolução Semanal de Casos no RJ")
estado = 'RJ'
st.write(f"**Estado Escolhido:** {estado}. Escolhido por ter sido o estado onde eu estava durante a pandemia.")
df_rj = df[(df['estado'] == estado) & (df['municipio'].isnull())]
casos_semana_rj = df_rj.groupby('semanaEpi')['casosNovos'].sum()
st.bar_chart(casos_semana_rj)
st.markdown("---")

# EXERCÍCIO 3: Gráfico de Linha com Streamlit
st.header("3. Gráfico de Linha com Streamlit - Óbitos Acumulados no Brasil")
st.write("A curva de óbitos durante o primeiro ano de pandemia mostra um aumento bastante constante e estável, com leve desaceleração a partir da 40a semana, provavelmente devido às medidas de contenção e isolamento.")
df_brasil = df[df['municipio'].isnull()].groupby('semanaEpi')['obitosAcumulado'].sum()
st.line_chart(df_brasil)
st.markdown("---")

# EXERCÍCIO 4: Gráfico de Área com Streamlit
st.header("4. Gráfico de Área com Streamlit - Casos Acumulados no RJ, SP e MG")
estados_comparacao = ['RJ', 'SP', 'MG']
df_area = df[(df['estado'].isin(estados_comparacao)) & (df['municipio'].isnull())]
tabela_area = df_area.pivot_table(index='semanaEpi', columns='estado', values='casosAcumulado', aggfunc='sum')
st.area_chart(tabela_area)
st.write("Devido à grande densidade populacional, o estado de SP apresenta curva de casos acumulados começando a subir antes dos outros estados, e mantendo uma tendência bem mais acentuada. O estado de MG, apesar de começar a curva mais tarde, sobe o número de casos de forma mais acentuada do que o RJ, ultrapassando-o em poucas semanas. O RJ, por sua vez, mantém crescimento no número de casos estável, e mesmo no pico fica abaixo de SP e MG.")
st.markdown("---")

# EXERCÍCIO 5: Mapa com Streamlit
st.header("5. Mapa com Streamlit - Top 5 Municípios com Maior Número de Casos no RJ")
st.write("Mapear os municípios com maior número de casos pode informar decisões de gestão pública, como a alocação de recursos médicos, vacinas e leitos hospitalares. A informação geográfica pode também auxiliar na identificação de padrões de contágio e na intensificação de medidas de contenção e isolamento.")

df_rj_municipios = df[(df['estado'] == 'RJ') & (df['municipio'].notnull())].copy()
df_rj_agrupado = df_rj_municipios.groupby('municipio')['casosAcumulado'].max().reset_index()
top_5_rj = df_rj_agrupado.nlargest(5, 'casosAcumulado')
coordenadas_rj = {
    'Rio de Janeiro': {'latitude': -22.90138484752003, 'longitude': -43.24300759406431},
    'São Gonçalo': {'latitude': -22.823226033115237, 'longitude': -43.047958351163494},
    'Niterói': {'latitude': -22.8854041628991, 'longitude': -43.117232874147724},
    'Petrópolis': {'latitude': -22.508419784349194, 'longitude': -43.175594470986915},
    'Volta Redonda': {'latitude': -22.50766751541158, 'longitude': -44.09602130716566}
}
top_5_rj['latitude'] = top_5_rj['municipio'].apply(lambda x: coordenadas_rj.get(x, {}).get('latitude'))
top_5_rj['longitude'] = top_5_rj['municipio'].apply(lambda x: coordenadas_rj.get(x, {}).get('longitude'))

st.write("Tabela dos 5 municípios mais afetados no RJ:", top_5_rj[['municipio', 'casosAcumulado', 'latitude', 'longitude']].reset_index(drop=True))
st.map(top_5_rj[['latitude', 'longitude']])
st.markdown("---")

# EXERCÍCIO 6: Visualização com Matplotlib
st.header("6. Visualização com Matplotlib")
semana_recente = df['semanaEpi'].max()
df_mat = df[(df['semanaEpi'] == semana_recente) & (df['municipio'].isnull())].groupby('estado')[['casosNovos', 'obitosNovos']].sum()

fig, ax = plt.subplots(figsize=(10, 5))
df_mat.plot(kind='bar', ax=ax, width=0.8)
ax.set_title(f'Casos e Óbitos na Semana Epidemiológica {semana_recente}')
ax.set_ylabel('Quantidade')
st.pyplot(fig)
st.write("O gráfico mostra que a quantidade de casos é significativamente maior do que a quantidade de óbitos em todos os estados, indicando que a taxa de letalidade é relativamente baixa.")
st.markdown("---")

# EXERCÍCIO 7: Boxplot com Seaborn
st.header("7. Boxplot com Seaborn")
regioes_selecionadas = ['Norte', 'Nordeste', 'Sudeste']
df_box = df[(df['regiao'].isin(regioes_selecionadas)) & (df['municipio'].isnull())]

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df_box, x='regiao', y='casosNovos', ax=ax2)
ax2.set_title('Distribuição de Casos Novos por Semana Epidemiológica')
st.pyplot(fig2)
st.write("Enquanto a região Norte apresenta uma distribuição de novos casos mais estável, a região Nordeste mostra um padrão mais volátil, com mais outliers, e a região Sudeste vai ao extremo, com muitos outliers, indicando que a alta densidade populacional contribuiu para picos de contágio.")
st.markdown("---")

# EXERCÍCIO 8: Gráfico de Área com Altair
st.header("8. Gráfico de Área com Altair")
df_altair = df[(df['regiao'] == 'Sudeste') & (df['municipio'].isnull())].groupby('semanaEpi')['casosNovos'].sum().reset_index()

grafico_area = alt.Chart(df_altair).mark_area(opacity=0.6).encode(
    x=alt.X('semanaEpi', title='Semana Epidemiológica'),
    y=alt.Y('casosNovos', title='Casos Novos'),
    tooltip=['semanaEpi', 'casosNovos']
).properties(title="Evolução de Casos Novos - Sudeste", width=700, height=400)

st.altair_chart(grafico_area, use_container_width=True)
st.write("O Sudeste foi escolhido por sua alta densidade populacional. O gráfico mostra que houveram ondas de contágio, seguidas de vales onde a quantidade de novos casos diminuiu, mas não de forma consistente, já que houveram diversos picos subsequentes.")
st.markdown("---")

# EXERCÍCIO 9: Heatmap com Altair
st.header("9. Heatmap com Altair")
df_rj_corr = df[(df['estado'] == 'RJ') & (df['municipio'].isnull())][['casosNovos', 'obitosNovos']].corr().reset_index()
df_corr_melted = df_rj_corr.melt(id_vars='index', var_name='Variavel2', value_name='Correlacao')
df_corr_melted.rename(columns={'index': 'Variavel1'}, inplace=True)

heatmap = alt.Chart(df_corr_melted).mark_rect().encode(
    x='Variavel1:O',
    y='Variavel2:O',
    color=alt.Color('Correlacao:Q', scale=alt.Scale(domain=[-1, 1])),
    tooltip=['Variavel1', 'Variavel2', 'Correlacao']
).properties(title="Matriz de Correlação (Rio de Janeiro)", width=400, height=400)

st.altair_chart(heatmap, use_container_width=False)
st.write("Há uma forte correlação positiva entre novos casos e novos óbitos, o que é esperado, dado que a taxa de letalidade faz com que quanto mais casos, mais óbitos ocorram.")
st.markdown("---")

# EXERCÍCIO 10: Gráfico de Pizza com Plotly
st.header("10. Gráfico de Pizza com Plotly")
df_pizza = df[(df['semanaEpi'] == semana_recente) & (df['municipio'].isnull()) & (df['regiao'] != "Brasil")].groupby('regiao')['casosAcumulado'].sum().reset_index()

fig_pie = px.pie(df_pizza, values='casosAcumulado', names='regiao', title='Distribuição de Casos Acumulados por Região', hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)
st.write("A distribuição de casos por região mostra que a densidade populacional do Sudeste e Nordeste é compatível com a quantiade de casos, já que o contágio é favorecido por grandes centros urbanos onde a transmissão do vírus é mais fácil.")
st.markdown("---")

# EXERCÍCIO 11: Subplots com Plotly
st.header("11. Subplots com Plotly")
df_sul = df[(df['regiao'] == 'Sul') & (df['municipio'].isnull())].groupby('semanaEpi')[['casosNovos', 'obitosNovos']].sum().reset_index()
df_norte = df[(df['regiao'] == 'Norte') & (df['municipio'].isnull())].groupby('semanaEpi')[['casosNovos', 'obitosNovos']].sum().reset_index()

fig_sub = make_subplots(rows=2, cols=2, subplot_titles=("Casos - Sul", "Óbitos - Sul", "Casos - Norte", "Óbitos - Norte"))
fig_sub.add_trace(go.Bar(x=df_sul['semanaEpi'], y=df_sul['casosNovos'], name='Casos Sul', marker_color='blue'), row=1, col=1)
fig_sub.add_trace(go.Bar(x=df_sul['semanaEpi'], y=df_sul['obitosNovos'], name='Óbitos Sul', marker_color='red'), row=1, col=2)
fig_sub.add_trace(go.Bar(x=df_norte['semanaEpi'], y=df_norte['casosNovos'], name='Casos Norte', marker_color='lightblue'), row=2, col=1)
fig_sub.add_trace(go.Bar(x=df_norte['semanaEpi'], y=df_norte['obitosNovos'], name='Óbitos Norte', marker_color='orange'), row=2, col=2)

fig_sub.update_layout(height=600, showlegend=False, title_text="Região Sul vs Norte")
st.plotly_chart(fig_sub, use_container_width=True)
st.write("O gráfico mostra que apesar da região Sul ter apresentado um crescimento mais acentuado no número de óbitos em relação ao aumento de casos, a região Norte apresentou uma taxa de letalidade mais alta, mantendo números de óbitos mais elevados do que os da região Sul, mas com menor número de casos.")
st.markdown("---")

# EXERCÍCIO 12: Mapa Interativo com PyDeck
st.header("12. Mapa Interativo com PyDeck")
df_rj_municipios = df[(df['estado'] == 'RJ') & (df['municipio'].notnull())].copy()
df_rj_agrupado = df_rj_municipios.groupby('municipio').agg({
    'casosAcumulado': 'max',
    'populacaoTCU2019': 'max'
}).reset_index()
top_5_rj = df_rj_agrupado.nlargest(5, 'casosAcumulado')
coordenadas_rj = {
    'Rio de Janeiro': {'latitude': -22.90138484752003, 'longitude': -43.24300759406431},
    'São Gonçalo': {'latitude': -22.823226033115237, 'longitude': -43.047958351163494},
    'Niterói': {'latitude': -22.8854041628991, 'longitude': -43.117232874147724},
    'Petrópolis': {'latitude': -22.508419784349194, 'longitude': -43.175594470986915},
    'Volta Redonda': {'latitude': -22.50766751541158, 'longitude': -44.09602130716566}
}
top_5_rj['latitude'] = top_5_rj['municipio'].apply(lambda x: coordenadas_rj.get(x, {}).get('latitude'))
top_5_rj['longitude'] = top_5_rj['municipio'].apply(lambda x: coordenadas_rj.get(x, {}).get('longitude'))
top_5_rj['populacaoTCU2019'] = top_5_rj['populacaoTCU2019'].replace(0, 1) 
top_5_rj['casos_por_100k'] = (top_5_rj['casosAcumulado'] / top_5_rj['populacaoTCU2019']) * 100000
top_5_rj['raio_visual'] = top_5_rj['casos_por_100k'] * 3 

layer = pdk.Layer(
    "ScatterplotLayer",
    data=top_5_rj,
    get_position=['longitude', 'latitude'],
    get_radius='raio_visual',
    get_fill_color=[255, 75, 75, 180],
    pickable=True,
    radius_min_pixels=10,
    radius_max_pixels=100
)
view_state = pdk.ViewState(
    latitude=-22.90138484752003, 
    longitude=-43.24300759406431,
    zoom=8, 
    pitch=35
)
st.pydeck_chart(pdk.Deck(
    layers=[layer], 
    initial_view_state=view_state, 
    tooltip={"text": "{municipio}\nPopulação: {populacaoTCU2019}\nCasos Absolutos: {casosAcumulado}\nCasos por 100k Hab: {casos_por_100k}"}
))

st.write("Apesar da conclusão mais lógica ser de que a maior densidade populacional facilitaria o contágio e ampliaria o número de casos por 100k habitantes, os municípios menores, com menor densidade populacional, como Volta Redonda e Petrópolis, apresentaram taxa de casos por habitantes bem mais elevada. Uma possível razão para tal fenômeno é que a população desses municípios menores pode ter tido menos medidas de isolamento e contenção impostas.")
st.markdown("---")