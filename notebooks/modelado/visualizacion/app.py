import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Lectura de datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Configuración de la página
st.set_page_config(
    page_title="Herramienta de Visualización de Datos - 13MBID",
    page_icon="📊",
    layout="wide",
)

# Título de la aplicación
st.title("Herramienta de Visualización de Datos - 13MBID")
st.write("Esta aplicación permite explorar y visualizar los datos del proyecto en curso.")
st.write("Desarrollado por: Jorge Gómez Gómez")
st.markdown('----')

# ========= GRÁFICO 1 =========
st.header("Gráficos")
st.subheader("1. Caracterización de los créditos otorgados:")

# Cantidad de créditos por objetivo del mismo
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
st.plotly_chart(creditos_x_objetivo, use_container_width=True)

# Histograma de los importes de créditos otorgados
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')
st.plotly_chart(histograma_importes, use_container_width=True)

# ========= GRÁFICO 2 =========
st.subheader("2. Distribución por estado de crédito y mora, según objetivo")

# Selector
tipo_credito = st.selectbox("Selecciona el tipo de crédito:", df['objetivo_credito'].unique())
st.write("Tipo de crédito seleccionado:", tipo_credito)

# Filtro
df_filtrado = df[df['objetivo_credito'] == tipo_credito]

col1, col2 = st.columns(2)
with col1:
    barras_apiladas = px.histogram(df_filtrado, x='objetivo_credito', color='estado_credito_N',
                                    title='Distribución de créditos por estado y objetivo',
                                    barmode='stack')
    barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
    st.plotly_chart(barras_apiladas, use_container_width=True)

with col2:
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()
    fig_pie = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig_pie.update_layout(title_text='Distribución de créditos en función de registro de mora')
    st.plotly_chart(fig_pie, use_container_width=True)

# ========= GRÁFICO 3 =========
st.subheader("3. Importe promedio según antigüedad del cliente")

# Orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')
st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)

# ========= GRÁFICO 4 y 5 =========
st.subheader("4. Análisis de importes y duración del crédito")

# Filtros combinados
col_filtros1, col_filtros2 = st.columns(2)
with col_filtros1:
    objetivo_filtrado = st.selectbox("Filtra por objetivo del crédito:", df['objetivo_credito'].unique())
with col_filtros2:
    estado_filtrado = st.selectbox("Filtra por estado del crédito:", df['estado_credito_N'].unique())

# Aplicar ambos filtros
df_doble_filtrado = df[
    (df['objetivo_credito'] == objetivo_filtrado) &
    (df['estado_credito_N'] == estado_filtrado)
]

# Mostrar gráficos en dos columnas
col1, col2 = st.columns(2)

with col1:
    fig_box = px.box(
        df_doble_filtrado,
        x="objetivo_credito",
        y="importe_solicitado",
        title=f"Distribución de Importe por Objetivo ({estado_filtrado})",
        labels={
            "objetivo_credito": "Objetivo del Crédito",
            "importe_solicitado": "Importe Solicitado"
        }
    )
    fig_box.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        df_doble_filtrado,
        x="duracion_credito",
        y="importe_solicitado",
        color="objetivo_credito",
        title=f"Importe vs. Duración por Objetivo ({estado_filtrado})",
        labels={
            "duracion_credito": "Duración del Crédito",
            "importe_solicitado": "Importe Solicitado"
        }
    )
    fig_scatter.update_traces(marker=dict(size=6, opacity=0.7))
    st.plotly_chart(fig_scatter, use_container_width=True)

# ========= GRÁFICO 6 =========
st.subheader("5. Mapa de calor de correlación entre variables numéricas")

# Correlación entre variables
variables_corr = df[["importe_solicitado", "duracion_credito", "personas_a_cargo"]]
correlacion = variables_corr.corr()

fig_heatmap = px.imshow(correlacion, text_auto=True, color_continuous_scale="RdBu_r",
                        title="Mapa de Calor de Correlación entre Variables Seleccionadas",
                        labels=dict(color="Correlación"))
fig_heatmap.update_layout(xaxis_title="", yaxis_title="")
st.plotly_chart(fig_heatmap, use_container_width=True)
