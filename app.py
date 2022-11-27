# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


pd.options.plotting.backend = "plotly"

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Ecoframe Dashboard",
                   page_icon=":bar_chart:", layout="wide")


# ---- MAINPAGE ----
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image("Ecoframe-Logo.png")

with col3:
    st.write(' ')

st.title("📊 Ecoframe Dashboard")
st.markdown("##")


# ---- READ EXCEL ----

df = pd.read_excel('dataset_final.xlsx')
df.index = pd.to_datetime(df['Date'])
df.drop('Date', axis=1, inplace=True)
min_date = df.index.min()
max_date = df.index.max()

df_test_pred = pd.read_excel('test_pred.xlsx')
df_test_pred.index = pd.to_datetime(df_test_pred['Date'])
df_test_pred.drop('Date', axis=1, inplace=True)

df_top_kpi = df.copy()

df_opti = pd.read_excel('opti_example_dataset.xlsx')
df_opti.index = pd.to_datetime(df_opti['Date'])
df_opti.drop('Date', axis=1, inplace=True)


# ---- SIDEBAR ----
st.sidebar.header("Filtres")
date = st.sidebar.date_input(
    "Sélectionner la période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    disabled=False)

df = df.loc[date[0]:date[1]]
df_top_kpi = df_top_kpi.loc[date[0]:date[1]]

energy = st.sidebar.multiselect(
    "Sélectionner le type d'énergie",
    options=['kWh', 'eau', 'gaz'],
    default=['kWh', 'eau', 'gaz']
)
columns = list(df.columns)
if len(energy) == 1:
    res = list(filter(lambda x: energy[0] in x, columns))
    res = res+['Emission Co2e']
    df = df[res]
elif len(energy) == 2:
    subs1 = energy[0]
    subs2 = energy[1]
    res1 = list(filter(lambda x: subs1 in x, columns))
    res2 = list(filter(lambda x: subs2 in x, columns))
    res = res1 + res2
    res = res + ['Emission Co2e']
    df = df[res]
else:
    df = df.copy()

frequence = st.sidebar.selectbox(
    "Sélectionner la fréquence des visualisations",
    ('Mensuelle', 'Annuelle', 'Quotidienne'),
)
if frequence == 'Annuelle':
    freq_sec = 'D'
elif frequence == 'Mensuelle':
    freq_sec = 'M'
elif frequence == 'Quotidienne':
    freq_sec = 'D'

batiment = st.sidebar.multiselect(
    "Sélectionner le bâtiment",
    options=['Bâtiment A'],
    default=['Bâtiment A']
)

# TOP KPI's
sum_conso = round(df_top_kpi["Consommation (kWh)"].sum(), 1)
sum_gaz = round(df_top_kpi["Consommation (gaz)"].sum(), 1)
sum_eau = round(df_top_kpi["Consommation (eau)"].sum(), 1)


left_column, mid_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Consommation (électrique) :")
    st.subheader(f" {sum_conso}")
with mid_column:
    st.subheader("Total Consommation (gaz) :")
    st.subheader(f" {sum_gaz}")
with right_column:
    st.subheader("Total Consommation (eau) :")
    st.subheader(f" {sum_eau}")

st.markdown("""---""")


# Graph distribution pie_chart
def get_pie_distribution(df, variable, title):
    columns = list(df.columns)
    conso = variable
    res = list(filter(lambda x: conso in x, columns))
    df_conso = df[res]
    values = [df_conso[x].sum() for x in df_conso.columns]
    names = list(df_conso.columns)
    fig = px.pie(df_conso, values=values, names=names, title=title,
                 color_discrete_sequence=px.colors.sequential.Aggrnyl)
    return fig

# Graph courbes


def get_courbe(df, variable, freq_sec, title):
    columns = list(df.columns)
    conso = variable
    res = list(filter(lambda x: conso in x, columns))
    df_conso = df[res]
    fig = df_conso.groupby(pd.Grouper(freq=freq_sec)).sum().plot(title=title)
    return fig


fig_distribution_consommations_energetique = get_pie_distribution(
    df, variable='Consommation', title=' Distribution des différentes consommations énergétiques sur la période sélectionnée')

st.plotly_chart(fig_distribution_consommations_energetique,
                use_container_width=True, theme='Streamlit')

fig_Distribution_equivalents_Euro_consommations_energetique = get_pie_distribution(
    df, variable='Equivalent', title=" Distribution des equivalents en Euro des différentes consommations énergétiques sur la période sélectionnée")

st.plotly_chart(fig_Distribution_equivalents_Euro_consommations_energetique,
                use_container_width=True, theme='Streamlit')


st.plotly_chart(df[['Emission Co2e']].groupby(pd.Grouper(freq=freq_sec)).sum().plot(title='Distribution des emissions  ( KgCo2e) en fréquence {} sur la periode selectionnée'.format(frequence), kind='bar'),
                use_container_width=True, theme='Streamlit')

fig_courbe_distribution_multi_energy = get_courbe(
    df=df, variable='Consommation', freq_sec=freq_sec, title='Courbe des consommation multi-énergie selon la fréquence séléctionnée')

st.plotly_chart(fig_courbe_distribution_multi_energy,
                use_container_width=True, theme='Streamlit')

st.plotly_chart(df_test_pred.plot(),
                use_container_width=True, theme='Streamlit')


fig_opti_before = px.line(df_opti[['Consommation (kWh)', 'Sans optimisation']], title='Contrat avant optimisation',
                          range_x=['2022-02-21', '2022-02-28'], range_y=[0, 85])


fig_opti_after = px.line(df_opti[['Consommation (kWh)', 'Avec optimisation']], title='Contrat après optimisation',
                         range_x=['2022-02-21', '2022-02-28'], range_y=[0, 60])

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_opti_before,
                    use_container_width=True, theme='Streamlit')
with right_column:
    st.plotly_chart(fig_opti_after,
                    use_container_width=True, theme='Streamlit')

left_column, mid_column, right_column = st.columns(3)
with mid_column:
    st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Economie réalisée : 2 185,97 €</p>',
                unsafe_allow_html=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
