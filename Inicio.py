import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
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
                ["Línea", "Área", "Barra"]
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
                else:
                    st.bar_chart(temp_data)

                if show_moving_avg:
                    st.line_chart(temp_data.rolling(moving_avg_window).mean(), height=150, caption="Promedio móvil")

                st.write("### Humedad")
                hum_data = df_filtered["humedad"]
                if chart_type == "Línea":
                    st.line_chart(hum_data)
                elif chart_type == "Área":
                    st.area_chart(hum_data)
                else:
                    st.bar_chart(hum_data)

                if show_moving_avg:
                    st.line_chart(hum_data.rolling(moving_avg_window).mean(), height=150, caption="Promedio móvil")
            else:
                data = df_filtered[variable]
                if chart_type == "Línea":
                    st.line_chart(data)
                elif chart_type == "Área":
                    st.area_chart(data)
                else:
                    st.bar_chart(data)

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
                    st.metric("Temperatura Mediana", f"{df1[stat_variable].median():.2f}°C")
                    st.metric("Desviación estándar", f"{df1[stat_variable].std():.2f}°C")
                    st.metric("Temperatura 75 Percentil", f"{np.percentile(df1[stat_variable], 75):.2f}°C")
                    st.metric("Temperatura 25 Percentil", f"{np.percentile(df1[stat_variable], 25):.2f}°C")
                else:
                    st.metric("Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min']:.2f}%")
                    st.metric("Humedad Mediana", f"{df1[stat_variable].median():.2f}%")
                    st.metric("Desviación estándar", f"{df1[stat_variable].std():.2f}%")
                    st.metric("Humedad 75 Percentil", f"{np.percentile(df1[stat_variable], 75):.2f}%")
                    st.metric("Humedad 25 Percentil", f"{np.percentile(df1[stat_variable], 25):.2f}%")
                
                # Display histogram for the selected variable
                st.write(f"### Distribución de {stat_variable.capitalize()}")
                st.bar_chart(df1[stat_variable].value_counts())
                
                # Add a table with points (puntos de la variable)
                st.write(f"### Tabla de Puntos para {stat_variable.capitalize()}")
                points_df = df1[stat_variable].reset_index()[['Time', stat_variable]]
                st.dataframe(points_df)

                # Add a line chart to show the evolution over time
                st.write(f"### Evolución de {stat_variable.capitalize()} a lo largo del tiempo")
                st.line_chart(df1[stat_variable])


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

            # New Filters
            with col1:
                # Range Filter for Specific Interval
                range_min = st.slider(
                    f"Valor mínimo de {filter_variable} en intervalo",
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()) - 5,
                    key="range_min"
                )
                range_max = st.slider(
                    f"Valor máximo de {filter_variable} en intervalo",
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()) + 5,
                    key="range_max"
                )
                filtered_interval_df = df1[
                    (df1[filter_variable] >= range_min) & (df1[filter_variable] <= range_max)
                ]
                st.write(f"Registros en el intervalo de {filter_variable}:", f"{range_min} a {range_max}")
                st.dataframe(filtered_interval_df)

       
        with tab4:
            st.subheader("Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Altitud: ~1,495 metros sobre el nivel del mar")
            
            with col2:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variables medidas:")
                st.write("  * Temperatura (°C)")
                st.write("  * Humedad (%)")
                st.write("- Frecuencia de medición: Según configuración")
                st.write("- Ubicación: Campus universitario")

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
