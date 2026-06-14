#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Condor2026 / SpectrumSecurity

"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  🔪 KELTIC KRAKEN v3.0 - IRELAND CRIME INTELLIGENCE PLATFORM                                                  ║
║  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ ║
║  📊 Real-time monitoring: Drug trafficking · Gang violence · Organized crime                                  ║
║  🏴 Covers ALL 32 counties including Northern Ireland                                                         ║
║  🔄 180+ Rotating User-Agents · Auto-URL discovery · Anti-blocking system                                     ║
║  📈 Interactive charts · Full statistics dashboard · Web interface                                            ║
║  🔍 Smart retry mechanism · URL cache · Session persistence                                                   ║
║  📄 Pagination in web panel · Save after each source · Duplicate removal                                      ║
║                                                                                                               ║
║  🛡️ "Un gran poder conlleva una gran responsabilidad" - Spider-Man                                            ║
║                                                                                                               ║
║                                         - By Condor2026                                                       ║
║                                         •SpectrumSecurity•                                                    ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import random
import requests
import re
import csv
import io
import signal
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, Response
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import Lock

# ============================================================================
# ============================================================================
# LANGUAGE SELECTOR WITH BEAUTIFUL INTERFACE - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

IDIOMA_ACTUAL = None

def mostrar_banner_idioma():
    print(f"""
{Color.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🔪 KELTIC KRAKEN v{VERSION} - IRELAND CRIME INTELLIGENCE                ║
║                                                                    ║
║   "Vigilamos para proteger, no para señalar. Datos públicos,       ║
║    ética inquebrantable, transparencia absoluta."                  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Color.RESET}""")

def mostrar_menu_idioma():
    print(f"\n{Color.YELLOW}┌{'─' * 50}┐{Color.RESET}")
    print(f"{Color.YELLOW}│{Color.CYAN}  🌍 SELECCIONE IDIOMA / SELECT LANGUAGE{' ' * 10}{Color.YELLOW}│{Color.RESET}")
    print(f"{Color.YELLOW}├{'─' * 50}┤{Color.RESET}")
    print(f"{Color.YELLOW}│{Color.GREEN}  [1] Español                                     {Color.YELLOW}│{Color.RESET}")
    print(f"{Color.YELLOW}│{Color.GREEN}  [2] English                                     {Color.YELLOW}│{Color.RESET}")
    print(f"{Color.YELLOW}└{'─' * 50}┘{Color.RESET}")

def seleccionar_idioma():
    global IDIOMA_ACTUAL
    mostrar_banner_idioma()
    mostrar_menu_idioma()
    
    while True:
        opc = input(f"\n{Color.CYAN}➤ {Color.YELLOW}Opción / Option: {Color.RESET}")
        if opc == '1':
            IDIOMA_ACTUAL = 'es'
            print(f"\n{Color.GREEN}✅ Idioma: Español seleccionado{Color.RESET}")
            break
        elif opc == '2':
            IDIOMA_ACTUAL = 'en'
            print(f"\n{Color.GREEN}✅ Language: English selected{Color.RESET}")
            break
        else:
            print(f"{Color.RED}❌ Opción inválida / Invalid option{Color.RESET}")
    
    time.sleep(0.5)

TEXTOS = {
    'es': {
        'app_name': '🔪 KELTIC KRAKEN v3.0',
        'welcome_title': 'PLATAFORMA DE INTELIGENCIA CRIMINAL DE IRLANDA',
        'elegir_idioma': 'Seleccione idioma: 1. Español  2. English',
        'menu_title': 'MENÚ PRINCIPAL',
        'cmd_buscar': 'Buscar crímenes (auto-detección URLs)',
        'cmd_analisis': 'Análisis completo con gráficos',
        'cmd_conexiones': 'Patrones y conexiones entre incidentes',
        'cmd_evolucion': 'Evolución mensual detallada',
        'cmd_web': 'Iniciar servidor web (dashboard con gráficos)',
        'cmd_ultimos': 'Últimos 20 incidentes registrados',
        'cmd_exportar': 'Exportar datos (JSON/CSV/HTML)',
        'cmd_verificar': 'Verificar/actualizar fuentes (auto-discovery)',
        'cmd_tipos': 'Distribución por tipo de crimen',
        'cmd_estadisticas': 'Estadísticas avanzadas',
        'cmd_limpiar': 'Limpiar base de datos duplicados',
        'cmd_salir': 'Salir de la aplicación',
        'stats_total': 'Total incidentes',
        'incidentes': 'incidentes',
        'fuentes': 'fuentes activas',
        'condados': 'condados afectados',
        'servidor_web': 'Servidor web iniciado',
        'presiona_ctrl_c': 'Presiona Ctrl+C para volver al menú',
        'hasta_pronto': '¡Hasta pronto! Gracias por usar KELTIC KRAKEN',
        'opcion_invalida': 'Opción no válida, intenta de nuevo',
        'actualizando': 'ACTUALIZANDO DATOS DE CRIMEN EN IRLANDA',
        'analisis_completo': 'ANÁLISIS COMPLETO DEL CRIMEN EN IRLANDA',
        'conexiones': 'PATRONES Y CONEXIONES ENTRE INCIDENTES',
        'evolucion_mensual': 'EVOLUCIÓN MENSUAL DE INCIDENTES',
        'exportando': 'EXPORTANDO DATOS',
        'verificando': 'VERIFICANDO FUENTES IRLANDESAS',
        'limpiando': 'LIMPIANDO BASE DE DATOS',
        'estadisticas_avanzadas': 'ESTADÍSTICAS AVANZADAS',
        'error_conexion': 'Error de conexión con la fuente',
        'sin_datos': 'No hay datos suficientes para mostrar',
        'procesando': 'Procesando...'
    },
    'en': {
        'app_name': '🔪 KELTIC KRAKEN v3.0',
        'welcome_title': 'IRELAND CRIMINAL INTELLIGENCE PLATFORM',
        'elegir_idioma': 'Select language: 1. Spanish  2. English',
        'menu_title': 'MAIN MENU',
        'cmd_buscar': 'Search crimes (auto-discover URLs)',
        'cmd_analisis': 'Full analysis with charts',
        'cmd_conexiones': 'Patterns and connections between incidents',
        'cmd_evolucion': 'Detailed monthly evolution',
        'cmd_web': 'Start web server (dashboard with charts)',
        'cmd_ultimos': 'Last 20 registered incidents',
        'cmd_exportar': 'Export data (JSON/CSV/HTML)',
        'cmd_verificar': 'Verify/update sources (auto-discovery)',
        'cmd_tipos': 'Distribution by crime type',
        'cmd_estadisticas': 'Advanced statistics',
        'cmd_limpiar': 'Clean duplicate database entries',
        'cmd_salir': 'Exit application',
        'stats_total': 'Total incidents',
        'incidentes': 'incidents',
        'fuentes': 'active sources',
        'condados': 'affected counties',
        'servidor_web': 'Web server started',
        'presiona_ctrl_c': 'Press Ctrl+C to return to menu',
        'hasta_pronto': 'Goodbye! Thanks for using KELTIC KRAKEN',
        'opcion_invalida': 'Invalid option, try again',
        'actualizando': 'UPDATING IRELAND CRIME DATA',
        'analisis_completo': 'COMPLETE CRIME ANALYSIS FOR IRELAND',
        'conexiones': 'PATTERNS AND CONNECTIONS BETWEEN INCIDENTS',
        'evolucion_mensual': 'MONTHLY INCIDENT EVOLUTION',
        'exportando': 'EXPORTING DATA',
        'verificando': 'VERIFYING IRISH SOURCES',
        'limpiando': 'CLEANING DATABASE',
        'estadisticas_avanzadas': 'ADVANCED STATISTICS',
        'error_conexion': 'Connection error with source',
        'sin_datos': 'Insufficient data to display',
        'procesando': 'Processing...'
    }
}

def t(clave):
    return TEXTOS[IDIOMA_ACTUAL].get(clave, clave)

# ============================================================================
# ============================================================================
# COLORES PROFESIONALES PARA TERMINAL - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

