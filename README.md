# Planeador de Rutas Michoacán

Aplicación web ligera para:

- Visualizar municipios en mapa
- Cargar coordenadas UTM desde CSV
- Seleccionar destinos usando `Ctrl + Click`
- Calcular rutas óptimas
- Generar rutas circulares:

```txt
Origen → destinos → regreso al origen
```

- Mostrar información personalizada al hacer click sobre cada punto

La aplicación funciona completamente en el navegador usando:

- HTML
- JavaScript
- Leaflet
- OSRM
- Proj4
- PapaParse

---

# Características

## Coordenadas UTM

Soporta:

- EPSG:32614 (UTM 14N)
- EPSG:32613 (UTM 13N)

Convierte automáticamente:

```txt
UTM → Latitud/Longitud
```

---

# Selección de destinos

## Click normal

Muestra información del punto.

## Ctrl + Click

Selecciona o quita destinos para la ruta.

En Mac:

```txt
Cmd + Click
```

---

# Ruta circular

La aplicación calcula:

```txt
Origen → destinos → origen
```

---

# Optimización de ruta

## Hasta 8 destinos

Prueba todas las combinaciones posibles.

## Más de 8 destinos

Usa algoritmo aproximado tipo:

```txt
Nearest Neighbor
```

para evitar congelar el navegador.

---

# Configuración externa

Toda la configuración principal está en:

```txt
config.txt
```

Esto permite modificar:

- origen
- CSV por defecto
- columnas
- zona UTM
- columnas del popup

sin tocar el HTML.

---

# Estructura del proyecto

```txt
proyecto/
│
├── index.html
├── config.txt
├── municipios.csv
└── README.md
```

---

# Ejemplo de `config.txt`

```txt
CSV_DEFAULT=municipios.csv

ORIGEN_NOMBRE=Mi origen
ORIGEN_ESTE=275000
ORIGEN_NORTE=2180000
ORIGEN_EPSG=EPSG:32614

COLUMNA_MUNICIPIO=NOMBRE
COLUMNA_ESTE=METROS ESTE
COLUMNA_NORTE=METROS NORTE
ZONA_CSV=EPSG:32614

COLUMNAS_POPUP=NOMBRE,METROS ESTE,METROS NORTE
```

---

# Formato esperado del CSV

Ejemplo:

```csv
NOMBRE,METROS ESTE,METROS NORTE
Morelia,289000,2189000
Uruapan,245000,2145000
Zamora,220000,2230000
```

---

# Ejecutar el proyecto

## Requisitos

Tener Python instalado.

---

# Iniciar servidor local

Desde la carpeta del proyecto:

```bash
python -m http.server 8000
```

o:

```bash
python3 -m http.server 8000
```

---

# Abrir en navegador

```txt
http://localhost:8000
```

---

# Uso

## 1. Abrir aplicación

La app cargará automáticamente:

- `config.txt`
- CSV por defecto

---

## 2. Ver información

```txt
Click normal sobre un pin
```

---

## 3. Seleccionar destinos

```txt
Ctrl + Click
```

Los puntos seleccionados se vuelven rojos.

---

## 4. Calcular ruta

Presiona:

```txt
Calcular ruta circular
```

---

# Tecnologías utilizadas

## Leaflet

Mapa interactivo.

## OSRM

Cálculo de rutas reales por carretera.

API pública:

```txt
https://router.project-osrm.org
```

## Proj4js

Conversión UTM → Lat/Lon.

## PapaParse

Lectura de CSV.

---

# Personalización

## Cambiar origen

Editar:

```txt
config.txt
```

```txt
ORIGEN_NOMBRE=
ORIGEN_ESTE=
ORIGEN_NORTE=
```

---

# Cambiar columnas popup

```txt
COLUMNAS_POPUP=NOMBRE,POBLACION,REGION
```

---

# Cambiar CSV por defecto

```txt
CSV_DEFAULT=otro.csv
```

---

# Limitaciones

## OSRM público

La API pública tiene límites de uso.

Para proyectos grandes se recomienda:

- servidor OSRM propio
- GraphHopper
- Google Maps API
- Mapbox Directions API

---

# Mejoras futuras sugeridas

- Exportar ruta a PDF
- Exportar a Excel
- Guardar rutas favoritas
- Optimización avanzada TSP
- Filtros por región
- Búsqueda rápida
- Clusterización de puntos
- Modo oscuro
- Cálculo de combustible
- Restricciones por horario
- Multiusuario

---

# Licencia

Uso libre para proyectos personales o internos.