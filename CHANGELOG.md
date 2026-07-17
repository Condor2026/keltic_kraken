# 📋 CHANGELOG - KELTIC KRAKEN

## [4.1.0] - 2026-07-18

### ✨ AÑADIDO

- **🌍 Mapa Globo 3D interactivo** - Con MapLibre GL, vista global completa
- **⛶ Pantalla completa** - Expansión a todo el navegador con un solo click
- **🎯 Popups autocerrantes** - Al hacer click en otro punto, el anterior se cierra
- **🔗 Enlaces funcionales** - Click en cualquier título abre la fuente original
- **🎮 Botones 100% funcionales** - Todos los controles del mapa funcionan correctamente
- **📊 Dashboard interactivo** - Gráficos en tiempo real con Chart.js
- **🔍 Búsqueda en tiempo real** - Filtra crímenes mientras escribes
- **📄 Paginación mejorada** - 15 crímenes por página con navegación fluida
- **🔧 Reparación de datos** - Función automática que asigna coordenadas y colores a los crímenes guardados
- **🧹 Limpieza de duplicados** - Elimina registros repetidos automáticamente
- **📥 Exportación HTML** - Genera reportes profesionales con estadísticas

### 🔧 MEJORADO

- **Límite de puntos en el mapa** - Aumentado de 500 a 3000 puntos simultáneos
- **Colores de los puntos** - Ahora cada tipo de crimen tiene su color único:
  - 🔴 Drug Trafficking - `#ff0000`
  - 🔫 Gang Violence - `#ff4444`
  - 💀 Murder/Homicide - `#000000`
  - 👊 Assault - `#ff8c00`
  - 💰 Robbery/Theft - `#ffd700`
  - 🕴️ Organized Crime - `#800080`
  - 👮 Garda Operation - `#0066cc`
  - 🔪 Weapon Offense - `#990000`
- **Menú principal** - Nueva opción 12 para reparar datos existentes
- **Banner de inicio** - ASCII art actualizado con diseño mejorado
- **Coordenadas** - Asignación automática de coordenadas a crímenes sin ubicación

### 🐛 CORREGIDO

- **Error de visualización** - Los crímenes guardados ahora aparecen correctamente en el mapa
- **Colores inconsistentes** - Todos los puntos tienen el color correcto según su tipo
- **Límite de puntos** - Ya no se ocultan crímenes por el límite de 500
- **Coordenadas faltantes** - Los crímenes antiguos ahora tienen coordenadas asignadas automáticamente

---

## [3.4.0] - 2026-06-12

### ✨ AÑADIDO

- **Auto-discovery system** - Busca URLs alternativas automáticamente
- **180+ User-Agents** - Rotación completa anti-bloqueo
- **Gráficos interactivos** - Dashboard con Chart.js (barras, dona, línea, ranking)
- **Soporte bilingüe** - Español e Inglés completos
- **Exportación HTML** - Reportes profesionales con gráficos
- **Cache de URLs** - Guarda URLs encontradas para futuras ejecuciones
- **Estadísticas avanzadas** - Keywords, densidad, tendencia

### 🔧 MEJORADO

- Anti-bloqueo con delays aleatorios
- Verificación de fuentes con reintentos
- Parsing HTML con múltiples selectores
- Memoria optimizada para grandes datasets
- URLs actualizadas para 2026

### 🐛 CORREGIDO

- URLs rotas (404) con auto-discovery
- Errores 403 con headers rotativos
- Duplicados en la base de datos
- Timeouts controlados sin bloqueos

---

## [3.0.0] - 2026-06-01

### ✨ AÑADIDO

- **Mapa 3D** - Visualización interactiva con MapLibre GL
- **Puntos interactivos** - Click en puntos para ver detalles
- **Tooltips con severidad** - Información en tiempo real
- **32 condados** - Cobertura completa de toda Irlanda
- **Dashboard web** - Panel de control con Flask
- **Exportación JSON y CSV** - Datos en múltiples formatos

### 🔧 MEJORADO

- Refactorización completa del código
- Manejo de errores mejorado
- Sistema de logging avanzado

---

## [2.0.0] - 2026-05-20

### ✨ AÑADIDO

- 85+ fuentes irlandesas
- Detección de patrones criminales
- Clasificación inteligente de crímenes
- Estadísticas por condado y tipo

---

## [1.0.0] - 2026-05-15

### ✨ AÑADIDO

- Lanzamiento inicial
- Scraping básico de noticias
- Menú en terminal interactivo
- Persistencia de datos en JSON
- Detección básica de crímenes

---

## 📊 Leyenda de Versiones

| Versión | Fecha | Estado |
|---------|-------|--------|
| **4.1.0** | 2026-07-18 | ✅ Estable - Actual |
| 3.4.0 | 2026-06-12 | ✅ Estable |
| 3.0.0 | 2026-06-01 | ✅ Estable |
| 2.0.0 | 2026-05-20 | ⚠️ Descontinuado |
| 1.0.0 | 2026-05-15 | ⚠️ Descontinuado |

---

## 🚀 Próximas Mejoras (v4.2)

- [ ] Sistema de alertas en tiempo real
- [ ] Notificaciones por email
- [ ] API REST completa
- [ ] Dockerización optimizada
- [ ] Plugin para navegadores
- [ ] Integración con Telegram
- [ ] Análisis predictivo de crímenes
- [ ] Mapa de calor dinámico
```

## 📝 RESUMEN DE CAMBIOS:

| Elemento | Antes | Ahora |
|----------|-------|-------|
| **Versión** | 3.4.0 | **4.1.0** |
| **Fecha** | 2026-06-12 | **2026-07-18** |
| **Sección v4.1** | No existía | **AÑADIDA** |
| **Características** | Básicas | **+20 nuevas** |
| **Colores** | No especificados | **Detallados por tipo** |
| **Límite mapa** | 500 | **3000** |
| **Botones mapa** | Funcionalidad limitada | **100% funcionales** |
| **Leyenda** | No existía | **AÑADIDA** |
| **Próximas mejoras** | No existía | **AÑADIDA** |