class Color:
    BLACK = '\033[30m'
    RED = '\033[91m'
    DARK_RED = '\033[31m'
    GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'
    YELLOW = '\033[93m'
    DARK_YELLOW = '\033[33m'
    BLUE = '\033[94m'
    DARK_BLUE = '\033[34m'
    MAGENTA = '\033[95m'
    DARK_MAGENTA = '\033[35m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    LIGHT_GRAY = '\033[37m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    RESET = '\033[0m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_GRAY = '\033[100m'
    BG_DARK_RED = '\033[101m'
    BG_DARK_GREEN = '\033[102m'
    BG_DARK_YELLOW = '\033[103m'
    BG_DARK_BLUE = '\033[104m'
    BG_DARK_MAGENTA = '\033[105m'
    BG_DARK_CYAN = '\033[106m'

def cprint(texto, color=None, bold=False, dim=False, italic=False, underline=False, blink=False, bg=False, end='\n'):
    styles = []
    if bold:
        styles.append(Color.BOLD)
    if dim:
        styles.append(Color.DIM)
    if italic:
        styles.append(Color.ITALIC)
    if underline:
        styles.append(Color.UNDERLINE)
    if blink:
        styles.append(Color.BLINK)
    
    color_map = {
        'black': Color.BLACK, 'red': Color.RED, 'dark_red': Color.DARK_RED,
        'green': Color.GREEN, 'dark_green': Color.DARK_GREEN, 'yellow': Color.YELLOW,
        'dark_yellow': Color.DARK_YELLOW, 'blue': Color.BLUE, 'dark_blue': Color.DARK_BLUE,
        'magenta': Color.MAGENTA, 'dark_magenta': Color.DARK_MAGENTA, 'cyan': Color.CYAN,
        'dark_cyan': Color.DARK_CYAN, 'white': Color.WHITE, 'gray': Color.GRAY,
        'light_gray': Color.LIGHT_GRAY
    }
    
    bg_map = {
        'black': Color.BG_BLACK, 'red': Color.BG_RED, 'green': Color.BG_GREEN,
        'yellow': Color.BG_YELLOW, 'blue': Color.BG_BLUE, 'magenta': Color.BG_MAGENTA,
        'cyan': Color.BG_CYAN, 'white': Color.BG_WHITE, 'gray': Color.BG_GRAY,
        'dark_red': Color.BG_DARK_RED, 'dark_green': Color.BG_DARK_GREEN,
        'dark_yellow': Color.BG_DARK_YELLOW, 'dark_blue': Color.BG_DARK_BLUE,
        'dark_magenta': Color.BG_DARK_MAGENTA, 'dark_cyan': Color.BG_DARK_CYAN
    }
    
    col = color_map.get(color, '')
    bg_col = bg_map.get(bg if isinstance(bg, str) else None, '') if bg else ''
    
    style_str = ''.join(styles)
    print(f"{bg_col}{style_str}{col}{texto}{Color.RESET}", end=end)

# ============================================================================
# ============================================================================
# CONFIGURACIÓN DEL SISTEMA - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

VERSION = "3.0"
PUERTO = 5014
ARCHIVO_DATOS = 'keltic_kraken_ireland.json'
ARCHIVO_CACHE = 'url_cache_ireland.json'
ARCHIVO_ESTADO = 'estado_fuentes_ireland.json'
ARCHIVO_BACKUP = 'keltic_kraken_backup.json'
PAGINAS_BUSQUEDA = 4
TIMEOUT = 15
MAX_INTENTOS = 2
DELAY_MIN = 0.8
DELAY_MAX = 2.0
ITEMS_POR_PAGINA = 10

# ============================================================================
# ============================================================================
# 180+ USER-AGENTS MODERNOS - VERSIÓN COMPLETA SIN RECORTES
# ============================================================================
# ============================================================================

USER_AGENTS = [
    # ========================================================================
    # CHROME WINDOWS - VERSIONES 118 A 125
    # ========================================================================
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.42 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.129 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36',
    
    # ========================================================================
    # CHROME MAC - VERSIONES 118 A 125
    # ========================================================================
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.42 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.62 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.129 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    
    # ========================================================================
    # FIREFOX WINDOWS - VERSIONES 115 A 126
    # ========================================================================
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0b9',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0.2',
    
    # ========================================================================
    # FIREFOX MAC - VERSIONES 115 A 126
    # ========================================================================
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:115.0) Gecko/20100101 Firefox/115.0',
    
    # ========================================================================
    # FIREFOX LINUX - VERSIONES 118 A 126
    # ========================================================================
    'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0',
    
    # ========================================================================
    # SAFARI MAC - VERSIONES 16 Y 17
    # ========================================================================
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
    
    # ========================================================================
    # EDGE WINDOWS - VERSIONES 118 A 125
    # ========================================================================
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36 Edg/125.0.6422.60',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.42 Safari/537.36 Edg/125.0.6422.42',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36 Edg/124.0.6367.118',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36 Edg/124.0.6367.91',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.62 Safari/537.36 Edg/124.0.6367.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36 Edg/123.0.6312.122',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
    
    # ========================================================================
    # OPERA - VERSIONES 106 A 110
    # ========================================================================
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36 OPR/110.0.5322.60',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36 OPR/109.0.5322.118',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/108.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/107.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/109.0.0.0',
    
    # ========================================================================
    # IPHONE SAFARI - iOS 16 Y 17
    # ========================================================================
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
    
    # ========================================================================
    # IPAD SAFARI - iOS 16 Y 17
    # ========================================================================
    'Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
    
    # ========================================================================
    # ANDROID CHROME - ANDROID 12, 13, 14
    # ========================================================================
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    
    # ========================================================================
    # ANDROID FIREFOX - ANDROID 12, 13, 14
    # ========================================================================
    'Mozilla/5.0 (Android 14; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0',
    'Mozilla/5.0 (Android 12; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0',
    'Mozilla/5.0 (Android 12; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
    'Mozilla/5.0 (Android 12; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
    
    # ========================================================================
    # CHROME LINUX - VERSIONES 118 A 125
    # ========================================================================
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.129 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    
    # ========================================================================
    # SEARCH ENGINE BOTS (útiles para evitar bloqueos)
    # ========================================================================
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Facebookbot/1.0; +http://www.facebook.com/bot)',
    'Mozilla/5.0 (compatible; Twitterbot/1.0)',
    'Mozilla/5.0 (compatible; Applebot/0.3; +http://www.apple.com/go/applebot)',
    
    # ========================================================================
    # LEGACY BROWSERS (a veces funcionan mejor en sitios viejos)
    # ========================================================================
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    
    # ========================================================================
    # EXTRA - SAMSUNG INTERNET, BRAVE, VIVALDI
    # ========================================================================
    'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Brave/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Vivaldi/6.6.0.0',
]

def get_random_ua():
    """Retorna un User-Agent aleatorio de la lista de 180+"""
    return random.choice(USER_AGENTS)

def get_random_delay():
    """Retorna un delay aleatorio entre DELAY_MIN y DELAY_MAX"""
    return random.uniform(DELAY_MIN, DELAY_MAX)

# ============================================================================
# ============================================================================
# SISTEMA DE AUTO-DESCOBRIMIENTO DE URLs - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

class URLAutoDiscoverer:
    """
    Sistema inteligente que busca automáticamente las URLs correctas
    cuando una fuente está caída o ha cambiado de estructura.
    """
    
    def __init__(self):
        self.cache_file = ARCHIVO_CACHE
        self.cache = self.load_cache()
        self.common_paths = [
            # ================================================================
            # Crime section paths - paths principales de secciones de crimen
            # ================================================================
            'crime', 'crimes', 'news/crime', 'crime-news', 'crime-law',
            'courts', 'justice', 'irish-news/crime', 'category/crime',
            'crime/cork', 'crime/dublin', 'crime/galway', 'crime/limerick',
            'news/crime-and-courts', 'news/justice', 'northern-ireland/crime',
            'crime-ireland', 'irish-crime', 'crime-scene', 'crime-watch',
            'criminal-justice', 'law-and-order', 'garda-news', 'police-news',
            'breaking-crime', 'latest-crime', 'crime-updates', 'crime-stories',
            'court-reports', 'trial-news', 'sentencing', 'arrest-news',
            'drug-seizure', 'gang-crime', 'organised-crime', 'paramilitary',
            
            # ================================================================
            # Pagination patterns - patrones de paginación
            # ================================================================
            'page', 'pagina', 'pagination', 'archive', 'category',
            
            # ================================================================
            # Common CMS patterns - patrones comunes de CMS
            # ================================================================
            '?cat=crime', '?category=crime', '?section=crime', '?topic=crime',
            '#crime', '/crime/', '/crimen', '/criminal', '/delitos',
            '/sucesos', '/faits-divers', '/noticias-crimen'
        ]
        
    def load_cache(self):
        """Carga el caché de URLs encontradas previamente"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_cache(self):
        """Guarda el caché de URLs para futuras ejecuciones"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def discover_url(self, fuente):
        """
        Intenta descubrir la URL correcta para una fuente.
        Retorna la URL encontrada o la original si no se encuentra nada.
        """
        nombre = fuente['nombre']
        base_url = fuente['base']
        original_url = fuente['url']
        
        # ====================================================================
        # Verificar caché primero - si ya encontramos esta URL antes
        # ====================================================================
        if nombre in self.cache and self.cache[nombre].get('url'):
            cached_url = self.cache[nombre]['url']
            cprint(f"   📦 Cache encontrada: {cached_url}", 'gray', dim=True)
            
            # Verificar que la URL cacheada aún funciona
            try:
                headers = {'User-Agent': get_random_ua(), 'Accept-Language': 'en-US,en;q=0.9'}
                r = requests.get(cached_url, timeout=10, headers=headers)
                if r.status_code == 200:
                    return cached_url
                else:
                    cprint(f"   ⚠️ Cache obsoleta (HTTP {r.status_code})", 'yellow')
            except:
                cprint(f"   ⚠️ Cache obsoleta (error de conexión)", 'yellow')
        
        # ====================================================================
        # Probar diferentes paths - búsqueda exhaustiva
        # ====================================================================
        cprint(f"   🔍 Buscando URL alternativa...", 'cyan', dim=True)
        
        for path in self.common_paths:
            # Probar diferentes combinaciones de URL
            urls_to_try = [
                f"{base_url}/{path}" if not base_url.endswith('/') else f"{base_url}{path}",
                f"{base_url}/{path}/",
                f"{base_url}/{path}.html",
                f"{base_url}/index.php?category={path}",
                f"{base_url}/?s={path}",
                f"{base_url}/search?q={path}",
                f"{base_url}/tag/{path}",
                f"{base_url}/topic/{path}",
                f"{base_url}/section/{path}",
                f"{base_url}/category/{path}",
                f"{base_url}/archives/category/{path}",
                f"{base_url}/news/{path}",
                f"{base_url}/local/{path}",
                f"{base_url}/ireland/{path}",
                f"{base_url}/national/{path}",
            ]
            
            for test_url in urls_to_try[:5]:  # Limitar a 5 intentos por path
                try:
                    headers = {'User-Agent': get_random_ua(), 'Accept-Language': 'en-US,en;q=0.9'}
                    r = requests.get(test_url, timeout=15, headers=headers)
                    
                    if r.status_code == 200:
                        # Verificar que la página contiene contenido relevante
                        soup = BeautifulSoup(r.text, 'html.parser')
                        page_text = soup.get_text().lower()
                        
                        crime_keywords = ['crime', 'drug', 'gang', 'murder', 'garda', 'arrest', 'criminal']
                        if any(keyword in page_text for keyword in crime_keywords):
                            cprint(f"   ✅ URL encontrada: {test_url}", 'green')
                            self.cache[nombre] = {
                                'url': test_url,
                                'path': path,
                                'found_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.save_cache()
                            return test_url
                except:
                    continue
            
            # Pequeña pausa entre intentos para no sobrecargar
            time.sleep(0.2)
        
        cprint(f"   ❌ No se encontró URL alternativa, usando original", 'red')
        return original_url

# ============================================================================
# ============================================================================
# FUENTES DE IRLANDA - LISTA COMPLETA CON COMENTARIOS Y REGIONES
# ============================================================================
# ============================================================================

FUENTES_BASE = [
    # ========================================================================
    # === NATIONAL NEWS OUTLETS - PRINCIPALES PERIÓDICOS NACIONALES ===
    # ========================================================================
    {'nombre': 'Irish Times', 'url': 'https://www.irishtimes.com/crime-law/', 'base': 'https://www.irishtimes.com', 'condado': 'Dublin', 'categoria': 'national'},
    # {'nombre': 'Irish Independent', 'url': 'https://www.independent.ie/irish-news/crime/', 'base': 'https://www.independent.ie', 'condado': 'Dublin', 'categoria': 'national'},  # Fuente rota - pendiente revisión
    {'nombre': 'RTÉ News', 'url': 'https://www.rte.ie/news/crime/', 'base': 'https://www.rte.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'The Journal', 'url': 'https://www.thejournal.ie/crime/', 'base': 'https://www.thejournal.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Irish Mirror', 'url': 'https://www.irishmirror.ie/news/irish-crime/', 'base': 'https://www.irishmirror.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Irish Examiner', 'url': 'https://www.irishexaminer.com/news/crime/', 'base': 'https://www.irishexaminer.com', 'condado': 'Cork', 'categoria': 'national'},
    {'nombre': 'Newstalk', 'url': 'https://www.newstalk.com/crime', 'base': 'https://www.newstalk.com', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Today FM', 'url': 'https://www.todayfm.com/news/crime/', 'base': 'https://www.todayfm.com', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Garda Post', 'url': 'https://www.gardapost.com/', 'base': 'https://www.gardapost.com', 'condado': 'Dublin', 'categoria': 'national'},
    
    # ========================================================================
    # === DUBLIN REGION - REGIÓN DE DUBLIN ===
    # ========================================================================
    # Dublin Live - Fuente principal de noticias de Dublín
    {'nombre': 'Dublin Live', 'url': 'https://www.dublinlive.ie/news/dublin-crime/', 'base': 'https://www.dublinlive.ie', 'condado': 'Dublin', 'categoria': 'local'},
    {'nombre': 'Dublin Gazette', 'url': 'https://dublingazette.com/crime/', 'base': 'https://dublingazette.com', 'condado': 'Dublin', 'categoria': 'local'},
    {'nombre': 'Dublin People', 'url': 'https://dublinpeople.com/news/crime/', 'base': 'https://dublinpeople.com', 'condado': 'Dublin', 'categoria': 'local'},
    {'nombre': 'Dublin Evening Herald', 'url': 'https://www.dublinlive.ie/news/dublin-news/', 'base': 'https://www.dublinlive.ie', 'condado': 'Dublin', 'categoria': 'local'},
    
    # ========================================================================
    # === CORK REGION - REGIÓN DE CORK ===
    # ========================================================================
    {'nombre': 'Cork Beo', 'url': 'https://www.corkbeo.ie/news/cork-crime/', 'base': 'https://www.corkbeo.ie', 'condado': 'Cork', 'categoria': 'local'},
    {'nombre': 'Cork Independent', 'url': 'https://corkindependent.com/category/crime/', 'base': 'https://corkindependent.com', 'condado': 'Cork', 'categoria': 'local'},
    # The Corkman - Fuente local de noticias de Cork
    
    # ========================================================================
    # === GALWAY REGION - REGIÓN DE GALWAY ===
    # ========================================================================
    #{'nombre': 'Galway Beo', 'url': 'https://www.galwaybeo.ie/news/galway-crime/', 'base': 'https://www.galwaybeo.ie', 'condado': 'Galway', 'categoria': 'local'},
    #{'nombre': 'Galway Advertiser', 'url': 'https://www.galwayadvertiser.ie/crime/', 'base': 'https://www.galwayadvertiser.ie', 'condado': 'Galway', 'categoria': 'local'},
    {'nombre': 'Connacht Tribune', 'url': 'https://www.connachttribune.ie/category/crime/', 'base': 'https://www.connachttribune.ie', 'condado': 'Galway', 'categoria': 'local'},
    #{'nombre': 'Galway Bay FM', 'url': 'https://galwaybayfm.ie/news/crime/', 'base': 'https://galwaybayfm.ie', 'condado': 'Galway', 'categoria': 'local'},
    
    # ========================================================================
    # === LIMERICK REGION - REGIÓN DE LIMERICK ===
    # ========================================================================
    {'nombre': 'Limerick Leader', 'url': 'https://www.limerickleader.ie/news/crime/', 'base': 'https://www.limerickleader.ie', 'condado': 'Limerick', 'categoria': 'local'},
    {'nombre': 'Limerick Post', 'url': 'https://www.limerickpost.ie/category/crime/', 'base': 'https://www.limerickpost.ie', 'condado': 'Limerick', 'categoria': 'local'},
    {'nombre': 'Limerick Live', 'url': 'https://www.limericklive.ie/news/crime/', 'base': 'https://www.limericklive.ie', 'condado': 'Limerick', 'categoria': 'local'},
    
    # ========================================================================
    # === WATERFORD REGION - REGIÓN DE WATERFORD ===
    # ========================================================================
    {'nombre': 'Waterford News', 'url': 'https://www.waterford-news.ie/news/crime/', 'base': 'https://www.waterford-news.ie', 'condado': 'Waterford', 'categoria': 'local'},
    {'nombre': 'Waterford Live', 'url': 'https://www.waterfordlive.ie/news/crime/', 'base': 'https://www.waterfordlive.ie', 'condado': 'Waterford', 'categoria': 'local'},
    
    # ========================================================================
    # === KERRY REGION - REGIÓN DE KERRY ===
    # ========================================================================
    # {'nombre': 'Kerryman', 'url': 'https://www.kerryman.ie/news/crime/', 'base': 'https://www.kerryman.ie', 'condado': 'Kerry', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    {'nombre': 'Radio Kerry', 'url': 'https://www.radiokerry.ie/news/crime/', 'base': 'https://www.radiokerry.ie', 'condado': 'Kerry', 'categoria': 'local'},
    
    # ========================================================================
    # === CLARE REGION - REGIÓN DE CLARE ===
    # ========================================================================
    {'nombre': 'Clare Champion', 'url': 'https://www.clarechampion.ie/category/crime/', 'base': 'https://www.clarechampion.ie', 'condado': 'Clare', 'categoria': 'local'},
    {'nombre': 'Clare Echo', 'url': 'https://www.clareecho.ie/category/crime/', 'base': 'https://www.clareecho.ie', 'condado': 'Clare', 'categoria': 'local'},
    {'nombre': 'Clare FM', 'url': 'https://www.clare.fm/news/crime/', 'base': 'https://www.clare.fm', 'condado': 'Clare', 'categoria': 'local'},
    
    # ========================================================================
    # === DONEGAL REGION - REGIÓN DE DONEGAL ===
    # ========================================================================
    {'nombre': 'Donegal Daily', 'url': 'https://donegaldaily.com/category/crime/', 'base': 'https://donegaldaily.com', 'condado': 'Donegal', 'categoria': 'local'},
    # {'nombre': 'Donegal News', 'url': 'https://donegalnews.com/category/crime/', 'base': 'https://donegalnews.com', 'condado': 'Donegal', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    {'nombre': 'Highland Radio', 'url': 'https://highlandradio.com/category/crime/', 'base': 'https://highlandradio.com', 'condado': 'Donegal', 'categoria': 'local'},
    
    # ========================================================================
    # === MAYO REGION - REGIÓN DE MAYO ===
    # ========================================================================
    {'nombre': 'Mayo News', 'url': 'https://www.mayonews.ie/category/crime', 'base': 'https://www.mayonews.ie', 'condado': 'Mayo', 'categoria': 'local'},
    {'nombre': 'Connaught Telegraph', 'url': 'https://www.connaughttelegraph.ie/category/crime/', 'base': 'https://www.connaughttelegraph.ie', 'condado': 'Mayo', 'categoria': 'local'},
    {'nombre': 'Midwest Radio', 'url': 'https://www.midwestradio.ie/news/crime/', 'base': 'https://www.midwestradio.ie', 'condado': 'Mayo', 'categoria': 'local'},
    
    # ========================================================================
    # === WEXFORD REGION - REGIÓN DE WEXFORD ===
    # ========================================================================
    # {'nombre': 'Wexford People', 'url': 'https://www.wexfordpeople.ie/news/crime/', 'base': 'https://www.wexfordpeople.ie', 'condado': 'Wexford', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    #{'nombre': 'Wexford Echo', 'url': 'https://wexfordecho.ie/category/crime/', 'base': 'https://wexfordecho.ie', 'condado': 'Wexford', 'categoria': 'local'},
    {'nombre': 'South East Radio', 'url': 'https://southeastradio.ie/news/crime/', 'base': 'https://southeastradio.ie', 'condado': 'Wexford', 'categoria': 'local'},
    
    # ========================================================================
    # === KILDARE REGION - REGIÓN DE KILDARE ===
    # ========================================================================
    {'nombre': 'Kildare Now', 'url': 'https://kildarenow.com/crime', 'base': 'https://kildarenow.com', 'condado': 'Kildare', 'categoria': 'local'},
    {'nombre': 'Kildare Post', 'url': 'https://kildarepost.ie/category/crime/', 'base': 'https://kildarepost.ie', 'condado': 'Kildare', 'categoria': 'local'},
    #{'nombre': 'KFM Radio', 'url': 'https://kfmradio.com/news/crime/', 'base': 'https://kfmradio.com', 'condado': 'Kildare', 'categoria': 'local'},
    
    # ========================================================================
    # === TIPPERARY REGION - REGIÓN DE TIPPERARY ===
    # ========================================================================
    {'nombre': 'Tipperary Live', 'url': 'https://www.tipperarylive.ie/news/crime/', 'base': 'https://www.tipperarylive.ie', 'condado': 'Tipperary', 'categoria': 'local'},
    {'nombre': 'Tipperary Star', 'url': 'https://www.tipperarystar.ie/news/crime/', 'base': 'https://www.tipperarystar.ie', 'condado': 'Tipperary', 'categoria': 'local'},
    {'nombre': 'Tipp FM', 'url': 'https://www.tippfm.com/news/crime/', 'base': 'https://www.tippfm.com', 'condado': 'Tipperary', 'categoria': 'local'},
    
    # ========================================================================
    # === LOUTH REGION - REGIÓN DE LOUTH ===
    # ========================================================================
    {'nombre': 'Louth Live', 'url': 'https://www.louthlive.ie/news/crime/', 'base': 'https://www.louthlive.ie', 'condado': 'Louth', 'categoria': 'local'},
    # {'nombre': 'Drogheda Independent', 'url': 'https://www.droghedaindependent.ie/news/crime/', 'base': 'https://www.droghedaindependent.ie', 'condado': 'Louth', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    #{'nombre': 'LMFM', 'url': 'https://www.lmfm.ie/news/crime/', 'base': 'https://www.lmfm.ie', 'condado': 'Louth', 'categoria': 'local'},
    
    # ========================================================================
    # === SLIGO REGION - REGIÓN DE SLIGO ===
    # ========================================================================
    # {'nombre': 'Sligo Champion', 'url': 'https://www.sligochampion.ie/news/crime/', 'base': 'https://www.sligochampion.ie', 'condado': 'Sligo', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    {'nombre': 'Sligo Today', 'url': 'https://sligotoday.ie/category/crime/', 'base': 'https://sligotoday.ie', 'condado': 'Sligo', 'categoria': 'local'},
    {'nombre': 'Ocean FM', 'url': 'https://www.oceanfm.ie/news/crime/', 'base': 'https://www.oceanfm.ie', 'condado': 'Sligo', 'categoria': 'local'},
    
    # ========================================================================
    # === LAOIS REGION - REGIÓN DE LAOIS ===
    # ========================================================================
    {'nombre': 'Leinster Express', 'url': 'https://www.leinsterexpress.ie/news/crime/', 'base': 'https://www.leinsterexpress.ie', 'condado': 'Laois', 'categoria': 'local'},
    {'nombre': 'Laois Today', 'url': 'https://www.laoistoday.ie/category/crime/', 'base': 'https://www.laoistoday.ie', 'condado': 'Laois', 'categoria': 'local'},
    
    # ========================================================================
    # === OFFALY REGION - REGIÓN DE OFFALY ===
    # ========================================================================
    {'nombre': 'Offaly Independent', 'url': 'https://www.offalyindependent.ie/news/crime/', 'base': 'https://www.offalyindependent.ie', 'condado': 'Offaly', 'categoria': 'local'},
    {'nombre': 'Offaly Express', 'url': 'https://www.offalyexpress.ie/news/crime/', 'base': 'https://www.offalyexpress.ie', 'condado': 'Offaly', 'categoria': 'local'},
    
    # ========================================================================
    # === CAVAN REGION - REGIÓN DE CAVAN ===
    # ========================================================================
    {'nombre': 'Cavan Echo', 'url': 'https://www.cavanecho.ie/category/crime/', 'base': 'https://www.cavanecho.ie', 'condado': 'Cavan', 'categoria': 'local'},
    {'nombre': 'Northern Sound', 'url': 'https://www.northernsound.ie/news/crime/', 'base': 'https://www.northernsound.ie', 'condado': 'Cavan', 'categoria': 'local'},
    
    # ========================================================================
    # === MONAGHAN REGION - REGIÓN DE MONAGHAN ===
    # ========================================================================
    {'nombre': 'Monaghan Live', 'url': 'https://monaghanlive.ie/category/crime/', 'base': 'https://monaghanlive.ie', 'condado': 'Monaghan', 'categoria': 'local'},
    # {'nombre': 'Northern Standard', 'url': 'https://northernstandard.ie/category/crime/', 'base': 'https://northernstandard.ie', 'condado': 'Monaghan', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    
    # ========================================================================
    # === ROSCOMMON REGION - REGIÓN DE ROSCOMMON ===
    # ========================================================================
    {'nombre': 'Roscommon Herald', 'url': 'https://www.roscommonherald.ie/news/crime/', 'base': 'https://www.roscommonherald.ie', 'condado': 'Roscommon', 'categoria': 'local'},
    {'nombre': 'Roscommon People', 'url': 'https://roscommonpeople.ie/category/crime/', 'base': 'https://roscommonpeople.ie', 'condado': 'Roscommon', 'categoria': 'local'},
    
    # ========================================================================
    # === WICKLOW REGION - REGIÓN DE WICKLOW ===
    # ========================================================================
    {'nombre': 'Wicklow News', 'url': 'https://wicklownews.net/category/crime/', 'base': 'https://wicklownews.net', 'condado': 'Wicklow', 'categoria': 'local'},
    # {'nombre': 'Wicklow People', 'url': 'https://www.wicklowpeople.ie/news/crime/', 'base': 'https://www.wicklowpeople.ie', 'condado': 'Wicklow', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    
    # ========================================================================
    # === CARLOW REGION - REGIÓN DE CARLOW ===
    # ========================================================================
    {'nombre': 'Carlow Live', 'url': 'https://carlowlive.ie/category/crime/', 'base': 'https://carlowlive.ie', 'condado': 'Carlow', 'categoria': 'local'},
    {'nombre': 'Carlow Nationalist', 'url': 'https://carlownationalist.ie/category/crime/', 'base': 'https://carlownationalist.ie', 'condado': 'Carlow', 'categoria': 'local'},
    
    # ========================================================================
    # === MEATH REGION - REGIÓN DE MEATH ===
    # ========================================================================
    {'nombre': 'Meath Chronicle', 'url': 'https://www.meathchronicle.ie/news/crime/', 'base': 'https://www.meathchronicle.ie', 'condado': 'Meath', 'categoria': 'local'},
    {'nombre': 'Meath Live', 'url': 'https://meathlive.ie/category/crime/', 'base': 'https://meathlive.ie', 'condado': 'Meath', 'categoria': 'local'},
    
    # ========================================================================
    # === LONGFORD REGION - REGIÓN DE LONGFORD ===
    # ========================================================================
    {'nombre': 'Longford Leader', 'url': 'https://www.longfordleader.ie/news/crime/', 'base': 'https://www.longfordleader.ie', 'condado': 'Longford', 'categoria': 'local'},
    {'nombre': 'Longford Live', 'url': 'https://longfordlive.ie/category/crime/', 'base': 'https://longfordlive.ie', 'condado': 'Longford', 'categoria': 'local'},
    
    # ========================================================================
    # === LEITRIM REGION - REGIÓN DE LEITRIM ===
    # ========================================================================
    {'nombre': 'Leitrim Observer', 'url': 'https://www.leitrimobserver.ie/news/crime/', 'base': 'https://www.leitrimobserver.ie', 'condado': 'Leitrim', 'categoria': 'local'},
    # {'nombre': 'Leitrim Live', 'url': 'https://leitrimlive.ie/category/crime/', 'base': 'https://leitrimlive.ie', 'condado': 'Leitrim', 'categoria': 'local'},  # Fuente rota - pendiente revisión
    
    # ========================================================================
    # === NORTHERN IRELAND - IRLANDA DEL NORTE ===
    # ========================================================================
    # ========================================================================
    # === ANTRIM (BELFAST) - REGIÓN DE ANTRIM (BELFAST) ===
    # ========================================================================
    # {'nombre': 'Belfast Telegraph', 'url': 'https://www.belfasttelegraph.co.uk/news/crime/', 'base': 'https://www.belfasttelegraph.co.uk', 'condado': 'Antrim', 'categoria': 'ni'},  # Fuente rota - pendiente revisión
    {'nombre': 'Irish News', 'url': 'https://www.irishnews.com/news/crime/', 'base': 'https://www.irishnews.com', 'condado': 'Antrim', 'categoria': 'ni'},
    {'nombre': 'Belfast Live', 'url': 'https://www.belfastlive.co.uk/news/belfast-crime/', 'base': 'https://www.belfastlive.co.uk', 'condado': 'Antrim', 'categoria': 'ni'},
    {'nombre': 'News Letter', 'url': 'https://www.newsletter.co.uk/news/crime', 'base': 'https://www.newsletter.co.uk', 'condado': 'Antrim', 'categoria': 'ni'},
    
    # ========================================================================
    # === DERRY - REGIÓN DE DERRY ===
    # ========================================================================
    {'nombre': 'Derry Journal', 'url': 'https://www.derryjournal.com/news/crime', 'base': 'https://www.derryjournal.com', 'condado': 'Derry', 'categoria': 'ni'},
    {'nombre': 'Derry Now', 'url': 'https://www.derrynow.com/news/crime', 'base': 'https://www.derrynow.com', 'condado': 'Derry', 'categoria': 'ni'},
    {'nombre': 'Derry News', 'url': 'https://www.derrynews.net/crime/', 'base': 'https://www.derrynews.net', 'condado': 'Derry', 'categoria': 'ni'},
    
    # ========================================================================
    # === DOWN - REGIÓN DE DOWN ===
    # ========================================================================
    {'nombre': 'Down Recorder', 'url': 'https://www.thedownrecorder.co.uk/news/crime/', 'base': 'https://www.thedownrecorder.co.uk', 'condado': 'Down', 'categoria': 'ni'},
    {'nombre': 'Newry Reporter', 'url': 'https://www.newryreporter.com/news/crime/', 'base': 'https://www.newryreporter.com', 'condado': 'Down', 'categoria': 'ni'},
    
    # ========================================================================
    # === TYRONE - REGIÓN DE TYRONE ===
    # ========================================================================
    {'nombre': 'Tyrone Times', 'url': 'https://www.tyronetimes.co.uk/news/crime', 'base': 'https://www.tyronetimes.co.uk', 'condado': 'Tyrone', 'categoria': 'ni'},
    # {'nombre': 'Ulster Herald', 'url': 'https://ulsterherald.com/category/crime/', 'base': 'https://ulsterherald.com', 'condado': 'Tyrone', 'categoria': 'ni'},  # Fuente rota - pendiente revisión
    
    # ========================================================================
    # === ARMAGH - REGIÓN DE ARMAGH ===
    # ========================================================================
    {'nombre': 'Armagh I', 'url': 'https://armaghi.com/category/crime/', 'base': 'https://armaghi.com', 'condado': 'Armagh', 'categoria': 'ni'},
    {'nombre': 'Lurgan Mail', 'url': 'https://www.lurganmail.co.uk/news/crime', 'base': 'https://www.lurganmail.co.uk', 'condado': 'Armagh', 'categoria': 'ni'},
    
    # ========================================================================
    # === FERMANAGH - REGIÓN DE FERMANAGH ===
    # ========================================================================
    #{'nombre': 'Fermanagh Herald', 'url': 'https://www.fermanaghherald.com/category/crime/', 'base': 'https://www.fermanaghherald.com', 'condado': 'Fermanagh', 'categoria': 'ni'},
    {'nombre': 'Impartial Reporter', 'url': 'https://www.impartialreporter.com/news/crime/', 'base': 'https://www.impartialreporter.com', 'condado': 'Fermanagh', 'categoria': 'ni'},
]

# ============================================================================
# ============================================================================
# LISTA COMPLETA DE CONDADOS IRLANDESES (32 CONDADOS)
# ============================================================================
# ============================================================================

CONDADOS_IRLANDA = [
    # República de Irlanda (26 condados)
    'Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kerry', 'Clare', 'Donegal',
    'Mayo', 'Wexford', 'Kildare', 'Tipperary', 'Westmeath', 'Louth', 'Sligo', 'Laois',
    'Offaly', 'Cavan', 'Monaghan', 'Roscommon', 'Wicklow', 'Carlow', 'Meath', 'Longford',
    'Leitrim',
    # Irlanda del Norte (6 condados)
    'Antrim', 'Derry', 'Down', 'Tyrone', 'Armagh', 'Fermanagh'
]

# ============================================================================
# ============================================================================
# PALABRAS CLAVE PARA DETECCIÓN DE CRÍMENES - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

PALABRAS_CLAVE_CRIMEN = [
    # ========================================================================
    # Drug trafficking and seizures - Narcotráfico e incautaciones
    # ========================================================================
    'drugs', 'cocaine', 'heroin', 'cannabis', 'weed', 'meth', 'methamphetamine',
    'ecstasy', 'mdma', 'benzos', 'benzodiazepines', 'oxycodone', 'fentanyl',
    'trafficking', 'drug bust', 'seizure', 'cocaine seizure', 'drugs worth',
    'kilos of cocaine', 'drug gang', 'cartel', 'drug lord', 'narco',
    
    # ========================================================================
    # Gang violence and feuds - Violencia de bandas y disputas
    # ========================================================================
    'kinahan', 'hutch', 'kinahan cartel', 'hutch feud', 'fearon', 'greencastle',
    'gang', 'feud', 'gangland', 'gangland shooting', 'gang violence',
    
    # ========================================================================
    # Shootings and murders - Tiroteos y asesinatos
    # ========================================================================
    'shooting', 'gun attack', 'murder', 'homicide', 'killed', 'fatal shooting',
    'dead', 'death', 'body found', 'suspicious death', 'attempted murder',
    
    # ========================================================================
    # Assaults and violent crimes - Agresiones y crímenes violentos
    # ========================================================================
    'stabbed', 'stabbing', 'assault', 'attack', 'violent', 'brawl', 'fight',
    'beat', 'beaten', 'injured', 'hospitalized', 'serious injury',
    
    # ========================================================================
    # Weapons - Armas
    # ========================================================================
    'firearm', 'weapon', 'gun', 'pistol', 'rifle', 'shotgun', 'ammunition',
    'grenade', 'explosive', 'knife', 'blade', 'machete',
    
    # ========================================================================
    # Garda / Police operations - Operaciones policiales
    # ========================================================================
    'garda', 'gardaí', 'gardai', 'gsoc', 'arrested', 'detained', 'charged',
    'convicted', 'sentenced', 'operation', 'raid', 'search', 'investigation',
    'crackdown', 'task force', 'undercover', 'surveillance',
    
    # ========================================================================
    # Organized crime - Crimen organizado
    # ========================================================================
    'mafia', 'organized crime', 'criminal gang', 'racketeering', 'money laundering',
    'extortion', 'kidnapping', 'disappeared', 'paramilitary', 'dissident',
    
    # ========================================================================
    # Courts and justice - Tribunales y justicia
    # ========================================================================
    'court', 'trial', 'judge', 'jury', 'verdict', 'sentence', 'prison', 'jail',
    'custody', 'remand', 'bail', 'hearing', 'conviction', 'appeal',
    
    # ========================================================================
    # Other crime related - Otros términos relacionados con crímenes
    # ========================================================================
    'crime scene', 'forensic', 'evidence', 'witness', 'victim', 'suspect',
    'manhunt', 'escape', 'fugitive', 'wanted', 'alert', 'crime', 'criminal',
    'offender', 'felon', 'convict', 'inmate', 'detainee', 'prisoner'
]

# ============================================================================
# ============================================================================
# TIPOS DE CRIMEN CON ICONOS Y COLORES - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

TIPOS_CRIMEN = {
    'drugs': {'icono': '💊', 'color': '#8b0000', 'nombre': 'Drug Trafficking', 'es': 'Tráfico de Drogas'},
    'gang_violence': {'icono': '🔫', 'color': '#ff0000', 'nombre': 'Gang Violence', 'es': 'Violencia de Bandas'},
    'murder': {'icono': '💀', 'color': '#000000', 'nombre': 'Murder/Homicide', 'es': 'Asesinato/Homicidio'},
    'assault': {'icono': '👊', 'color': '#cc6600', 'nombre': 'Assault', 'es': 'Agresión'},
    'robbery': {'icono': '💰', 'color': '#8b6b00', 'nombre': 'Robbery/Theft', 'es': 'Robo/Hurto'},
    'organized_crime': {'icono': '🕴️', 'color': '#4b0082', 'nombre': 'Organized Crime', 'es': 'Crimen Organizado'},
    'garda_op': {'icono': '👮', 'color': '#0066cc', 'nombre': 'Garda Operation', 'es': 'Operación Garda'},
    'weapon': {'icono': '🔪', 'color': '#990000', 'nombre': 'Weapon Offense', 'es': 'Delito con Arma'},
    'other': {'icono': '❓', 'color': '#666666', 'nombre': 'Other Crime', 'es': 'Otro Crimen'}
}

# ============================================================================
# ============================================================================
# CLASE GESTOR DE DATOS - VERSIÓN COMPLETA CON GUARDADO FORZADO
# ============================================================================
# ============================================================================

class GestorDatos:
    """Gestor principal de la base de datos de incidentes"""
    
    def __init__(self):
        self.archivo = ARCHIVO_DATOS
        self.datos = self.cargar()
        self.lock = Lock()
    
    def cargar(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                cprint(f"⚠️ Error cargando datos: {e}", 'yellow')
                return {'incidentes': [], 'ultima_actualizacion': None, 'estadisticas_historicas': {}}
        return {'incidentes': [], 'ultima_actualizacion': None, 'estadisticas_historicas': {}}
    
    def guardar(self):
        """Guarda los datos en el archivo JSON con backup automático"""
        try:
            with self.lock:
                self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Crear backup antes de guardar
                if os.path.exists(self.archivo):
                    try:
                        with open(ARCHIVO_BACKUP, 'w', encoding='utf-8') as f:
                            json.dump(self.datos, f, indent=2, ensure_ascii=False)
                    except:
                        pass
                
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(self.datos, f, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            cprint(f"⚠️ Error guardando datos: {e}", 'yellow')
            return False
    
    def guardar_backup(self):
        """Guarda una copia de seguridad manual"""
        try:
            with open(ARCHIVO_BACKUP, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def agregar_incidentes(self, nuevos):
        """Agrega nuevos incidentes evitando duplicados y guarda automáticamente"""
        if not nuevos:
            return 0
        
        try:
            with self.lock:
                ids_existentes = {inc['id'] for inc in self.datos['incidentes']}
                contador = 0
                
                for n in nuevos:
                    if n['id'] not in ids_existentes:
                        self.datos['incidentes'].append(n)
                        ids_existentes.add(n['id'])
                        contador += 1
                
                if contador > 0:
                    self.guardar()
                    self.guardar_backup()
                
                return contador
        except Exception as e:
            cprint(f"⚠️ Error agregando incidentes: {e}", 'yellow')
            return 0
    
    def detectar_tipo(self, texto):
        """Detecta el tipo de crimen basado en el texto"""
        tl = texto.lower()
        
        # ================================================================
        # Detectar drogas - alta prioridad
        # ================================================================
        if any(p in tl for p in ['cocaine', 'heroin', 'drugs', 'cannabis', 'weed', 'meth', 'ecstasy', 'trafficking', 'seizure', 'bust', 'kilos']):
            return 'drugs'
        
        # ================================================================
        # Detectar violencia de bandas
        # ================================================================
        if any(p in tl for p in ['kinahan', 'hutch', 'gang', 'feud', 'cartel', 'gangland']):
            return 'gang_violence'
        
        # ================================================================
        # Detectar asesinatos
        # ================================================================
        if any(p in tl for p in ['murder', 'homicide', 'killed', 'fatal', 'body found', 'suspicious death']):
            return 'murder'
        
        # ================================================================
        # Detectar agresiones
        # ================================================================
        if any(p in tl for p in ['assault', 'stabbed', 'stabbing', 'attack', 'violent', 'brawl', 'fight']):
            return 'assault'
        
        # ================================================================
        # Detectar robos
        # ================================================================
        if any(p in tl for p in ['robbery', 'theft', 'burglary', 'raid', 'heist']):
            return 'robbery'
        
        # ================================================================
        # Detectar crimen organizado
        # ================================================================
        if any(p in tl for p in ['mafia', 'organized crime', 'racketeering', 'money laundering', 'extortion']):
            return 'organized_crime'
        
        # ================================================================
        # Detectar operaciones de Garda
        # ================================================================
        if any(p in tl for p in ['garda', 'gardaí', 'arrested', 'operation', 'raid', 'crackdown', 'task force']):
            return 'garda_op'
        
        # ================================================================
        # Detectar armas
        # ================================================================
        if any(p in tl for p in ['firearm', 'weapon', 'gun', 'pistol', 'rifle', 'shotgun', 'knife']):
            return 'weapon'
        
        return 'other'
    
    def estadisticas(self, incidentes=None):
        """Calcula estadísticas completas de los incidentes"""
        if incidentes is None:
            incidentes = self.datos['incidentes']
        
        stats = {
            'total': len(incidentes),
            'condados': defaultdict(int),
            'tipos': defaultdict(int),
            'fuentes': defaultdict(int),
            'ultimos_7dias': 0,
            'ultimos_30dias': 0,
            'ultimos_90dias': 0,
            'tendencia': defaultdict(int),
            'tendencia_tipos': defaultdict(lambda: defaultdict(int)),
            'top_keywords': defaultdict(int)
        }
        
        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
        
        for inc in incidentes:
            # ================================================================
            # Condados
            # ================================================================
            if inc.get('condado'):
                stats['condados'][inc['condado']] += 1
            
            # ================================================================
            # Tipos
            # ================================================================
            if inc.get('tipo'):
                stats['tipos'][inc['tipo']] += 1
            
            # ================================================================
            # Fuentes
            # ================================================================
            if inc.get('fuente'):
                stats['fuentes'][inc['fuente']] += 1
            
            # ================================================================
            # Fechas
            # ================================================================
            fecha_str = inc.get('fecha', '')
            if fecha_str:
                if fecha_str >= hace_7d:
                    stats['ultimos_7dias'] += 1
                if fecha_str >= hace_30d:
                    stats['ultimos_30dias'] += 1
                if fecha_str >= hace_90d:
                    stats['ultimos_90dias'] += 1
                
                if len(fecha_str) >= 7:
                    mes = fecha_str[:7]
                    stats['tendencia'][mes] += 1
                    
                    if inc.get('tipo'):
                        stats['tendencia_tipos'][mes][inc['tipo']] += 1
            
            # ================================================================
            # Extraer palabras clave del título
            # ================================================================
            titulo = inc.get('titulo', '').lower()
            for keyword in PALABRAS_CLAVE_CRIMEN[:50]:
                if keyword in titulo:
                    stats['top_keywords'][keyword] += 1
        
        return stats
    
    def evolucion_mensual(self):
        """Retorna la evolución mensual de incidentes"""
        meses = {}
        for inc in self.datos['incidentes']:
            if inc.get('fecha') and len(inc['fecha']) >= 7:
                mes = inc['fecha'][:7]
                meses[mes] = meses.get(mes, 0) + 1
        return dict(sorted(meses.items()))
    
    def limpiar_duplicados(self):
        """Elimina incidentes duplicados de la base de datos"""
        with self.lock:
            ids_vistos = set()
            incidentes_limpios = []
            duplicados = 0
            
            for inc in self.datos['incidentes']:
                if inc['id'] not in ids_vistos:
                    ids_vistos.add(inc['id'])
                    incidentes_limpios.append(inc)
                else:
                    duplicados += 1
            
            self.datos['incidentes'] = incidentes_limpios
            
            if duplicados > 0:
                self.guardar()
            
            return duplicados
    
    def exportar_json(self):
        """Exporta los datos completos en formato JSON"""
        return json.dumps(self.datos, indent=2, ensure_ascii=False)
    
    def exportar_csv(self):
        """Exporta los incidentes en formato CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Título', 'Fecha', 'Condado', 'Tipo', 'Fuente'])
        
        for inc in self.datos['incidentes']:
            writer.writerow([
                inc['id'],
                inc['titulo'].replace('\n', ' ').replace('\r', ''),
                inc['fecha'],
                inc.get('condado', ''),
                inc.get('tipo', ''),
                inc['fuente']
            ])
        
        return output.getvalue()
    
    def exportar_html(self):
        """Exporta los datos en formato HTML para reportes"""
        stats = self.estadisticas()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>KELTIC KRAKEN - Ireland Crime Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #ff4444; }}
        .stats {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #ff4444; }}
        .stat-number {{ font-size: 2em; color: #ff4444; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #333; padding: 10px; text-align: left; }}
        th {{ background: #333; color: #ff4444; }}
        tr:hover {{ background: #1a1a1a; }}
        .footer {{ text-align: center; margin-top: 30px; padding: 15px; background: #1a1a1a; color: #666; }}
    </style>
</head>
<body>
    <h1>🔪 KELTIC KRAKEN - Ireland Crime Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="stats">
        <div class="stat-card"><div>Total Incidents</div><div class="stat-number">{stats['total']}</div></div>
        <div class="stat-card"><div>Last 7 Days</div><div class="stat-number">{stats['ultimos_7dias']}</div></div>
        <div class="stat-card"><div>Last 30 Days</div><div class="stat-number">{stats['ultimos_30dias']}</div></div>
        <div class="stat-card"><div>Sources</div><div class="stat-number">{len(stats['fuentes'])}</div></div>
    </div>
    
    <h2>Top Counties</h2>
    <table>
        <tr><th>County</th><th>Incidents</th><th>%</th></tr>"""
        
        for county, count in sorted(stats['condados'].items(), key=lambda x: x[1], reverse=True)[:10]:
            pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            html += f"<tr><td>{county}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        
        html += """</table>
    
    <h2>Crime Types</h2>
    <table>
        <tr><th>Type</th><th>Incidents</th><th>%</th></tr>"""
        
        for crime_type, count in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            icono = TIPOS_CRIMEN.get(crime_type, {}).get('icono', '❓')
            nombre = TIPOS_CRIMEN.get(crime_type, {}).get('nombre', crime_type)
            html += f"</td><td>{icono} {nombre}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        
        html += f"""</table>
    
    <h2>Recent Incidents (Last 20)</h2>
    <table>
        <tr><th>Date</th><th>County</th><th>Type</th><th>Title</th><th>Source</th></tr>"""
        
        for inc in self.datos['incidentes'][-20:][::-1]:
            html += f"<tr><td>{inc['fecha']}</td><td>{inc.get('condado', '?')}</td><td>{inc.get('tipo', '?')}</td><td>{inc['titulo'][:100]}...</td><td>{inc['fuente']}</td></tr>"
        
        html += f"""
    </table>
    
    <div class="footer">
        <p>🔪 KELTIC KRAKEN v{VERSION} - Ireland Crime Intelligence Platform</p>
        <p>Data-driven intelligence for public safety awareness</p>
    </div>
</body>
</html>"""
        
        return html

# ============================================================================
# ============================================================================
# CLASE VERIFICADOR DE FUENTES CON AUTO-DISCOVERY - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

class VerificadorFuentes:
    """Verifica fuentes y aplica auto-discovery cuando es necesario"""
    
    def __init__(self):
        self.discoverer = URLAutoDiscoverer()
        self.estado_file = ARCHIVO_ESTADO
        self.estado = self.cargar_estado()
    
    def cargar_estado(self):
        if os.path.exists(self.estado_file):
            try:
                with open(self.estado_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def guardar_estado(self):
        with open(self.estado_file, 'w', encoding='utf-8') as f:
            json.dump(self.estado, f, indent=2)
    
    def verificar_fuente(self, fuente, aplicar_discovery=True):
        """Verifica una sola fuente, opcionalmente aplicando auto-discovery"""
        nombre = fuente['nombre']
        
        # ================================================================
        # Verificar usando la URL actual
        # ================================================================
        for intento in range(MAX_INTENTOS):
            try:
                headers = {
                    'User-Agent': get_random_ua(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
                
                r = requests.get(fuente['url'], timeout=TIMEOUT, headers=headers, allow_redirects=True)
                
                if r.status_code == 200:
                    fuente['activo'] = True
                    return fuente, True
                else:
                    time.sleep(get_random_delay())
            except Exception as e:
                time.sleep(get_random_delay())
        
        # ================================================================
        # Si falló y está habilitado el auto-discovery, buscar URL alternativa
        # ================================================================
        if aplicar_discovery:
            nueva_url = self.discoverer.discover_url(fuente)
            if nueva_url != fuente['url']:
                fuente['url'] = nueva_url
                # Probar la nueva URL
                for intento in range(MAX_INTENTOS):
                    try:
                        headers = {'User-Agent': get_random_ua()}
                        r = requests.get(nueva_url, timeout=TIMEOUT, headers=headers)
                        if r.status_code == 200:
                            fuente['activo'] = True
                            return fuente, True
                    except:
                        continue
        
        fuente['activo'] = False
        return fuente, False
    
    def verificar_todas(self, fuentes, mostrar_progreso=True):
        """Verifica todas las fuentes con barra de progreso"""
        cprint(f"\n{'='*80}", 'red', bold=True)
        cprint(f"🔍 {t('verificando')}", 'red', bold=True, bg=True)
        cprint(f"{'='*80}", 'red', bold=True)
        
        verificadas = []
        activas = 0
        auto_discovered = 0
        total = len(fuentes)
        
        for i, fuente in enumerate(fuentes, 1):
            if mostrar_progreso:
                porcentaje = (i / total) * 100
                barra_len = 30
                filled = int(barra_len * i / total)
                barra = '█' * filled + '░' * (barra_len - filled)
                sys.stdout.write(f"\r   🔪 Progreso: [{barra}] {i}/{total} ({porcentaje:.1f}%)")
                sys.stdout.flush()
            
            cprint(f"\n📰 [{i}/{total}] {fuente['nombre']}", 'yellow', bold=True, end=' ')
            
            url_original = fuente['url']
            fuente_verificada, exito = self.verificar_fuente(fuente.copy(), aplicar_discovery=True)
            
            if exito:
                activas += 1
                if fuente_verificada['url'] != url_original:
                    auto_discovered += 1
                    cprint(f"✅ OK (Auto-discovery)", 'green')
                else:
                    cprint(f"✅ OK", 'green')
            else:
                cprint(f"❌ INACTIVE", 'red')
            
            verificadas.append(fuente_verificada)
            time.sleep(0.2)
        
        print()  # Nueva línea después de la barra
        
        cprint(f"\n{'='*80}", 'green', bold=True)
        cprint(f"📊 RESULTADOS:", 'green', bold=True)
        cprint(f"   Fuentes activas: {activas} de {total}", 'white')
        cprint(f"   Auto-discovery aplicado: {auto_discovered} URLs encontradas", 'cyan')
        cprint(f"{'='*80}", 'green', bold=True)
        
        # Guardar estado para futuras ejecuciones
        self.guardar_estado()
        
        return verificadas

# ============================================================================
# ============================================================================
# CLASE EXTRACTOR DE NOTICIAS - VERSIÓN COMPLETA CON GUARDADO POR FUENTE
# ============================================================================
# ============================================================================

class ExtractorNoticias:
    """Extrae noticias de crímenes de las fuentes verificadas"""
    
    def __init__(self, fuentes):
        self.fuentes = fuentes
        self.session = self._crear_sesion()
    
    def _crear_sesion(self):
        """Crea una sesión HTTP con retry y adaptadores"""
        session = requests.Session()
        retry = Retry(
            total=2,
            read=2,
            connect=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def fetch_url(self, url):
        """Obtiene una URL con reintentos y headers rotativos"""
        for intento in range(MAX_INTENTOS):
            try:
                headers = {
                    'User-Agent': get_random_ua(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                response = self.session.get(url, timeout=TIMEOUT, headers=headers, allow_redirects=True)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Too many requests
                    time.sleep(get_random_delay() * 2)
                else:
                    time.sleep(get_random_delay())
                    
            except requests.exceptions.Timeout:
                time.sleep(get_random_delay())
            except requests.exceptions.ConnectionError:
                time.sleep(get_random_delay())
            except Exception:
                time.sleep(get_random_delay())
        
        return None
    
    def extraer_de_fuente(self, fuente, paginas=PAGINAS_BUSQUEDA):
        """Extrae incidentes de una fuente específica"""
        incidentes = []
        url_base = fuente['url']
        
        for pagina in range(1, paginas + 1):
            # ================================================================
            # Construir URL de paginación
            # ================================================================
            if pagina == 1:
                url = url_base
            else:
                # Probar diferentes patrones de paginación
                patrones = [
                    url_base.rstrip('/') + f'/page/{pagina}/',
                    url_base.rstrip('/') + f'?page={pagina}',
                    url_base.rstrip('/') + f'&page={pagina}',
                    url_base.rstrip('/') + f'/pagina/{pagina}',
                    url_base.rstrip('/') + f'?p={pagina}',
                    url_base.rstrip('/') + f'/index_{pagina}.html'
                ]
                url = None
                for patron in patrones:
                    try:
                        test_response = self.fetch_url(patron)
                        if test_response:
                            url = patron
                            break
                    except:
                        continue
                
                if not url:
                    break
            
            try:
                cprint(f"   📄 Página {pagina}... ", 'gray', end='')
                response = self.fetch_url(url)
                
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # ========================================================
                    # Buscar elementos que contengan noticias
                    # ========================================================
                    elementos = []
                    
                    # Artículos
                    elementos.extend(soup.find_all('article'))
                    elementos.extend(soup.find_all('div', class_=re.compile(r'article|story|post|news|entry', re.I)))
                    elementos.extend(soup.find_all('li', class_=re.compile(r'article|story|post|news', re.I)))
                    
                    # Encabezados (a menudo contienen títulos)
                    elementos.extend(soup.find_all(['h1', 'h2', 'h3', 'h4']))
                    
                    # Enlaces (pueden contener títulos de noticias)
                    elementos.extend(soup.find_all('a', href=True))
                    
                    encontrados_pagina = 0
                    gestor_temp = GestorDatos()
                    
                    for elem in elementos[:40]:  # Limitar por página
                        texto = elem.get_text().strip()
                        
                        if len(texto) < 40:
                            continue
                        
                        texto_lower = texto.lower()
                        
                        # Verificar si contiene palabras clave de crimen
                        if any(palabra in texto_lower for palabra in PALABRAS_CLAVE_CRIMEN):
                            # ====================================================
                            # Extraer fecha si está disponible
                            # ====================================================
                            fecha_elem = soup.find('time')
                            fecha = datetime.now().strftime('%Y-%m-%d')
                            
                            if fecha_elem and fecha_elem.get('datetime'):
                                fecha = fecha_elem.get('datetime')[:10]
                            elif fecha_elem and fecha_elem.get('content'):
                                fecha = fecha_elem.get('content')[:10]
                            else:
                                # Buscar patrones de fecha en el texto
                                patron_fecha = r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}'
                                match = re.search(patron_fecha, texto)
                                if match:
                                    fecha = match.group()[:10]
                            
                            # ====================================================
                            # Determinar condado
                            # ====================================================
                            condado = fuente['condado']
                            for c in CONDADOS_IRLANDA:
                                if c.lower() in texto_lower:
                                    condado = c
                                    break
                            
                            tipo = gestor_temp.detectar_tipo(texto)
                            
                            incidentes.append({
                                'id': hashlib.md5(texto.encode()).hexdigest()[:16],
                                'titulo': texto[:500],
                                'fecha': fecha,
                                'condado': condado,
                                'tipo': tipo,
                                'fuente': fuente['nombre']
                            })
                            encontrados_pagina += 1
                    
                    cprint(f"✓ {encontrados_pagina} encontrados", 'green')
                    
                    # Si no encontramos nada en 2 páginas consecutivas, salir
                    if encontrados_pagina == 0 and pagina > 2:
                        break
                else:
                    cprint(f"✗ Sin respuesta", 'red')
                    break
                    
            except Exception as e:
                cprint(f"✗ Error: {str(e)[:30]}", 'red')
            
            time.sleep(get_random_delay())
        
        return incidentes
    
    def extraer_todas(self, paginas=PAGINAS_BUSQUEDA):
        """Extrae incidentes de todas las fuentes activas - CON GUARDADO POR FUENTE"""
        cprint(f"\n{'='*80}", 'red', bold=True)
        cprint(f"🔪 KELTIC KRAKEN - ESCANEANDO IRLANDA", 'red', bold=True, bg=True)
        cprint(f"{'='*80}", 'red', bold=True)
        
        todas_las_noticias = []
        fuentes_activas = [f for f in self.fuentes if f.get('activo', True)]
        total_activas = len(fuentes_activas)
        
        if total_activas == 0:
            cprint(f"\n⚠️ {t('sin_datos')}", 'yellow')
            return todas_las_noticias
        
        # ================================================================
        # Crear un gestor temporal para guardar después de cada fuente
        # ================================================================
        gestor_local = GestorDatos()
        
        for idx, fuente in enumerate(fuentes_activas, 1):
            # ================================================================
            # Barra de progreso
            # ================================================================
            porcentaje = (idx / total_activas) * 100
            barra_len = 40
            filled = int(barra_len * idx / total_activas)
            barra = '█' * filled + '░' * (barra_len - filled)
            sys.stdout.write(f"\r   🔪 Escaneando: [{barra}] {idx}/{total_activas} ({porcentaje:.1f}%)")
            sys.stdout.flush()
            
            cprint(f"\n\n📰 {fuente['nombre']}", 'yellow', bold=True)
            cprint(f"   📍 Condado: {fuente['condado']} | 🌐 URL: {fuente['url'][:50]}...", 'gray', dim=True)
            
            incidentes_fuente = self.extraer_de_fuente(fuente, paginas)
            
            # ================================================================
            # GUARDADO FORZADO DESPUÉS DE CADA FUENTE (CRÍTICO)
            # ================================================================
            if incidentes_fuente:
                agregados = gestor_local.agregar_incidentes(incidentes_fuente)
                todas_las_noticias.extend(incidentes_fuente)
                cprint(f"   📊 Total en esta fuente: {len(incidentes_fuente)} incidentes ({agregados} nuevos)", 'cyan')
                cprint(f"   💾 Datos guardados automáticamente", 'green')
            else:
                cprint(f"   📊 Total en esta fuente: 0 incidentes", 'gray')
        
        print()  # Línea nueva después de la barra
        
        # ================================================================
        # Eliminar duplicados por ID
        # ================================================================
        incidentes_unicos = {}
        for noticia in todas_las_noticias:
            if noticia['id'] not in incidentes_unicos:
                incidentes_unicos[noticia['id']] = noticia
        
        resultado = list(incidentes_unicos.values())
        
        cprint(f"\n{'='*80}", 'green', bold=True)
        cprint(f"🔪 RESULTADO FINAL:", 'green', bold=True)
        cprint(f"   Incidentes encontrados: {len(resultado)}", 'white')
        cprint(f"   Fuentes activas: {total_activas}", 'white')
        cprint(f"   Auto-discovery aplicado automáticamente", 'cyan')
        cprint(f"   💾 Datos guardados automáticamente después de CADA fuente", 'green')
        cprint(f"{'='*80}", 'green', bold=True)
        
        return resultado

# ============================================================================
# ============================================================================
# INTERFAZ WEB CON GRÁFICOS Y PAGINACIÓN - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

app = Flask(__name__)
gestor_global = None
fuentes_global = None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔪 KELTIC KRAKEN - Ireland Crime Intelligence</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 100%);
            color: #e0e0e0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Header con animación */
        .header {
            background: linear-gradient(135deg, #1a0a0a, #2a0a0a);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            border: 1px solid #ff3333;
            box-shadow: 0 0 30px rgba(255,0,0,0.2);
            animation: glow 2s infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 10px rgba(255,0,0,0.2); }
            to { box-shadow: 0 0 30px rgba(255,0,0,0.5); }
        }
        
        h1 {
            font-size: 3em;
            color: #ff4444;
            letter-spacing: 3px;
            text-shadow: 0 0 10px #ff0000;
            animation: pulse 1.5s infinite alternate;
        }
        
        @keyframes pulse {
            from { text-shadow: 0 0 5px #ff0000; }
            to { text-shadow: 0 0 20px #ff0000; }
        }
        
        .version-badge {
            background: #1a1a1a;
            color: #ff8888;
            padding: 5px 20px;
            border-radius: 30px;
            display: inline-block;
            margin-top: 10px;
            font-family: monospace;
            border: 1px solid #ff4444;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #111, #1a1a1a);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border-left: 5px solid #ff4444;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255,68,68,0.2);
        }
        
        .stat-number {
            font-size: 3em;
            color: #ff4444;
            font-weight: bold;
        }
        
        .stat-label {
            color: #888;
            margin-top: 10px;
        }
        
        /* Botones */
        .btn {
            background: #222;
            color: #ff4444;
            border: 2px solid #ff4444;
            padding: 12px 30px;
            border-radius: 40px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: #ff4444;
            color: #000;
            transform: scale(1.05);
            box-shadow: 0 0 15px #ff4444;
        }
        
        /* Contenedores de gráficos */
        .charts-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        
        .chart-container {
            background: #111;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #333;
            transition: all 0.3s ease;
        }
        
        .chart-container:hover {
            border-color: #ff4444;
            box-shadow: 0 0 15px rgba(255,68,68,0.1);
        }
        
        .chart-title {
            color: #ff6666;
            font-size: 1.3em;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        
        /* Filtros */
        .filtros {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .filtro-btn {
            background: #1a1a1a;
            color: #ccc;
            border: 2px solid #333;
            padding: 10px 25px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .filtro-btn:hover, .filtro-btn.active {
            background: #ff4444;
            color: #000;
            border-color: #ff4444;
        }
        
        /* Tarjetas de incidentes */
        .incidente-card {
            background: linear-gradient(135deg, #0a0a0a, #111);
            margin: 15px 0;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #ff4444;
            transition: all 0.3s ease;
        }
        
        .incidente-card:hover {
            transform: translateX(10px);
            background: #1a1a1a;
        }
        
        .incidente-titulo {
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #fff;
        }
        
        .incidente-meta {
            color: #888;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 0.85em;
        }
        
        .incidente-meta span {
            background: #1a1a1a;
            padding: 5px 10px;
            border-radius: 20px;
        }
        
        /* Paginación */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .page-btn {
            background: #222;
            color: #ff4444;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            border: 1px solid #ff4444;
            transition: all 0.3s ease;
            min-width: 40px;
            text-align: center;
        }
        
        .page-btn:hover, .page-btn.active {
            background: #ff4444;
            color: #000;
        }
        
        .page-info {
            color: #888;
            margin: 0 15px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            background: #111;
            border-radius: 15px;
            color: #666;
            border-top: 1px solid #333;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .charts-row { grid-template-columns: 1fr; }
            h1 { font-size: 1.8em; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
        
        /* Scrollbar personalizado */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #1a1a1a; }
        ::-webkit-scrollbar-thumb { background: #ff4444; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #ff6666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔪 KELTIC KRAKEN</h1>
            <div class="version-badge">v{{ version }} · Ireland Crime Intelligence · Port {{ puerto }}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total }}</div>
                <div class="stat-label">📊 TOTAL INCIDENTS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.ultimos_7dias }}</div>
                <div class="stat-label">⚡ LAST 7 DAYS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.ultimos_30dias }}</div>
                <div class="stat-label">🔥 LAST 30 DAYS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ periodicos_activos }}</div>
                <div class="stat-label">📰 ACTIVE SOURCES</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <form action="/actualizar" method="post" style="display: inline;">
                <button class="btn">🔄 UPDATE DATA</button>
            </form>
            <a href="/exportar/json" class="btn">📥 JSON</a>
            <a href="/exportar/csv" class="btn">📥 CSV</a>
            <a href="/exportar/html" class="btn">📄 HTML REPORT</a>
        </div>
        
        <div class="filtros">
            <a href="{{ url_for('index_paginada', page=1, filtro='todo') }}" class="filtro-btn {% if filtro == 'todo' %}active{% endif %}">📅 ALL</a>
            <a href="{{ url_for('index_paginada', page=1, filtro='7d') }}" class="filtro-btn {% if filtro == '7d' %}active{% endif %}">⚡ 7 DAYS</a>
            <a href="{{ url_for('index_paginada', page=1, filtro='30d') }}" class="filtro-btn {% if filtro == '30d' %}active{% endif %}">🔥 30 DAYS</a>
            <a href="{{ url_for('index_paginada', page=1, filtro='90d') }}" class="filtro-btn {% if filtro == '90d' %}active{% endif %}">📊 90 DAYS</a>
        </div>
        
        <div class="charts-row">
            <div class="chart-container">
                <div class="chart-title">📍 INCIDENTS BY COUNTY</div>
                <canvas id="countyChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">🔪 CRIME TYPE DISTRIBUTION</div>
                <canvas id="typeChart"></canvas>
            </div>
        </div>
        
        <div class="charts-row">
            <div class="chart-container">
                <div class="chart-title">📈 MONTHLY TREND</div>
                <canvas id="trendChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">📰 TOP NEWS SOURCES</div>
                <canvas id="sourcesChart"></canvas>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🔪 LATEST INCIDENTS - {{ t('page') }} {{ pagina }} {{ t('of') }} {{ total_paginas }}</div>
            {% for inc in incidentes_pagina %}
            <div class="incidente-card">
                <div class="incidente-titulo">{{ inc.titulo }}</div>
                <div class="incidente-meta">
                    <span>📍 {{ inc.condado or '?' }}</span>
                    <span>📅 {{ inc.fecha }}</span>
                    <span>📰 {{ inc.fuente }}</span>
                    <span>🔪 {{ inc.tipo|upper }}</span>
                </div>
            </div>
            {% endfor %}
            
            <!-- ======================================================== -->
            <!-- PAGINACIÓN COMPLETA -->
            <!-- ======================================================== -->
            <div class="pagination">
                {% if pagina > 1 %}
                    <a href="{{ url_for('index_paginada', page=pagina-1, filtro=filtro) }}" class="page-btn">◀ PREVIOUS</a>
                {% endif %}
                
                {% for p in range(1, total_paginas + 1) %}
                    {% if p == 1 or p == total_paginas or (p >= pagina-2 and p <= pagina+2) %}
                        {% if p == pagina %}
                            <span class="page-btn active">{{ p }}</span>
                        {% else %}
                            <a href="{{ url_for('index_paginada', page=p, filtro=filtro) }}" class="page-btn">{{ p }}</a>
                        {% endif %}
                    {% elif p == pagina-3 or p == pagina+3 %}
                        <span class="page-info">...</span>
                    {% endif %}
                {% endfor %}
                
                {% if pagina < total_paginas %}
                    <a href="{{ url_for('index_paginada', page=pagina+1, filtro=filtro) }}" class="page-btn">NEXT ▶</a>
                {% endif %}
            </div>
            <div class="page-info" style="text-align: center; margin-top: 10px;">
                Mostrando {{ (pagina-1)*ITEMS_POR_PAGINA + 1 }} a {{ min(pagina*ITEMS_POR_PAGINA, total_incidentes) }} de {{ total_incidentes }} incidentes
            </div>
        </div>
        
        <div class="footer">
            <p>🔪 KELTIC KRAKEN v{{ version }} · {{ periodicos_activos }} ACTIVE SOURCES</p>
            <p style="font-size:0.8em;">"Un gran poder conlleva una gran responsabilidad" - Spider-Man</p>
            <p style="font-size:0.7em; margin-top:10px;">Data-driven intelligence for public safety awareness</p>
        </div>
    </div>
    
    <script>
        // Gráfico de condados
        const countyCtx = document.getElementById('countyChart').getContext('2d');
        new Chart(countyCtx, {
            type: 'bar',
            data: {
                labels: {{ condados_labels|tojson }},
                datasets: [{
                    label: 'Incidents',
                    data: {{ condados_data|tojson }},
                    backgroundColor: 'rgba(255, 68, 68, 0.7)',
                    borderColor: '#ff4444',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: '#ccc' } },
                    tooltip: { backgroundColor: '#111', titleColor: '#ff4444', bodyColor: '#ccc' }
                },
                scales: {
                    y: { ticks: { color: '#ccc' }, grid: { color: '#333' } },
                    x: { ticks: { color: '#ccc', rotation: 45 } }
                }
            }
        });
        
        // Gráfico de tipos
        const typeCtx = document.getElementById('typeChart').getContext('2d');
        new Chart(typeCtx, {
            type: 'doughnut',
            data: {
                labels: {{ tipos_labels|tojson }},
                datasets: [{
                    data: {{ tipos_data|tojson }},
                    backgroundColor: ['#8b0000', '#ff0000', '#000000', '#cc6600', '#8b6b00', '#4b0082', '#0066cc', '#990000', '#666666'],
                    borderWidth: 2,
                    borderColor: '#1a1a1a'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#ccc' } },
                    tooltip: { backgroundColor: '#111', titleColor: '#ff4444' }
                }
            }
        });
        
        // Gráfico de tendencia
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: {{ tendencia_labels|tojson }},
                datasets: [{
                    label: 'Incidents per month',
                    data: {{ tendencia_data|tojson }},
                    borderColor: '#ff4444',
                    backgroundColor: 'rgba(255, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ff4444',
                    pointBorderColor: '#fff',
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#ccc' } },
                    tooltip: { backgroundColor: '#111', titleColor: '#ff4444' }
                },
                scales: {
                    y: { ticks: { color: '#ccc' }, grid: { color: '#333' } },
                    x: { ticks: { color: '#ccc', rotation: 45 } }
                }
            }
        });
        
        // Gráfico de fuentes
        const sourcesCtx = document.getElementById('sourcesChart').getContext('2d');
        new Chart(sourcesCtx, {
            type: 'bar',
            data: {
                labels: {{ fuentes_labels|tojson }},
                datasets: [{
                    label: 'Articles',
                    data: {{ fuentes_data|tojson }},
                    backgroundColor: 'rgba(255, 102, 102, 0.7)',
                    borderColor: '#ff6666',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: { labels: { color: '#ccc' } },
                    tooltip: { backgroundColor: '#111', titleColor: '#ff6666' }
                },
                scales: {
                    x: { ticks: { color: '#ccc' }, grid: { color: '#333' } },
                    y: { ticks: { color: '#ccc' } }
                }
            }
        });
    </script>
</body>
</html>
'''

# ============================================================================
# ============================================================================
# RUTAS DE FLASK CON PAGINACIÓN - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

@app.route('/')
def index():
    return index_paginada(1, 'todo')

@app.route('/page/<int:page>')
def index_paginada(page=1, filtro='todo'):
    global gestor_global, fuentes_global
    
    # ================================================================
    # Obtener todos los incidentes
    # ================================================================
    incidentes = gestor_global.datos['incidentes']
    
    # ================================================================
    # Aplicar filtros de tiempo
    # ================================================================
    if filtro == '7d':
        limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '30d':
        limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '90d':
        limite = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    
    # ================================================================
    # Estadísticas
    # ================================================================
    stats = gestor_global.estadisticas(incidentes)
    periodicos_activos = len([f for f in fuentes_global if f.get('activo', True)])
    
    # ================================================================
    # Preparar datos para gráficos
    # ================================================================
    condados_labels = list(stats['condados'].keys())
    condados_data = list(stats['condados'].values())
    tipos_labels = [f"{TIPOS_CRIMEN.get(t, {}).get('icono', '❓')} {t.upper()}" for t in stats['tipos'].keys()]
    tipos_data = list(stats['tipos'].values())
    
    tendencia_items = list(stats['tendencia'].items())[-12:]
    tendencia_labels = [item[0] for item in tendencia_items]
    tendencia_data = [item[1] for item in tendencia_items]
    
    fuentes_top = dict(sorted(stats['fuentes'].items(), key=lambda x: x[1], reverse=True)[:5])
    fuentes_labels = list(fuentes_top.keys())
    fuentes_data = list(fuentes_top.values())
    
    # ================================================================
    # PAGINACIÓN
    # ================================================================
    total_incidentes = len(incidentes)
    total_paginas = max(1, (total_incidentes + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA)
    pagina = max(1, min(page, total_paginas))
    inicio = (pagina - 1) * ITEMS_POR_PAGINA
    fin = inicio + ITEMS_POR_PAGINA
    incidentes_pagina = incidentes[::-1][inicio:fin]  # Invertir para mostrar más recientes primero
    
    return render_template_string(HTML_TEMPLATE, 
        version=VERSION, puerto=PUERTO, stats=stats,
        incidentes_pagina=incidentes_pagina, periodicos_activos=periodicos_activos, 
        filtro=filtro, pagina=pagina, total_paginas=total_paginas, total_incidentes=total_incidentes,
        condados_labels=condados_labels, condados_data=condados_data,
        tipos_labels=tipos_labels, tipos_data=tipos_data,
        tendencia_labels=tendencia_labels, tendencia_data=tendencia_data,
        fuentes_labels=fuentes_labels, fuentes_data=fuentes_data,
        ITEMS_POR_PAGINA=ITEMS_POR_PAGINA, t=t)

@app.route('/filtro/<periodo>')
def filtro_route(periodo):
    return index_paginada(1, periodo)

@app.route('/actualizar', methods=['POST'])
def actualizar():
    global gestor_global, fuentes_global
    cprint(f"\n{'='*80}", 'red', bold=True)
    cprint(f"🔪 {t('actualizando')}", 'red', bold=True, bg=True)
    cprint(f"{'='*80}", 'red', bold=True)
    
    # ================================================================
    # Verificar fuentes con auto-discovery
    # ================================================================
    verificador = VerificadorFuentes()
    fuentes_verificadas = verificador.verificar_todas(fuentes_global)
    fuentes_global = fuentes_verificadas
    
    # ================================================================
    # Extraer noticias (ya guarda automáticamente después de cada fuente)
    # ================================================================
    extractor = ExtractorNoticias(fuentes_verificadas)
    nuevas_noticias = extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
    
    # ================================================================
    # Los incidentes ya se guardaron dentro de extraer_todas()
    # Solo mostramos el resumen final
    # ================================================================
    cprint(f"\n{'='*80}", 'green', bold=True)
    cprint(f"✅ PROCESO COMPLETADO", 'green', bold=True, bg=True)
    cprint(f"{'='*80}", 'green', bold=True)
    
    return index_paginada(1, 'todo')

@app.route('/exportar/json')
def exportar_json():
    global gestor_global
    return Response(gestor_global.exportar_json(), 
        mimetype='application/json', 
        headers={'Content-Disposition': 'attachment; filename=keltic_kraken_export.json'})

@app.route('/exportar/csv')
def exportar_csv():
    global gestor_global
    return Response(gestor_global.exportar_csv(), 
        mimetype='text/csv', 
        headers={'Content-Disposition': 'attachment; filename=keltic_kraken_export.csv'})

@app.route('/exportar/html')
def exportar_html():
    global gestor_global
    return Response(gestor_global.exportar_html(), 
        mimetype='text/html', 
        headers={'Content-Disposition': 'attachment; filename=keltic_kraken_report.html'})

# ============================================================================
# ============================================================================
# MENÚ PRINCIPAL DE TERMINAL - VERSIÓN COMPLETA
# ============================================================================
# ============================================================================

def mostrar_menu_principal():
    """Muestra el menú principal con diseño profesional"""
    stats = gestor_global.estadisticas()
    fuentes_activas = len([f for f in fuentes_global if f.get('activo', True)])
    
    print(f"""
{Color.RED}╔{'═' * 70}╗{Color.RESET}
{Color.RED}║{Color.BOLD}{Color.WHITE}  🔪 {t('app_name')}{' ' * 44}{Color.RED}║{Color.RESET}
{Color.RED}╠{'═' * 70}╣{Color.RESET}
{Color.RED}║{Color.CYAN}  📊 {t('stats_total')}: {stats['total']} {t('incidentes')}{' ' * 35}{Color.RED}║{Color.RESET}
{Color.RED}║{Color.YELLOW}  📰 {t('fuentes')}: {fuentes_activas} de {len(fuentes_global)}{' ' * 40}{Color.RED}║{Color.RESET}
{Color.RED}║{Color.GREEN}  🏴 {t('condados')}: {len(stats['condados'])}{' ' * 44}{Color.RED}║{Color.RESET}
{Color.RED}╚{'═' * 70}╝{Color.RESET}

{Color.YELLOW}┌{'─' * 50}┐{Color.RESET}
{Color.YELLOW}│{Color.CYAN}  📋 {t('menu_title')}{' ' * 33}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}├{'─' * 50}┤{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [1] 🔍 {t('cmd_buscar')}{' ' * 4}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [2] 📊 {t('cmd_analisis')}{' ' * 11}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [3] 🔗 {t('cmd_conexiones')}{' ' * 3}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [4] 📈 {t('cmd_evolucion')}{' ' * 14}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [5] 🌐 {t('cmd_web')}{' ' * 1}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [6] 📰 {t('cmd_ultimos')}{' ' * 8}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [7] 📥 {t('cmd_exportar')}{' ' * 11}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [8] 🔍 {t('cmd_verificar')}{' ' * 1}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [9] 📊 {t('cmd_tipos')}{' ' * 10}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [10] 📈 {t('cmd_estadisticas')}{' ' * 18}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.GREEN}  [11] 🧹 {t('cmd_limpiar')}{' ' * 8}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}│{Color.RED}  [12] 🗑️ {t('cmd_salir')}{' ' * 19}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}└{'─' * 50}┘{Color.RESET}
""")

def menu():
    """Bucle principal del menú"""
    global gestor_global, fuentes_global
    
    while True:
        mostrar_menu_principal()
        
        opcion = input(f"{Color.CYAN}➤ {Color.YELLOW}Opción: {Color.RESET}")
        
        if opcion == '1':
            cprint(f"\n🔍 {t('procesando')}", 'cyan', bold=True)
            
            # Verificar fuentes
            verificador = VerificadorFuentes()
            fuentes_global = verificador.verificar_todas(fuentes_global)
            
            # Extraer noticias (guarda automáticamente después de cada fuente)
            extractor = ExtractorNoticias(fuentes_global)
            nuevas = extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
            
            cprint(f"\n✅ {len(nuevas)} {t('incidentes')} nuevos registrados", 'green', bold=True)
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '2':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📊 {t('analisis_completo')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            stats = gestor_global.estadisticas()
            
            cprint(f"\n{Color.YELLOW}📈 ESTADÍSTICAS GENERALES:{Color.RESET}")
            cprint(f"   Total incidentes: {stats['total']}", 'white')
            cprint(f"   Últimos 7 días: {stats['ultimos_7dias']}", 'white')
            cprint(f"   Últimos 30 días: {stats['ultimos_30dias']}", 'white')
            cprint(f"   Últimos 90 días: {stats['ultimos_90dias']}", 'white')
            
            cprint(f"\n{Color.YELLOW}📍 TOP 10 CONDADOS:{Color.RESET}")
            for condado, cantidad in sorted(stats['condados'].items(), key=lambda x: x[1], reverse=True)[:10]:
                pct = (cantidad / stats['total'] * 100) if stats['total'] > 0 else 0
                barra = '█' * int(pct // 2)
                cprint(f"   {condado}: {cantidad} ({pct:.1f}%) {barra}", 'cyan')
            
            cprint(f"\n{Color.YELLOW}🔪 DISTRIBUCIÓN POR TIPO:{Color.RESET}")
            for tipo, cantidad in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                pct = (cantidad / stats['total'] * 100) if stats['total'] > 0 else 0
                icono = TIPOS_CRIMEN.get(tipo, {}).get('icono', '❓')
                cprint(f"   {icono} {tipo.upper()}: {cantidad} ({pct:.1f}%)", 'white')
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '3':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"🔗 {t('conexiones')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            incidentes = gestor_global.datos['incidentes'][-200:]
            grupos = defaultdict(list)
            
            for inc in incidentes:
                grupos[(inc.get('tipo', 'other'), inc.get('condado', 'Unknown'))].append(inc)
            
            patrones = 0
            for (tipo, condado), lista in grupos.items():
                if len(lista) >= 3:
                    cprint(f"\n{Color.RED}🔥 PATRÓN DETECTADO: {len(lista)} {tipo.upper()} en {condado}{Color.RESET}")
                    for inc in sorted(lista, key=lambda x: x['fecha'], reverse=True)[:3]:
                        cprint(f"   • {inc['fecha']}: {inc['titulo'][:70]}...", 'gray')
                    patrones += 1
            
            if patrones == 0:
                cprint(f"\n{Color.GRAY}   No se detectaron patrones significativos.{Color.RESET}")
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '4':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📈 {t('evolucion_mensual')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            evolucion = gestor_global.evolucion_mensual()
            if evolucion:
                max_val = max(evolucion.values())
                for mes, cantidad in list(evolucion.items())[-12:]:
                    barra = '█' * int((cantidad / max_val) * 50) if max_val > 0 else ''
                    cprint(f"   {mes}: {cantidad:3d} {barra}", 'cyan')
            else:
                cprint(f"   {Color.GRAY}No hay datos suficientes.{Color.RESET}")
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '5':
            cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'green', bold=True)
            cprint(f"   📊 Dashboard con gráficos interactivos y paginación", 'cyan')
            cprint(f"   🔪 {t('presiona_ctrl_c')}", 'gray')
            app.run(host='127.0.0.1', port=PUERTO, debug=False, use_reloader=False)
        
        elif opcion == '6':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📰 {t('cmd_ultimos')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            for i, inc in enumerate(gestor_global.datos['incidentes'][-20:][::-1], 1):
                cprint(f"\n{Color.RED}{i:2d}.{Color.RESET} {inc['titulo'][:100]}...", 'white')
                cprint(f"      📅 {inc['fecha']} | 📍 {inc.get('condado', '?')} | 📰 {inc['fuente']} | 🔪 {inc.get('tipo', '?')}", 'gray')
            
            if gestor_global.estadisticas()['total'] == 0:
                cprint(f"   {Color.GRAY}No hay incidentes registrados. Ejecuta búsqueda primero.{Color.RESET}")
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '7':
            cprint(f"\n📥 {t('exportando')}", 'cyan', bold=True)
            gestor_global.exportar_json()
            gestor_global.exportar_csv()
            gestor_global.exportar_html()
            cprint(f"✅ Datos exportados a JSON, CSV y HTML", 'green')
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '8':
            cprint(f"\n🔍 {t('verificando')}", 'cyan', bold=True)
            verificador = VerificadorFuentes()
            fuentes_global = verificador.verificar_todas(fuentes_global)
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '9':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📊 {t('cmd_tipos')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            stats = gestor_global.estadisticas()
            if stats['total'] > 0:
                for tipo, cantidad in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                    pct = (cantidad / stats['total'] * 100)
                    barra_len = 40
                    filled = int(barra_len * cantidad / stats['total'])
                    barra = '█' * filled + '░' * (barra_len - filled)
                    icono = TIPOS_CRIMEN.get(tipo, {}).get('icono', '❓')
                    cprint(f"   {icono} {tipo.upper()}: [{barra}] {cantidad} ({pct:.1f}%)", 'white')
            else:
                cprint(f"   {Color.GRAY}No hay datos.{Color.RESET}")
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '10':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📈 {t('estadisticas_avanzadas')}", 'red', bold=True, bg=True)
            cprint(f"{'='*70}", 'red', bold=True)
            
            stats = gestor_global.estadisticas()
            
            cprint(f"\n{Color.YELLOW}📊 MÉTRICAS AVANZADAS:{Color.RESET}")
            cprint(f"   Densidad de incidentes: {stats['total'] / max(1, len(stats['condados'])):.1f} por condado", 'white')
            cprint(f"   Fuentes por incidente: {stats['total'] / max(1, len(stats['fuentes'])):.2f}", 'white')
            
            if stats['ultimos_30dias'] > 0 and stats['ultimos_90dias'] > 0:
                tendencia = (stats['ultimos_30dias'] / stats['ultimos_90dias'] * 30) if stats['ultimos_90dias'] > 0 else 0
                cprint(f"   Tendencia mensual: {tendencia:.1f} incidentes/mes", 'white')
            
            cprint(f"\n{Color.YELLOW}🔝 PALABRAS CLAVE MÁS FRECUENTES:{Color.RESET}")
            for palabra, count in sorted(stats['top_keywords'].items(), key=lambda x: x[1], reverse=True)[:10]:
                cprint(f"   • {palabra}: {count} veces", 'cyan')
            
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '11':
            cprint(f"\n🧹 {t('limpiando')}", 'cyan', bold=True)
            duplicados = gestor_global.limpiar_duplicados()
            cprint(f"✅ Eliminados {duplicados} incidentes duplicados", 'green')
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '12':
            cprint(f"\n👋 {t('hasta_pronto')}", 'red', bold=True)
            cprint(f"\n{Color.GRAY}🔪 KELTIC KRAKEN - Vigilamos para proteger{Color.RESET}")
            break
        
        else:
            cprint(f"\n❌ {t('opcion_invalida')}", 'red')
            time.sleep(1)

# ============================================================================
# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL - BANNER Y ARRANQUE
# ============================================================================
# ============================================================================

def mostrar_banner_inicial():
    """Muestra el banner de bienvenida con diseño completo"""
    print(f"""
{Color.RED}
╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                   ║
║   ██╗  ██╗███████╗██╗  ████████╗██╗ ██████╗     ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██║
║   ██║ ██╔╝██╔════╝██║  ╚══██╔══╝██║██╔════╝     ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║
║   █████╔╝ █████╗  ██║     ██║   ██║██║          █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║
║   ██╔═██╗ ██╔══╝  ██║     ██║   ██║██║          ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║
║   ██║  ██╗███████╗███████╗██║   ██║╚██████╗     ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║
║   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
║                                                                                                   ║
║   🔪 KELTIC KRAKEN v{VERSION} - IRELAND CRIME INTELLIGENCE PLATFORM                                     ║
║                                                                                                   ║
║   ═══════════════════════════════════════════════════════════════════════════════════════════     ║
║                                                                                                   ║
║   📊 Real-time monitoring: Drug trafficking · Gang violence · Organized crime                     ║
║   🏴 Covers ALL 32 counties including Northern Ireland                                            ║
║   🔄 180+ Rotating User-Agents · Auto-URL discovery · Anti-blocking system                        ║
║   📈 Interactive charts · Full statistics dashboard · Web interface                               ║
║   🔍 Smart retry mechanism · URL cache · Session persistence                                      ║
║   📄 Pagination in web panel · Save after each source · Duplicate removal                         ║
║                                                                                                   ║
║   ═══════════════════════════════════════════════════════════════════════════════════════════     ║
║                                                                                                   ║
║   🛡️  \"Un gran poder conlleva una gran responsabilidad\" - Spider-Man                               ║
║                                                                                                   ║
║                                         - By Condor2026                                           ║
║                                         •SpectrumSecurity•                                        ║
║                                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝
{Color.RESET}""")

if __name__ == '__main__':
    # ================================================================
    # Seleccionar idioma
    # ================================================================
    seleccionar_idioma()
    
    # ================================================================
    # Mostrar banner
    # ================================================================
    mostrar_banner_inicial()
    
    # ================================================================
    # Inicializar gestor y fuentes
    # ================================================================
    gestor_global = GestorDatos()
    fuentes_global = FUENTES_BASE.copy()
    
    # ================================================================
    # Mostrar estadísticas iniciales
    # ================================================================
    stats = gestor_global.estadisticas()
    cprint(f"\n{Color.GREEN}📊 Base de datos: {stats['total']} incidentes almacenados{Color.RESET}")
    cprint(f"{Color.YELLOW}⏳ Última actualización: {gestor_global.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")
    cprint(f"{Color.CYAN}📰 Fuentes configuradas: {len(fuentes_global)} periódicos irlandeses{Color.RESET}")
    cprint(f"{Color.MAGENTA}🔧 Auto-discovery activado | 180+ User-Agents | Guardado después de CADA fuente{Color.RESET}")
    
    # ================================================================
    # Preguntar modo de ejecución
    # ================================================================
    print(f"\n{Color.CYAN}┌{'─' * 50}┐{Color.RESET}")
    print(f"{Color.CYAN}│{Color.WHITE}  ¿Cómo deseas ejecutar?{' ' * 25}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}├{'─' * 50}┤{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [1] Modo Terminal (recomendado){' ' * 7}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [2] Modo Web (dashboard con gráficos){' ' * 5}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}└{'─' * 50}┘{Color.RESET}")
    
    modo = input(f"\n{Color.CYAN}➤ {Color.YELLOW}Elige: {Color.RESET}")
    
    if modo == '2':
        cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'green', bold=True)
        cprint(f"   📊 Dashboard con gráficos: Barras, Dona, Línea y Ranking", 'cyan')
        cprint(f"   📄 Paginación: {ITEMS_POR_PAGINA} incidentes por página", 'cyan')
        cprint(f"   🔪 Auto-discovery activado para URLs caídas", 'cyan')
        cprint(f"   💾 Guardado automático después de CADA fuente", 'green')
        cprint(f"   {Color.GRAY}Presiona Ctrl+C para volver al menú{Color.RESET}")
        app.run(host='127.0.0.1', port=PUERTO, debug=False, use_reloader=False)
    else:
        menu()
