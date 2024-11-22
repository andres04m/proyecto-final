import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Page configuration
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

# Title and description
st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("""
    Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores de temperatura y humedad en diferentes puntos de la ciudad.
""")

# Create map data for EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Display map
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# File uploader
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        # Load and process data
        df1 = pd.read_csv(uploaded_file)
        
        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio"])

        with tab1:
            st.subheader('Visualización de Datos')
            
            # Rango de fechas
            st.write("### Filtro por Rango de Fechas")
            start_date, end_date = st.date_input(
                "Seleccione un rango de fechas:",
                [df1.index.min().date(), df1.index.max().date()]
            )
            df_filtered = df1.loc[start_date:end_date]

            # Variable selector
            variable = st.selectbox(
                "Seleccione variable a visualizar",
                ["temperatura", "humedad", "Ambas variables"]
            )
            
            # Chart type selector
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra", "Puntos"]
            )

            # Promedio móvil
            show_moving_avg = st.checkbox("Mostrar promedio móvil")
            moving_avg_window = st.slider("Ventana para promedio móvil:", 1, 30, 7) if show_moving_avg else None

            # Create plot based on selection
            if variable == "Ambas variables":
                st.write("### Temperatura")
                temp_data = df_filtered["temperatura"]
                if chart_type == "Línea":
                    st.line_chart(temp_data)
                elif chart_type == "Área":
                    st.area_chart(temp_data)
                elif chart_type == "Barra":
                    st.bar_chart(temp_data)
                elif chart_type == "Puntos":
                    fig, ax = plt.subplots()
                    ax.scatter(temp_data.index, temp_data, label="Temperatura", color='red')
                    ax.set_xlabel("Fecha")
                    ax.set_ylabel("Temperatura (°C)")
                    ax.set_title("Gráfico de Puntos de Temperatura")
                    st.pyplot(fig)

                if show_moving_avg:
                    st.line_chart(temp_data.rolling(moving_avg_window).mean(), height=150, caption="Promedio móvil")

                st.write("### Humedad")
                hum_data = df_filtered["humedad"]
                if chart_type == "Línea":
                    st.line_chart(hum_data)
                elif chart_type == "Área":
                    st.area_chart(hum_data)
                elif chart_type == "Barra":
                    st.bar_chart(hum_data)
                elif chart_type == "Puntos":
                    fig, ax = plt.subplots()
                    ax.scatter(hum_data.index, hum_data, label="Humedad", color='blue')
                    ax.set_xlabel("Fecha")
                    ax.set_ylabel("Humedad (%)")
                    ax.set_title("Gráfico de Puntos de Humedad")
                    st.pyplot(fig)

                if show_moving_avg:
                    st.line_chart(hum_data.rolling(moving_avg_window).mean(), height=150, caption="Promedio móvil")
            else:
                data = df_filtered[variable]
                if chart_type == "Línea":
                    st.line_chart(data)
                elif chart_type == "Área":
                    st.area_chart(data)
                elif chart_type == "Barra":
                    st.bar_chart(data)
                elif chart_type == "Puntos":
                    fig, ax = plt.subplots()
                    ax.scatter(data.index, data, label=variable, color='green')
                    ax.set_xlabel("Fecha")
                    ax.set_ylabel(variable.capitalize())
                    ax.set_title(f"Gráfico de Puntos de {variable.capitalize()}")
                    st.pyplot(fig)

                if show_moving_avg:
                    st.line_chart(data.rolling(moving_avg_window).mean(), height=150, caption="Promedio móvil")

                # Visualizar máximo y mínimo
                st.metric(f"Valor máximo de {variable}", data.max())
                st.metric(f"Valor mínimo de {variable}", data.min())

            # Raw data display with toggle
            if st.checkbox('Mostrar datos crudos'):
                st.write(df_filtered)

        with tab2:
            st.subheader('Análisis Estadístico')
            
            # Variable selector for statistics
            stat_variable = st.radio(
                "Seleccione variable para estadísticas",
                ["temperatura", "humedad"]
            )
            
            # Statistical summary
            stats_df = df1[stat_variable].describe()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df)
            
            with col2:
                # Additional statistics
                if stat_variable == "temperatura":
                    st.metric("Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                    st.metric("Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                    st.metric("Temperatura Mínima", f"{stats_df['min']:.2f}°C")
                else:
                    st.metric("Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min']:.2f}%")

        with tab3:
            st.subheader('Filtros de Datos')
            
            # Variable selector for filtering
            filter_variable = st.selectbox(
                "Seleccione variable para filtrar",
                ["temperatura", "humedad"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Minimum value filter
                min_val = st.slider(
                    f'Valor mínimo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="min_val"
                )
                
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"Registros con {filter_variable} superior a", 
                        f"{min_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_min)
                
            with col2:
                # Maximum value filter
                max_val = st.slider(
                    f'Valor máximo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="max_val"
                )
                
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"Registros con {filter_variable} inferior a",
                        f"{max_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_max)

            # Download filtered data
            if st.button('Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name='datos_filtrados.csv',
                    mime='text/csv',
                )

        with tab4:
            st.subheader("Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Dirección: Calle 7 sur # 42-06")
                st.write("- Código Postal: 050022")
            
            with col2:
                st.write("### Descripción del Proyecto")
                st.write("Este proyecto recopila datos de sensores de temperatura y humedad en la Universidad EAFIT con el fin de monitorizar las condiciones ambientales. Estos datos serán utilizados para mejorar la eficiencia energética y otros aspectos operacionales del campus.")
                st.write("La aplicación proporciona herramientas para visualizar, analizar y filtrar estos datos de manera eficiente.")
                
    except Exception as e:
        st.error(f'Error al cargar o procesar el archivo CSV: {e}')
