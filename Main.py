import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns 
import altair as alt
from UI import *
from matplotlib import pyplot as plt

#pip install streamlit-extras
#https://pypi.org/project/streamlit-extras/

from streamlit_extras.dataframe_explorer import dataframe_explorer


#page layout
st.set_page_config(page_title="Analisis de Gastos", page_icon="bar:chart", layout="wide")

#streamlit theme=none
theme_plotly = None 

# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

UI()
#load dataset
#df=pd.read_csv('data.csv')

df=pd.read_excel('data.xlsx')

st.sidebar.image("images/grafico-de-linea.gif")
#filter date to view data
with st.sidebar:
 st.title("Seleccione el rango de fecha")
 st.markdown("desde Ene/2024-May/2024")
 start_date=st.date_input(label="Fecha Inicio")

with st.sidebar:
 end_date=st.date_input(label="Fecha Final")
st.error("Business Metrics between[ "+str(start_date)+"] and ["+str(end_date)+"]")


#compare date
df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

#Toast for page refresh
st.toast("La página ha sido actualizada")

#dataframe
with st.expander("Filtrar Datos de Excel"):
 filtered_df = dataframe_explorer(df2, case=False)
 st.dataframe(filtered_df, use_container_width=True)


b1, b2=st.columns(2)

#bar chart
with b1:  
 st.subheader('Gastos & Cantidades', divider='rainbow',)
 source = pd.DataFrame({
        "Cantidad ($)": df2["Cantidad"],
        "Gastos": df2["Gastos"]
      })
 
 bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Cantidad ($)):Q",
        y=alt.Y("Gastos:N", sort="-x")
    )
 st.altair_chart(bar_chart, use_container_width=True,theme=theme_plotly)
 
 #metric cards
 with b2:
    st.subheader('Métricas de Datos', divider='rainbow',)
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, = st.columns(2)
    col1.metric(label="Detelle de los Gastos ", value=df2.Gastos.count(), delta="Número de Gastos")
    col2.metric(label="Suma de Gastos valor en USD:", value= f"{df2.ValorTotal.sum():,.0f}",delta=round(df2.ValorTotal.median(),2))
    
    col11, col22,col33, = st.columns(3)
    col11.metric(label="Max Valor en USD:", value= f"{ df2.ValorTotal.max():,.0f}",delta="Max Valor")
    col22.metric(label="Min. Valor en USD:", value= f"{ df2.ValorTotal.min():,.0f}",delta="Min. Valor")
    col33.metric(label="Rango Valor Total en USD:", value= f"{ df2.ValorTotal.max()-df2.ValorTotal.min():,.0f}",delta="Rango Anual de Gastos")
    #style the metric
    style_metric_cards(background_color="#596073",border_left_color="#F71938",border_color="#1f66bd",box_shadow="#F71938")


#dot Plot
a1,a2=st.columns(2)
with a1:
 st.subheader('Gastos & Valor Total', divider='rainbow',)
 source = df2
 chart = alt.Chart(source).mark_circle().encode(
    x='Gastos',
    y='ValorTotal',
    color='Categoria',
 ).interactive()
 st.altair_chart(chart, theme="streamlit", use_container_width=True)


with a2:
 st.subheader('Gastos & Valor Unitario', divider='rainbow',)
 energy_source = pd.DataFrame({
    "Gastos": df2["Gastos"],
    "ValorUnitario ($)":  df2["ValorUnitario"],
    "Date": df2["OrderDate"]
    })
 
 #bar Graph
 bar_chart = alt.Chart(energy_source).mark_bar().encode(
        x="month(Date):O",
        y="sum(ValorUnitario ($)):Q",
        color="Gastos:N"
    )
 st.altair_chart(bar_chart, use_container_width=True,theme=theme_plotly)
 
 
 #select only numeric or number data
 #pip install pandas-select
 #https://pypi.org/project/pandas-select/
p1,p2=st.columns(2) 
with p1:
# Select features to display scatter plot
 st.subheader('Frecuencia de Gastos', divider='rainbow',)
 feature_x = st.selectbox('Seleccionar característica para x Datos cualitativos', df2.select_dtypes("object").columns)
 feature_y = st.selectbox('Seleccionar característica para y Datos cualitativos', df2.select_dtypes("number").columns)

# Display scatter plot
 fig, ax = plt.subplots()
 sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df.Gastos, ax=ax)
 st.pyplot(fig)


with p2:
 st.subheader('Frecuencia de Gastos', divider='rainbow',)
 feature = st.selectbox('Seleccionar gastos por ', df2.select_dtypes("object").columns)
# Plot histogram
 fig, ax = plt.subplots()
 ax.hist(df2[feature], bins=20)

# Set the title and labels
 ax.set_title(f'Histograma de {feature}')
 ax.set_xlabel(feature)
 ax.set_ylabel('Frecuencia')

 # Display the plot
 st.pyplot(fig)
 st.markdown("")  
 st.markdown("---") 
 st.markdown("")  
 st.markdown("@ 2024 - Walter Gómez - Fullstack Developer")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

 



 















 


