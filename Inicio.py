import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="📊",
    layout="wide"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    body {background-color: #f0f2f6;}
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("""
    Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores de temperatura y humedad en diferentes puntos de la ciudad.
""")

# Subtítulo: Ubicación de Sensores
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})
st.map(eafit_location, zoom=15)

# Cargador de archivos
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        # Cargar y procesar datos
        df1 = pd.read_csv(uploaded_file)
        
        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Crear pestañas
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", 
             "🗺️ Información del Sitio", "📉 Pronósticos y Tendencias"]
        )

        # Pestaña 1: Visualización
        with tab1:
            st.subheader('Visualización de Datos')
            variable = st.selectbox(
                "Seleccione variable a visualizar",
                ["temperatura", "humedad", "Ambas variables"]
            )
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra", "Histograma", "Dispersión"]
            )
            if variable == "Ambas variables":
                st.write("### Temperatura")
                if chart_type in ["Línea", "Área", "Barra"]:
                    st.line_chart(df1["temperatura"]) if chart_type == "Línea" else st.area_chart(df1["temperatura"])
                else:
                    fig_temp = px.histogram(df1, x="temperatura", title="Distribución de Temperatura")
                    st.plotly_chart(fig_temp)

                st.write("### Humedad")
                if chart_type in ["Línea", "Área", "Barra"]:
                    st.line_chart(df1["humedad"]) if chart_type == "Línea" else st.area_chart(df1["humedad"])
                else:
                    fig_hum = px.histogram(df1, x="humedad", title="Distribución de Humedad")
                    st.plotly_chart(fig_hum)
            else:
                if chart_type in ["Línea", "Área", "Barra"]:
                    st.line_chart(df1[variable]) if chart_type == "Línea" else st.area_chart(df1[variable])
                elif chart_type == "Histograma":
                    fig = px.histogram(df1, x=variable, title=f"Distribución de {variable.capitalize()}")
                    st.plotly_chart(fig)
                elif chart_type == "Dispersión":
                    fig = px.scatter(df1, x=df1.index, y=variable, title=f"Dispersión de {variable.capitalize()}")
                    st.plotly_chart(fig)

        # Pestaña 2: Estadísticas
        with tab2:
            st.subheader('Análisis Estadístico')
            stat_variable = st.radio(
                "Seleccione variable para estadísticas", ["temperatura", "humedad"]
            )
            stats_df = df1[stat_variable].describe(percentiles=[0.25, 0.5, 0.75])
            st.dataframe(stats_df)

            # Métricas adicionales
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Promedio", f"{stats_df['mean']:.2f}")
            with col2:
                st.metric("Desviación Estándar", f"{stats_df['std']:.2f}")
            with col3:
                st.metric("Mediana", f"{stats_df['50%']:.2f}")

        # Pestaña 3: Filtros
        with tab3:
            st.subheader('Filtros Avanzados')
            # Filtro por rango de fechas
            min_date, max_date = st.date_input("Seleccione rango de fechas", 
                                               value=(df1.index.min().date(), df1.index.max().date()))
            filtered_df = df1.loc[(df1.index.date >= min_date) & (df1.index.date <= max_date)]
            
            # Filtro por rango de valores
            variable = st.selectbox("Variable para filtrar", ["temperatura", "humedad"])
            min_val, max_val = st.slider(
                f"Seleccione rango de {variable}",
                float(filtered_df[variable].min()),
                float(filtered_df[variable].max()),
                (float(filtered_df[variable].min()), float(filtered_df[variable].max()))
            )
            final_df = filtered_df[(filtered_df[variable] >= min_val) & (filtered_df[variable] <= max_val)]
            st.dataframe(final_df)

        # Pestaña 4: Información del sitio
        with tab4:
            st.subheader("Información del Sitio de Medición")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variables medidas:")
                st.write("  * Temperatura (°C)")
                st.write("  * Humedad (%)")
                st.write("- Frecuencia: Según configuración")
            with col2:
                st.write("### Ubicación")
                st.map(eafit_location, zoom=16)

        # Pestaña 5: Pronósticos
        with tab5:
            st.subheader("📉 Pronósticos y Tendencias")
            y = df1["temperatura"]
            X = np.array(range(len(y))).reshape(-1, 1)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
            model = LinearRegression().fit(X_train, y_train)
            pred_future = model.predict([[len(y)+1]])
            st.metric("Predicción futura (próxima observación)", f"{pred_future[0]:.2f}°C")
            st.line_chart(y)

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')

# Footer
st.markdown("""
    ---
    Desarrollado para el análisis de datos de sensores urbanos.
    Ubicación: Universidad EAFIT, Medellín, Colombia
""")
