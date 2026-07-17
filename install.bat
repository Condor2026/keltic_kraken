@echo off
title 🦈 KELTIC KRAKEN v4.1 - INSTALLER
color 0C

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║   🦈 KELTIC KRAKEN v4.1 - INSTALLER                           ║
echo ║   Ireland Crime Intelligence Platform                         ║
echo ║                                                               ║
echo ║   "With great power comes great responsibility"               ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

:: ============================================
:: VERIFICAR PYTHON
:: ============================================
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo.
    echo Descarga Python 3.8+ desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

:: ============================================
:: VERIFICAR PIP
:: ============================================
echo [2/5] Verificando PIP...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PIP no encontrado
    echo Instalando PIP...
    python -m ensurepip --upgrade
)

echo [OK] PIP encontrado
echo.

:: ============================================
:: ACTUALIZAR PIP
:: ============================================
echo [3/5] Actualizando PIP...
pip install --upgrade pip
echo.

:: ============================================
:: INSTALAR DEPENDENCIAS
:: ============================================
echo [4/5] Instalando dependencias...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt no encontrado
    echo Instalando dependencias minimas...
    pip install requests beautifulsoup4 flask flask-cors
)
echo.

:: ============================================
:: VERIFICAR INSTALACION
:: ============================================
echo [5/5] Verificando instalacion...
python -c "import requests, bs4, flask" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Algunas dependencias no se instalaron correctamente
    echo Intenta: pip install requests beautifulsoup4 flask
) else (
    echo [OK] Todas las dependencias instaladas correctamente
)
echo.

:: ============================================
:: CREAR ARCHIVOS DE CONFIGURACION
:: ============================================
if not exist .env (
    echo [INFO] Creando archivo .env de ejemplo...
    copy env.example .env >nul 2>&1
    echo [OK] .env creado (ajusta las variables si es necesario)
)
echo.

:: ============================================
:: CREAR CARPETAS
:: ============================================
if not exist data (
    mkdir data
    echo [OK] Carpeta data creada
)
if not exist logs (
    mkdir logs
    echo [OK] Carpeta logs creada
)
echo.

:: ============================================
:: MENSAJE FINAL
:: ============================================
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║   ✅ INSTALACION COMPLETADA!                                  ║
echo ║                                                               ║
echo ║   Para ejecutar: python keltic_kraken.py                      ║
echo ║                                                               ║
echo ║   🌐 Web Dashboard: http://localhost:5019                     ║
echo ║                                                               ║
echo ║   🦈 KELTIC KRAKEN v4.1 - Ready to monitor Ireland's crime    ║
echo ║                                                               ║
echo ║   "With great power comes great responsibility"               ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Archivos generados:
echo   📁 data/         - Datos persistentes
echo   📁 logs/         - Archivos de log
echo   📄 .env          - Variables de entorno (ajusta si quieres)
echo.
pause
```

## 📝 CAMBIOS PRINCIPALES:

| Elemento | v3.0 | v4.1 |
|----------|------|------|
| **Versión** | KELTIC KRAKEN | **🦈 KELTIC KRAKEN v4.1** |
| **Color** | 0C (rojo) | **0C (rojo)** |
| **Pasos** | 3 | **5** |
| **Verificación PIP** | No | **Sí** |
| **Creación .env** | No | **Sí** |
| **Creación carpetas** | No | **data/ y logs/** |
| **Verificación final** | No | **Sí** |
| **Puerto** | No | **5019** |
| **Mensaje Spider-Man** | No | **Sí** |

## 🎯 NUEVAS CARACTERÍSTICAS:

1. **Verificación de PIP** - Comprueba que pip esté instalado
2. **Creación automática de .env** - Copia desde env.example
3. **Creación de carpetas** - data/ y logs/ para persistencia
4. **Verificación final** - Comprueba que todo funcione
5. **Mensaje de Spider-Man** - "With great power..."
