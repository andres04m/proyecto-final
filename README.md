# citydata

# 📊 Análisis de Sensores - Mi Ciudad

Una aplicación web desarrollada con Streamlit para visualizar y analizar datos de sensores de temperatura y humedad ubicados en la Universidad EAFIT, Medellín.

## 📋 Descripción

Esta aplicación permite analizar datos de temperatura y humedad recolectados por sensores ESP32 distribuidos en diferentes puntos de la universidad. La aplicación proporciona visualizaciones interactivas, análisis estadísticos y funcionalidades de filtrado de datos.

## ✨ Características

- 📈 Visualización de datos de temperatura y humedad
  - Gráficos de línea, área y barras
  - Visualización individual o conjunta de variables
- 📊 Análisis estadístico detallado
  - Estadísticas descriptivas
  - Métricas clave (promedios, máximos, mínimos)
- 🔍 Filtros de datos personalizables
  - Filtrado por rangos de temperatura y humedad
  - Exportación de datos filtrados
- 🗺️ Visualización de ubicación de sensores
  - Mapa interactivo con ubicaciones de sensores
  - Información detallada del sitio de medición

## 🚀 Instalación

1. Clone este repositorio:
```bash
git clone https://github.com/your-username/analisis-sensores-ciudad.git
cd analisis-sensores-ciudad
```

2. Instale las dependencias requeridas:
```bash
pip install -r requirements.txt
```

3. Ejecute la aplicación:
```bash
streamlit run app.py
```

## 📦 Dependencias

- Python 3.7+
- streamlit
- pandas
- PIL
- numpy
- datetime

## 📁 Formato de Datos

La aplicación espera archivos CSV con el siguiente formato:

- Columna de tiempo: 'Time'
- Columnas de datos:
  - 'temperatura {device="ESP32", name="Sensor 1"}'
  - 'humedad {device="ESP32", name="Sensor 1"}'

## 🛠️ Uso

1. Inicie la aplicación
2. Cargue un archivo CSV con los datos de los sensores obtenidos de la plataforma grafana, combinando los datos
3. Utilice las diferentes pestañas para:
   - Visualizar los datos en diferentes tipos de gráficos
   - Ver estadísticas descriptivas
   - Aplicar filtros a los datos
   - Consultar información sobre la ubicación de los sensores

## 📍 Ubicación

- Universidad EAFIT
- Medellín, Colombia
- Coordenadas: 6.2006, -75.5783
- Altitud: ~1,495 metros sobre el nivel del mar

## 👥 Contribución

Si desea contribuir al proyecto:

1. Haga un Fork del repositorio
2. Cree una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Realice sus cambios y haga commit (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Cree un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia CC.

## 🤝 Contacto

Para preguntas o sugerencias, por favor abra un issue en este repositorio.

---
Desarrollado para el análisis de datos de sensores urbanos en la Universidad EAFIT.
