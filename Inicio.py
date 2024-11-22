import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime


st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("""
    Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores de temperatura y humedad en diferentes puntos de la ciudad.
""")

# Ubicación del sensor
eafit_location = pd.DataFrame({'lat': [6.2006], 'lon': [-75.5783], 'location': ['Universidad EAFIT']})
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)
        column_mapping = {'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
                          'humedad {device="ESP32", name="Sensor 1"}': 'humedad'}
        df1 = df1.rename(columns=column_mapping)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio", "🔎 Comparaciones"])

        # Cambios en Visualización
        with tab1:
            st.subheader('Visualización de Datos')
            variable = st.selectbox("Seleccione variable a visualizar", ["temperatura", "humedad", "Ambas variables"])
            chart_type = st.selectbox("Seleccione tipo de gráfico", ["Línea", "Área", "Barra", "Dispersión"])
            
            if variable == "Ambas variables":
                st.write("### Temperatura")
                if chart_type == "Línea":
                    st.line_chart(df1["temperatura"])
                elif chart_type == "Área":
                    st.area_chart(df1["temperatura"])
                elif chart_type == "Dispersión":
                    st.write(st.pyplot(df1["temperatura"].plot(style='.', title="Dispersión de Temperatura")))
                else:
                    st.bar_chart(df1["temperatura"])
                st.write("### Humedad")
                st.line_chart(df1["humedad"]) if chart_type == "Línea" else st.area_chart(df1["humedad"])
            else:
                if chart_type == "Dispersión":
                    st.write(st.pyplot(df1[variable].plot(style='.', title=f"Dispersión de {variable}")))
                elif chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])

            if st.checkbox('Mostrar datos crudos'):
                st.dataframe(df1)

        # Cambios en Estadísticas
        with tab2:
            st.subheader('Análisis Estadístico')
            stat_variable = st.radio("Seleccione variable para estadísticas", ["temperatura", "humedad"])
            stats_df = df1[stat_variable].describe()
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df)
                if st.button('Mostrar resumen en texto'):
                    st.write(f"La variable seleccionada ({stat_variable}) tiene un promedio de {stats_df['mean']:.2f}, "
                             f"un máximo de {stats_df['max']:.2f}, y un mínimo de {stats_df['min']:.2f}.")
            
            with col2:
                comp_variable = 'humedad' if stat_variable == 'temperatura' else 'temperatura'
                st.metric(f"Máximo {stat_variable.capitalize()}", f"{stats_df['max']:.2f}")
                st.metric(f"Mínimo {stat_variable.capitalize()}", f"{stats_df['min']:.2f}")
                st.metric(f"Comparación con Máx. {comp_variable.capitalize()}",
                          f"{stats_df['max'] - df1[comp_variable].max():.2f}")

        # Cambios en Filtros
        with tab3:
            st.subheader('Filtros de Datos')
            filter_variable = st.selectbox("Seleccione variable para filtrar", ["temperatura", "humedad"])
            range_filter = st.slider(f"Rango de {filter_variable}",
                                      float(df1[filter_variable].min()),
                                      float(df1[filter_variable].max()),
                                      (float(df1[filter_variable].min()), float(df1[filter_variable].max())))
            filtrado_df_range = df1[(df1[filter_variable] >= range_filter[0]) & (df1[filter_variable] <= range_filter[1])]
            st.write(f"Registros filtrados por {filter_variable} entre {range_filter[0]} y {range_filter[1]}:")
            st.dataframe(filtrado_df_range)

            promedio_filtrado = filtrado_df_range[filter_variable].mean()
            st.metric(f"Promedio Filtrado de {filter_variable}", f"{promedio_filtrado:.2f}")

        # Nueva pestaña Comparaciones
        with tab5:
            st.subheader("Análisis de Correlación")
            if "temperatura" in df1.columns and "humedad" in df1.columns:
                correlacion = df1.corr().loc['temperatura', 'humedad']
                st.write(f"La correlación entre temperatura y humedad es: {correlacion:.2f}")
                st.line_chart(df1[['temperatura', 'humedad']])
            else:
                st.error("No se encontraron datos suficientes para realizar comparaciones.")

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')

st.markdown("---\nDesarrollado para análisis urbano en Medellín, Colombia.")
