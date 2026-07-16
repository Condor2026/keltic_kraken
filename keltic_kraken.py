#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Condor2026 / SpectrumSecurity

"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  🔪 KELTIC KRAKEN v3.0 - IRELAND CRIME INTELLIGENCE PLATFORM                                                  ║
║  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════  ║
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
import asyncio
import aiohttp
import concurrent.futures
import gc
import psutil
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, Response
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import Lock
from contextlib import contextmanager

# ============================================================================
# ============================================================================
# LANGUAGE SELECTOR
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
# COLORES
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
# CONFIGURACIÓN
# ============================================================================
# ============================================================================

VERSION = "3.0"
PUERTO = 5014
ARCHIVO_DATOS = 'keltic_kraken_ireland.json'
ARCHIVO_CACHE = 'url_cache_ireland.json'
ARCHIVO_ESTADO = 'estado_fuentes_ireland.json'
ARCHIVO_BACKUP = 'keltic_kraken_backup.json'
PAGINAS_BUSQUEDA = 3
TIMEOUT = 15
MAX_INTENTOS = 2
DELAY_MIN = 0.8
DELAY_MAX = 2.0
ITEMS_POR_PAGINA = 10
MAX_WORKERS = 12
TIMEOUT_PAGINA = 15
TIMEOUT_FUENTE = 40
BATCH_SAVE_SIZE = 25
CACHE_TTL_MINUTOS = 15
MAX_CONEXIONES = 30
MAX_CONEXIONES_POR_HOST = 10

# ============================================================================
# ============================================================================
# USER-AGENTS
# ============================================================================
# ============================================================================

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Android 14; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)',
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_random_delay():
    return random.uniform(DELAY_MIN, DELAY_MAX)

# ============================================================================
# ============================================================================
# GESTOR DE RECURSOS
# ============================================================================
# ============================================================================

class GestorRecursos:
    def __init__(self, max_memory_percent=70, max_cpu_percent=80):
        self.max_memory = max_memory_percent
        self.max_cpu = max_cpu_percent
        self.process = psutil.Process()
        
    @contextmanager
    def limitar_recursos(self):
        try:
            self._limpiar_memoria()
            yield
        finally:
            self._limpiar_memoria()
            
    def _limpiar_memoria(self):
        mem = psutil.virtual_memory()
        if mem.percent > self.max_memory:
            gc.collect()
            
    def deberia_pausar(self):
        mem = psutil.virtual_memory()
        cpu = self.process.cpu_percent()
        return mem.percent > self.max_memory or cpu > self.max_cpu

# ============================================================================
# ============================================================================
# CLIENTE HTTP OPTIMIZADO
# ============================================================================
# ============================================================================

class HttpClientOptimizado:
    def __init__(self, max_connections=MAX_CONEXIONES):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=MAX_CONEXIONES_POR_HOST,
            ttl_dns_cache=300,
            force_close=False,
            enable_cleanup_closed=True
        )
        self.timeout = aiohttp.ClientTimeout(total=20, connect=5, sock_read=15)
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout,
            headers={'Accept-Encoding': 'gzip, deflate'}
        )
        return self
        
    async def __aexit__(self, *args):
        await self.session.close()
        await self.connector.close()
        
    async def fetch(self, url, retry_count=2):
        for intento in range(retry_count + 1):
            try:
                headers = {
                    'User-Agent': get_random_ua(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache'
                }
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 429:
                        await asyncio.sleep(2 ** intento)
                    else:
                        await asyncio.sleep(0.5)
            except (aiohttp.ClientError, asyncio.TimeoutError):
                await asyncio.sleep(0.5 * (intento + 1))
        return None

# ============================================================================
# ============================================================================
# AUTO-DISCOVERY
# ============================================================================
# ============================================================================

class URLAutoDiscoverer:
    def __init__(self):
        self.cache_file = ARCHIVO_CACHE
        self.cache = self.load_cache()
        self.common_paths = [
            'crime', 'crimes', 'news/crime', 'crime-news', 'crime-law',
            'courts', 'justice', 'irish-news/crime', 'category/crime',
            'crime/cork', 'crime/dublin', 'crime/galway', 'crime/limerick',
            'news/crime-and-courts', 'news/justice', 'northern-ireland/crime',
            'crime-ireland', 'irish-crime', 'crime-scene', 'crime-watch',
            'garda-news', 'police-news', 'breaking-crime', 'latest-crime',
            'court-reports', 'trial-news', 'sentencing', 'arrest-news',
            'drug-seizure', 'gang-crime', 'organised-crime', 'paramilitary'
        ]
        
    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def discover_url(self, fuente):
        nombre = fuente['nombre']
        base_url = fuente['base']
        original_url = fuente['url']
        
        if nombre in self.cache and self.cache[nombre].get('url'):
            cached_url = self.cache[nombre]['url']
            try:
                headers = {'User-Agent': get_random_ua()}
                r = requests.get(cached_url, timeout=10, headers=headers)
                if r.status_code == 200:
                    return cached_url
            except:
                pass
        
        for path in self.common_paths:
            urls_to_try = [
                f"{base_url}/{path}" if not base_url.endswith('/') else f"{base_url}{path}",
                f"{base_url}/{path}/",
                f"{base_url}/{path}.html",
                f"{base_url}/?s={path}",
                f"{base_url}/category/{path}",
                f"{base_url}/archives/category/{path}",
                f"{base_url}/news/{path}",
                f"{base_url}/local/{path}",
                f"{base_url}/ireland/{path}",
                f"{base_url}/national/{path}",
            ]
            
            for test_url in urls_to_try[:5]:
                try:
                    headers = {'User-Agent': get_random_ua()}
                    r = requests.get(test_url, timeout=15, headers=headers)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        page_text = soup.get_text().lower()
                        crime_keywords = ['crime', 'drug', 'gang', 'murder', 'garda', 'arrest']
                        if any(keyword in page_text for keyword in crime_keywords):
                            self.cache[nombre] = {
                                'url': test_url,
                                'path': path,
                                'found_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.save_cache()
                            return test_url
                except:
                    continue
            time.sleep(0.2)
        
        return original_url

# ============================================================================
# ============================================================================
# FUENTES DE IRLANDA
# ============================================================================
# ============================================================================

FUENTES_BASE = [
    # NATIONAL
    {'nombre': 'Irish Times', 'url': 'https://www.irishtimes.com/crime-law/', 'base': 'https://www.irishtimes.com', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'RTÉ News', 'url': 'https://www.rte.ie/news/crime/', 'base': 'https://www.rte.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'The Journal', 'url': 'https://www.thejournal.ie/crime/', 'base': 'https://www.thejournal.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Irish Mirror', 'url': 'https://www.irishmirror.ie/news/irish-crime/', 'base': 'https://www.irishmirror.ie', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Irish Examiner', 'url': 'https://www.irishexaminer.com/news/crime/', 'base': 'https://www.irishexaminer.com', 'condado': 'Cork', 'categoria': 'national'},
    {'nombre': 'Newstalk', 'url': 'https://www.newstalk.com/crime', 'base': 'https://www.newstalk.com', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Today FM', 'url': 'https://www.todayfm.com/news/crime/', 'base': 'https://www.todayfm.com', 'condado': 'Dublin', 'categoria': 'national'},
    {'nombre': 'Garda Post', 'url': 'https://www.gardapost.com/', 'base': 'https://www.gardapost.com', 'condado': 'Dublin', 'categoria': 'national'},
    # DUBLIN
    {'nombre': 'Dublin Live', 'url': 'https://www.dublinlive.ie/news/dublin-crime/', 'base': 'https://www.dublinlive.ie', 'condado': 'Dublin', 'categoria': 'local'},
    {'nombre': 'Dublin Gazette', 'url': 'https://dublingazette.com/crime/', 'base': 'https://dublingazette.com', 'condado': 'Dublin', 'categoria': 'local'},
    {'nombre': 'Dublin People', 'url': 'https://dublinpeople.com/news/crime/', 'base': 'https://dublinpeople.com', 'condado': 'Dublin', 'categoria': 'local'},
    # CORK
    {'nombre': 'Cork Beo', 'url': 'https://www.corkbeo.ie/news/cork-crime/', 'base': 'https://www.corkbeo.ie', 'condado': 'Cork', 'categoria': 'local'},
    {'nombre': 'Cork Independent', 'url': 'https://corkindependent.com/category/crime/', 'base': 'https://corkindependent.com', 'condado': 'Cork', 'categoria': 'local'},
    # GALWAY
    {'nombre': 'Connacht Tribune', 'url': 'https://www.connachttribune.ie/category/crime/', 'base': 'https://www.connachttribune.ie', 'condado': 'Galway', 'categoria': 'local'},
    # LIMERICK
    {'nombre': 'Limerick Leader', 'url': 'https://www.limerickleader.ie/news/crime/', 'base': 'https://www.limerickleader.ie', 'condado': 'Limerick', 'categoria': 'local'},
    {'nombre': 'Limerick Post', 'url': 'https://www.limerickpost.ie/category/crime/', 'base': 'https://www.limerickpost.ie', 'condado': 'Limerick', 'categoria': 'local'},
    {'nombre': 'Limerick Live', 'url': 'https://www.limericklive.ie/news/crime/', 'base': 'https://www.limericklive.ie', 'condado': 'Limerick', 'categoria': 'local'},
    # WATERFORD
    {'nombre': 'Waterford News', 'url': 'https://www.waterford-news.ie/news/crime/', 'base': 'https://www.waterford-news.ie', 'condado': 'Waterford', 'categoria': 'local'},
    {'nombre': 'Waterford Live', 'url': 'https://www.waterfordlive.ie/news/crime/', 'base': 'https://www.waterfordlive.ie', 'condado': 'Waterford', 'categoria': 'local'},
    # KERRY
    {'nombre': 'Radio Kerry', 'url': 'https://www.radiokerry.ie/news/crime/', 'base': 'https://www.radiokerry.ie', 'condado': 'Kerry', 'categoria': 'local'},
    # CLARE
    {'nombre': 'Clare Champion', 'url': 'https://www.clarechampion.ie/category/crime/', 'base': 'https://www.clarechampion.ie', 'condado': 'Clare', 'categoria': 'local'},
    {'nombre': 'Clare Echo', 'url': 'https://www.clareecho.ie/category/crime/', 'base': 'https://www.clareecho.ie', 'condado': 'Clare', 'categoria': 'local'},
    {'nombre': 'Clare FM', 'url': 'https://www.clare.fm/news/crime/', 'base': 'https://www.clare.fm', 'condado': 'Clare', 'categoria': 'local'},
    # DONEGAL
    {'nombre': 'Donegal Daily', 'url': 'https://donegaldaily.com/category/crime/', 'base': 'https://donegaldaily.com', 'condado': 'Donegal', 'categoria': 'local'},
    {'nombre': 'Highland Radio', 'url': 'https://highlandradio.com/category/crime/', 'base': 'https://highlandradio.com', 'condado': 'Donegal', 'categoria': 'local'},
    # MAYO
    {'nombre': 'Mayo News', 'url': 'https://www.mayonews.ie/category/crime', 'base': 'https://www.mayonews.ie', 'condado': 'Mayo', 'categoria': 'local'},
    {'nombre': 'Connaught Telegraph', 'url': 'https://www.connaughttelegraph.ie/category/crime/', 'base': 'https://www.connaughttelegraph.ie', 'condado': 'Mayo', 'categoria': 'local'},
    {'nombre': 'Midwest Radio', 'url': 'https://www.midwestradio.ie/news/crime/', 'base': 'https://www.midwestradio.ie', 'condado': 'Mayo', 'categoria': 'local'},
    # WEXFORD
    {'nombre': 'South East Radio', 'url': 'https://southeastradio.ie/news/crime/', 'base': 'https://southeastradio.ie', 'condado': 'Wexford', 'categoria': 'local'},
    # KILDARE
    {'nombre': 'Kildare Now', 'url': 'https://kildarenow.com/crime', 'base': 'https://kildarenow.com', 'condado': 'Kildare', 'categoria': 'local'},
    {'nombre': 'Kildare Post', 'url': 'https://kildarepost.ie/category/crime/', 'base': 'https://kildarepost.ie', 'condado': 'Kildare', 'categoria': 'local'},
    # TIPPERARY
    {'nombre': 'Tipperary Live', 'url': 'https://www.tipperarylive.ie/news/crime/', 'base': 'https://www.tipperarylive.ie', 'condado': 'Tipperary', 'categoria': 'local'},
    {'nombre': 'Tipperary Star', 'url': 'https://www.tipperarystar.ie/news/crime/', 'base': 'https://www.tipperarystar.ie', 'condado': 'Tipperary', 'categoria': 'local'},
    {'nombre': 'Tipp FM', 'url': 'https://www.tippfm.com/news/crime/', 'base': 'https://www.tippfm.com', 'condado': 'Tipperary', 'categoria': 'local'},
    # LOUTH
    {'nombre': 'Louth Live', 'url': 'https://www.louthlive.ie/news/crime/', 'base': 'https://www.louthlive.ie', 'condado': 'Louth', 'categoria': 'local'},
    # SLIGO
    {'nombre': 'Sligo Today', 'url': 'https://sligotoday.ie/category/crime/', 'base': 'https://sligotoday.ie', 'condado': 'Sligo', 'categoria': 'local'},
    {'nombre': 'Ocean FM', 'url': 'https://www.oceanfm.ie/news/crime/', 'base': 'https://www.oceanfm.ie', 'condado': 'Sligo', 'categoria': 'local'},
    # LAOIS
    {'nombre': 'Leinster Express', 'url': 'https://www.leinsterexpress.ie/news/crime/', 'base': 'https://www.leinsterexpress.ie', 'condado': 'Laois', 'categoria': 'local'},
    {'nombre': 'Laois Today', 'url': 'https://www.laoistoday.ie/category/crime/', 'base': 'https://www.laoistoday.ie', 'condado': 'Laois', 'categoria': 'local'},
    # OFFALY
    {'nombre': 'Offaly Independent', 'url': 'https://www.offalyindependent.ie/news/crime/', 'base': 'https://www.offalyindependent.ie', 'condado': 'Offaly', 'categoria': 'local'},
    {'nombre': 'Offaly Express', 'url': 'https://www.offalyexpress.ie/news/crime/', 'base': 'https://www.offalyexpress.ie', 'condado': 'Offaly', 'categoria': 'local'},
    # CAVAN
    {'nombre': 'Cavan Echo', 'url': 'https://www.cavanecho.ie/category/crime/', 'base': 'https://www.cavanecho.ie', 'condado': 'Cavan', 'categoria': 'local'},
    {'nombre': 'Northern Sound', 'url': 'https://www.northernsound.ie/news/crime/', 'base': 'https://www.northernsound.ie', 'condado': 'Cavan', 'categoria': 'local'},
    # MONAGHAN
    {'nombre': 'Monaghan Live', 'url': 'https://monaghanlive.ie/category/crime/', 'base': 'https://monaghanlive.ie', 'condado': 'Monaghan', 'categoria': 'local'},
    # ROSCOMMON
    {'nombre': 'Roscommon Herald', 'url': 'https://www.roscommonherald.ie/news/crime/', 'base': 'https://www.roscommonherald.ie', 'condado': 'Roscommon', 'categoria': 'local'},
    {'nombre': 'Roscommon People', 'url': 'https://roscommonpeople.ie/category/crime/', 'base': 'https://roscommonpeople.ie', 'condado': 'Roscommon', 'categoria': 'local'},
    # WICKLOW
    {'nombre': 'Wicklow News', 'url': 'https://wicklownews.net/category/crime/', 'base': 'https://wicklownews.net', 'condado': 'Wicklow', 'categoria': 'local'},
    # CARLOW
    {'nombre': 'Carlow Live', 'url': 'https://carlowlive.ie/category/crime/', 'base': 'https://carlowlive.ie', 'condado': 'Carlow', 'categoria': 'local'},
    {'nombre': 'Carlow Nationalist', 'url': 'https://carlownationalist.ie/category/crime/', 'base': 'https://carlownationalist.ie', 'condado': 'Carlow', 'categoria': 'local'},
    # MEATH
    {'nombre': 'Meath Chronicle', 'url': 'https://www.meathchronicle.ie/news/crime/', 'base': 'https://www.meathchronicle.ie', 'condado': 'Meath', 'categoria': 'local'},
    {'nombre': 'Meath Live', 'url': 'https://meathlive.ie/category/crime/', 'base': 'https://meathlive.ie', 'condado': 'Meath', 'categoria': 'local'},
    # LONGFORD
    {'nombre': 'Longford Leader', 'url': 'https://www.longfordleader.ie/news/crime/', 'base': 'https://www.longfordleader.ie', 'condado': 'Longford', 'categoria': 'local'},
    {'nombre': 'Longford Live', 'url': 'https://longfordlive.ie/category/crime/', 'base': 'https://longfordlive.ie', 'condado': 'Longford', 'categoria': 'local'},
    # LEITRIM
    {'nombre': 'Leitrim Observer', 'url': 'https://www.leitrimobserver.ie/news/crime/', 'base': 'https://www.leitrimobserver.ie', 'condado': 'Leitrim', 'categoria': 'local'},
    # NORTHERN IRELAND
    {'nombre': 'Irish News', 'url': 'https://www.irishnews.com/news/crime/', 'base': 'https://www.irishnews.com', 'condado': 'Antrim', 'categoria': 'ni'},
    {'nombre': 'Belfast Live', 'url': 'https://www.belfastlive.co.uk/news/belfast-crime/', 'base': 'https://www.belfastlive.co.uk', 'condado': 'Antrim', 'categoria': 'ni'},
    {'nombre': 'News Letter', 'url': 'https://www.newsletter.co.uk/news/crime', 'base': 'https://www.newsletter.co.uk', 'condado': 'Antrim', 'categoria': 'ni'},
    {'nombre': 'Derry Journal', 'url': 'https://www.derryjournal.com/news/crime', 'base': 'https://www.derryjournal.com', 'condado': 'Derry', 'categoria': 'ni'},
    {'nombre': 'Derry Now', 'url': 'https://www.derrynow.com/news/crime', 'base': 'https://www.derrynow.com', 'condado': 'Derry', 'categoria': 'ni'},
    {'nombre': 'Derry News', 'url': 'https://www.derrynews.net/crime/', 'base': 'https://www.derrynews.net', 'condado': 'Derry', 'categoria': 'ni'},
    {'nombre': 'Down Recorder', 'url': 'https://www.thedownrecorder.co.uk/news/crime/', 'base': 'https://www.thedownrecorder.co.uk', 'condado': 'Down', 'categoria': 'ni'},
    {'nombre': 'Newry Reporter', 'url': 'https://www.newryreporter.com/news/crime/', 'base': 'https://www.newryreporter.com', 'condado': 'Down', 'categoria': 'ni'},
    {'nombre': 'Tyrone Times', 'url': 'https://www.tyronetimes.co.uk/news/crime', 'base': 'https://www.tyronetimes.co.uk', 'condado': 'Tyrone', 'categoria': 'ni'},
    {'nombre': 'Armagh I', 'url': 'https://armaghi.com/category/crime/', 'base': 'https://armaghi.com', 'condado': 'Armagh', 'categoria': 'ni'},
    {'nombre': 'Lurgan Mail', 'url': 'https://www.lurganmail.co.uk/news/crime', 'base': 'https://www.lurganmail.co.uk', 'condado': 'Armagh', 'categoria': 'ni'},
    {'nombre': 'Impartial Reporter', 'url': 'https://www.impartialreporter.com/news/crime/', 'base': 'https://www.impartialreporter.com', 'condado': 'Fermanagh', 'categoria': 'ni'},
]

CONDADOS_IRLANDA = [
    'Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kerry', 'Clare', 'Donegal',
    'Mayo', 'Wexford', 'Kildare', 'Tipperary', 'Westmeath', 'Louth', 'Sligo', 'Laois',
    'Offaly', 'Cavan', 'Monaghan', 'Roscommon', 'Wicklow', 'Carlow', 'Meath', 'Longford',
    'Leitrim', 'Antrim', 'Derry', 'Down', 'Tyrone', 'Armagh', 'Fermanagh'
]

PALABRAS_CLAVE_CRIMEN = [
    'drugs', 'cocaine', 'heroin', 'cannabis', 'weed', 'meth', 'trafficking',
    'seizure', 'bust', 'kilos', 'kinahan', 'hutch', 'gang', 'feud', 'gangland',
    'shooting', 'gun attack', 'murder', 'homicide', 'killed', 'fatal', 'dead',
    'stabbed', 'stabbing', 'assault', 'attack', 'violent', 'brawl', 'fight',
    'firearm', 'weapon', 'gun', 'pistol', 'rifle', 'shotgun', 'knife',
    'garda', 'gardaí', 'arrested', 'detained', 'charged', 'convicted',
    'sentenced', 'operation', 'raid', 'search', 'investigation',
    'crackdown', 'task force', 'mafia', 'organized crime', 'racketeering',
    'money laundering', 'extortion', 'kidnapping', 'paramilitary',
    'court', 'trial', 'judge', 'jury', 'verdict', 'sentence', 'prison', 'jail',
    'custody', 'remand', 'bail', 'hearing', 'conviction', 'appeal',
    'crime', 'criminal', 'offender', 'felon', 'convict', 'inmate'
]

TIPOS_CRIMEN = {
    'drugs': {'icono': '💊', 'color': '#8b0000', 'nombre': 'Drug Trafficking'},
    'gang_violence': {'icono': '🔫', 'color': '#ff0000', 'nombre': 'Gang Violence'},
    'murder': {'icono': '💀', 'color': '#000000', 'nombre': 'Murder/Homicide'},
    'assault': {'icono': '👊', 'color': '#cc6600', 'nombre': 'Assault'},
    'robbery': {'icono': '💰', 'color': '#8b6b00', 'nombre': 'Robbery/Theft'},
    'organized_crime': {'icono': '🕴️', 'color': '#4b0082', 'nombre': 'Organized Crime'},
    'garda_op': {'icono': '👮', 'color': '#0066cc', 'nombre': 'Garda Operation'},
    'weapon': {'icono': '🔪', 'color': '#990000', 'nombre': 'Weapon Offense'},
    'other': {'icono': '❓', 'color': '#666666', 'nombre': 'Other Crime'}
}

# ============================================================================
# ============================================================================
# GESTOR DE DATOS
# ============================================================================
# ============================================================================

class GestorDatos:
    def __init__(self):
        self.archivo = ARCHIVO_DATOS
        self.datos = self.cargar()
        self.lock = Lock()
    
    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'incidentes': [], 'ultima_actualizacion': None}
        return {'incidentes': [], 'ultima_actualizacion': None}
    
    def guardar(self):
        try:
            with self.lock:
                self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(self.datos, f, indent=2, ensure_ascii=False)
                return True
        except:
            return False
    
    def agregar_incidentes(self, nuevos):
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
                
                return contador
        except:
            return 0
    
    def detectar_tipo(self, texto):
        tl = texto.lower()
        
        if any(p in tl for p in ['cocaine', 'heroin', 'drugs', 'cannabis', 'weed', 'meth', 'ecstasy', 'trafficking', 'seizure']):
            return 'drugs'
        if any(p in tl for p in ['kinahan', 'hutch', 'gang', 'feud', 'cartel', 'gangland']):
            return 'gang_violence'
        if any(p in tl for p in ['murder', 'homicide', 'killed', 'fatal', 'body found']):
            return 'murder'
        if any(p in tl for p in ['assault', 'stabbed', 'stabbing', 'attack', 'violent']):
            return 'assault'
        if any(p in tl for p in ['robbery', 'theft', 'burglary', 'raid']):
            return 'robbery'
        if any(p in tl for p in ['mafia', 'organized crime', 'racketeering', 'money laundering']):
            return 'organized_crime'
        if any(p in tl for p in ['garda', 'gardaí', 'arrested', 'operation', 'raid']):
            return 'garda_op'
        if any(p in tl for p in ['firearm', 'weapon', 'gun', 'pistol', 'rifle', 'shotgun']):
            return 'weapon'
        return 'other'
    
    def estadisticas(self, incidentes=None):
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
            'top_keywords': defaultdict(int)
        }
        
        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
        
        for inc in incidentes:
            if inc.get('condado'):
                stats['condados'][inc['condado']] += 1
            if inc.get('tipo'):
                stats['tipos'][inc['tipo']] += 1
            if inc.get('fuente'):
                stats['fuentes'][inc['fuente']] += 1
            
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
        
        return stats
    
    def evolucion_mensual(self):
        meses = {}
        for inc in self.datos['incidentes']:
            if inc.get('fecha') and len(inc['fecha']) >= 7:
                mes = inc['fecha'][:7]
                meses[mes] = meses.get(mes, 0) + 1
        return dict(sorted(meses.items()))
    
    def limpiar_duplicados(self):
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
        return json.dumps(self.datos, indent=2, ensure_ascii=False)
    
    def exportar_csv(self):
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
            html += f"<tr><td>{icono} {nombre}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        
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
# VERIFICADOR DE FUENTES
# ============================================================================
# ============================================================================

class VerificadorFuentes:
    def __init__(self):
        self.discoverer = URLAutoDiscoverer()
        self.estado_file = ARCHIVO_ESTADO
    
    def verificar_fuente(self, fuente, aplicar_discovery=True):
        for intento in range(MAX_INTENTOS):
            try:
                headers = {
                    'User-Agent': get_random_ua(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive'
                }
                r = requests.get(fuente['url'], timeout=TIMEOUT, headers=headers, allow_redirects=True)
                if r.status_code == 200:
                    fuente['activo'] = True
                    return fuente, True
                else:
                    time.sleep(get_random_delay())
            except:
                time.sleep(get_random_delay())
        
        if aplicar_discovery:
            nueva_url = self.discoverer.discover_url(fuente)
            if nueva_url != fuente['url']:
                fuente['url'] = nueva_url
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
        cprint(f"\n{'=' * 80}", 'red', bold=True)
        cprint(f"🔍 {t('verificando')}", 'red', bold=True)
        cprint(f"{'=' * 80}", 'red', bold=True)
        
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
        
        print()
        
        cprint(f"\n{'=' * 80}", 'green', bold=True)
        cprint(f"📊 RESULTADOS:", 'green', bold=True)
        cprint(f"   Fuentes activas: {activas} de {total}", 'white')
        cprint(f"   Auto-discovery aplicado: {auto_discovered} URLs encontradas", 'cyan')
        cprint(f"{'=' * 80}", 'green', bold=True)
        
        return verificadas

# ============================================================================
# ============================================================================
# EXTRACTOR DE NOTICIAS OPTIMIZADO
# ============================================================================
# ============================================================================

class ExtractorNoticias:
    def __init__(self, fuentes):
        self.fuentes = fuentes
        self.gestor_local = GestorDatos()
    
    async def _extraer_fuente_async(self, fuente, http_client, paginas=PAGINAS_BUSQUEDA):
        incidentes = []
        url_base = fuente['url']
        
        for pagina in range(1, paginas + 1):
            try:
                if pagina == 1:
                    url = url_base
                else:
                    url = url_base.rstrip('/') + f'/page/{pagina}/'
                
                html = await http_client.fetch(url)
                if not html:
                    break
                
                soup = BeautifulSoup(html, 'lxml')
                elementos = soup.find_all(['article', 'div', 'h1', 'h2', 'h3', 'li'])
                
                for elem in elementos[:30]:
                    texto = elem.get_text().strip()
                    if len(texto) < 40:
                        continue
                    
                    texto_lower = texto.lower()
                    if any(palabra in texto_lower for palabra in PALABRAS_CLAVE_CRIMEN):
                        fecha = datetime.now().strftime('%Y-%m-%d')
                        fecha_elem = soup.find('time')
                        if fecha_elem and fecha_elem.get('datetime'):
                            fecha = fecha_elem.get('datetime')[:10]
                        
                        condado = fuente['condado']
                        for c in CONDADOS_IRLANDA:
                            if c.lower() in texto_lower:
                                condado = c
                                break
                        
                        tipo = self.gestor_local.detectar_tipo(texto)
                        
                        incidentes.append({
                            'id': hashlib.md5(texto.encode()).hexdigest()[:16],
                            'titulo': texto[:500],
                            'fecha': fecha,
                            'condado': condado,
                            'tipo': tipo,
                            'fuente': fuente['nombre']
                        })
                
                time.sleep(0.5)
            except:
                break
        
        return incidentes
    
    async def extraer_todas_paralelo(self, paginas=PAGINAS_BUSQUEDA):
        cprint(f"\n{'=' * 80}", 'red', bold=True)
        cprint(f"🔪 KELTIC KRAKEN - ESCANEO RÁPIDO PARALELO", 'red', bold=True)
        cprint(f"{'=' * 80}", 'red', bold=True)
        
        fuentes_activas = [f for f in self.fuentes if f.get('activo', True)]
        total_activas = len(fuentes_activas)
        
        if total_activas == 0:
            cprint(f"\n⚠️ {t('sin_datos')}", 'yellow')
            return []
        
        http_client = await HttpClientOptimizado(max_connections=MAX_CONEXIONES).__aenter__()
        
        total_incidentes = 0
        total_nuevos = 0
        completadas = 0
        
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        
        async def procesar_fuente(fuente):
            nonlocal total_incidentes, total_nuevos, completadas
            
            async with semaphore:
                try:
                    incidentes = await self._extraer_fuente_async(fuente, http_client, paginas)
                    
                    if incidentes:
                        agregados = self.gestor_local.agregar_incidentes(incidentes)
                        total_incidentes += len(incidentes)
                        total_nuevos += agregados
                        cprint(f"\n✅ {fuente['nombre']}: {len(incidentes)} incidentes ({agregados} nuevos)", 'green')
                    else:
                        cprint(f"\n⚠️ {fuente['nombre']}: 0 incidentes", 'yellow')
                    
                    completadas += 1
                except Exception as e:
                    cprint(f"\n❌ {fuente['nombre']}: Error", 'red')
        
        tasks = [procesar_fuente(f) for f in fuentes_activas]
        await asyncio.gather(*tasks, return_exceptions=True)
        await http_client.__aexit__()
        
        cprint(f"\n{'=' * 80}", 'green', bold=True)
        cprint(f"✅ ESCANEO COMPLETADO", 'green', bold=True)
        cprint(f"   Fuentes procesadas: {completadas}/{total_activas}", 'white')
        cprint(f"   Incidentes encontrados: {total_incidentes}", 'white')
        cprint(f"   Incidentes nuevos guardados: {total_nuevos}", 'white')
        cprint(f"{'=' * 80}", 'green', bold=True)
        
        return self.gestor_local.datos['incidentes']
    
    def extraer_todas(self, paginas=PAGINAS_BUSQUEDA):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.extraer_todas_paralelo(paginas))
        finally:
            loop.close()

# ============================================================================
# ============================================================================
# APLICACIÓN FLASK
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
        body { background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 100%); color: #e0e0e0; font-family: 'Segoe UI', 'Arial', sans-serif; padding: 20px; min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #1a0a0a, #2a0a0a); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; border: 1px solid #ff3333; box-shadow: 0 0 30px rgba(255,0,0,0.2); animation: glow 2s infinite alternate; }
        @keyframes glow { from { box-shadow: 0 0 10px rgba(255,0,0,0.2); } to { box-shadow: 0 0 30px rgba(255,0,0,0.5); } }
        h1 { font-size: 3em; color: #ff4444; letter-spacing: 3px; text-shadow: 0 0 10px #ff0000; animation: pulse 1.5s infinite alternate; }
        @keyframes pulse { from { text-shadow: 0 0 5px #ff0000; } to { text-shadow: 0 0 20px #ff0000; } }
        .version-badge { background: #1a1a1a; color: #ff8888; padding: 5px 20px; border-radius: 30px; display: inline-block; margin-top: 10px; font-family: monospace; border: 1px solid #ff4444; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 30px 0; }
        .stat-card { background: linear-gradient(135deg, #111, #1a1a1a); padding: 20px; border-radius: 15px; text-align: center; border-left: 5px solid #ff4444; transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(255,68,68,0.2); }
        .stat-number { font-size: 2.5em; color: #ff4444; font-weight: bold; }
        .stat-label { color: #888; margin-top: 10px; font-size: 0.9em; }
        .btn { background: #222; color: #ff4444; border: 2px solid #ff4444; padding: 12px 30px; border-radius: 40px; font-size: 1em; font-weight: bold; cursor: pointer; margin: 10px; transition: all 0.3s ease; text-decoration: none; display: inline-block; }
        .btn:hover { background: #ff4444; color: #000; transform: scale(1.05); box-shadow: 0 0 15px #ff4444; }
        .charts-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 25px; margin: 30px 0; }
        .chart-container { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #333; transition: all 0.3s ease; }
        .chart-container:hover { border-color: #ff4444; box-shadow: 0 0 15px rgba(255,68,68,0.1); }
        .chart-title { color: #ff6666; font-size: 1.2em; margin-bottom: 15px; text-align: center; font-weight: bold; }
        .filtros { display: flex; gap: 15px; justify-content: center; margin: 30px 0; flex-wrap: wrap; }
        .filtro-btn { background: #1a1a1a; color: #ccc; border: 2px solid #333; padding: 10px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; transition: all 0.3s ease; }
        .filtro-btn:hover, .filtro-btn.active { background: #ff4444; color: #000; border-color: #ff4444; }
        .incidente-card { background: linear-gradient(135deg, #0a0a0a, #111); margin: 12px 0; padding: 18px; border-radius: 12px; border-left: 6px solid #ff4444; transition: all 0.3s ease; }
        .incidente-card:hover { transform: translateX(10px); background: #1a1a1a; }
        .incidente-titulo { font-size: 1.05em; font-weight: bold; margin-bottom: 8px; color: #fff; }
        .incidente-meta { color: #888; display: flex; gap: 15px; flex-wrap: wrap; font-size: 0.85em; }
        .incidente-meta span { background: #1a1a1a; padding: 4px 10px; border-radius: 20px; }
        .pagination { display: flex; justify-content: center; align-items: center; gap: 10px; margin: 25px 0; flex-wrap: wrap; }
        .page-btn { background: #222; color: #ff4444; padding: 8px 16px; border-radius: 20px; text-decoration: none; border: 1px solid #ff4444; transition: all 0.3s ease; min-width: 40px; text-align: center; }
        .page-btn:hover, .page-btn.active { background: #ff4444; color: #000; }
        .page-info { color: #888; margin: 0 15px; }
        .footer { text-align: center; margin-top: 50px; padding: 20px; background: #111; border-radius: 15px; color: #666; border-top: 1px solid #333; }
        @media (max-width: 768px) { .charts-row { grid-template-columns: 1fr; } h1 { font-size: 1.8em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
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
            <div class="stat-card"><div class="stat-number">{{ stats.total }}</div><div class="stat-label">📊 TOTAL INCIDENTS</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.ultimos_7dias }}</div><div class="stat-label">⚡ LAST 7 DAYS</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.ultimos_30dias }}</div><div class="stat-label">🔥 LAST 30 DAYS</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.ultimos_90dias }}</div><div class="stat-label">📊 LAST 90 DAYS</div></div>
            <div class="stat-card"><div class="stat-number">{{ periodicos_activos }}</div><div class="stat-label">📰 ACTIVE SOURCES</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.condados|length }}</div><div class="stat-label">🏴 COUNTIES AFFECTED</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.tipos|length }}</div><div class="stat-label">🔪 CRIME TYPES</div></div>
            <div class="stat-card"><div class="stat-number">{{ stats.fuentes|length }}</div><div class="stat-label">📰 SOURCES WITH DATA</div></div>
        </div>
        
        <div style="text-align: center;">
            <form action="/actualizar" method="post" style="display: inline;"><button class="btn">🔄 UPDATE DATA</button></form>
            <a href="/exportar/json" class="btn">📥 JSON</a>
            <a href="/exportar/csv" class="btn">📥 CSV</a>
            <a href="/exportar/html" class="btn">📄 HTML REPORT</a>
        </div>
        
        <div class="filtros">
            <a href="/page/1?filtro=todo" class="filtro-btn {% if filtro == 'todo' %}active{% endif %}">📅 ALL</a>
            <a href="/page/1?filtro=7d" class="filtro-btn {% if filtro == '7d' %}active{% endif %}">⚡ 7 DAYS</a>
            <a href="/page/1?filtro=30d" class="filtro-btn {% if filtro == '30d' %}active{% endif %}">🔥 30 DAYS</a>
            <a href="/page/1?filtro=90d" class="filtro-btn {% if filtro == '90d' %}active{% endif %}">📊 90 DAYS</a>
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
            <div class="chart-title">🔪 LATEST INCIDENTS - Page {{ pagina }} of {{ total_paginas }}</div>
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
            
            <div class="pagination">
                {% if pagina > 1 %}<a href="/page/{{ pagina-1 }}?filtro={{ filtro }}" class="page-btn">◀ PREVIOUS</a>{% endif %}
                {% for p in range(1, total_paginas + 1) %}
                    {% if p == 1 or p == total_paginas or (p >= pagina-2 and p <= pagina+2) %}
                        {% if p == pagina %}<span class="page-btn active">{{ p }}</span>
                        {% else %}<a href="/page/{{ p }}?filtro={{ filtro }}" class="page-btn">{{ p }}</a>{% endif %}
                    {% elif p == pagina-3 or p == pagina+3 %}<span class="page-info">...</span>{% endif %}
                {% endfor %}
                {% if pagina < total_paginas %}<a href="/page/{{ pagina+1 }}?filtro={{ filtro }}" class="page-btn">NEXT ▶</a>{% endif %}
            </div>
            <div class="page-info" style="text-align: center; margin-top: 10px;">
                Showing {{ (pagina-1)*ITEMS_POR_PAGINA + 1 }} to {{ (pagina-1)*ITEMS_POR_PAGINA + incidentes_pagina|length }} of {{ total_incidentes }} incidents
            </div>
        </div>
        
        <div class="footer">
            <p>🔪 KELTIC KRAKEN v{{ version }} · {{ periodicos_activos }} ACTIVE SOURCES</p>
            <p style="font-size:0.8em;">"Un gran poder conlleva una gran responsabilidad" - Spider-Man</p>
        </div>
    </div>
    
    <script>
        new Chart(document.getElementById('countyChart'), {
            type: 'bar',
            data: { labels: {{ condados_labels|tojson }}, datasets: [{ label: 'Incidents', data: {{ condados_data|tojson }}, backgroundColor: 'rgba(255,68,68,0.7)', borderColor: '#ff4444', borderWidth: 2, borderRadius: 5 }] },
            options: { responsive: true, plugins: { legend: { labels: { color: '#ccc' } } }, scales: { y: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, x: { ticks: { color: '#ccc', rotation: 45 } } } }
        });
        
        new Chart(document.getElementById('typeChart'), {
            type: 'doughnut',
            data: { labels: {{ tipos_labels|tojson }}, datasets: [{ data: {{ tipos_data|tojson }}, backgroundColor: ['#8b0000','#ff0000','#000000','#cc6600','#8b6b00','#4b0082','#0066cc','#990000','#666666'], borderWidth: 2, borderColor: '#1a1a1a' }] },
            options: { responsive: true, plugins: { legend: { labels: { color: '#ccc' } } } }
        });
        
        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: { labels: {{ tendencia_labels|tojson }}, datasets: [{ label: 'Incidents per month', data: {{ tendencia_data|tojson }}, borderColor: '#ff4444', backgroundColor: 'rgba(255,68,68,0.1)', fill: true, tension: 0.4, pointBackgroundColor: '#ff4444', pointBorderColor: '#fff', pointRadius: 5 }] },
            options: { responsive: true, plugins: { legend: { labels: { color: '#ccc' } } }, scales: { y: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, x: { ticks: { color: '#ccc', rotation: 45 } } } }
        });
        
        new Chart(document.getElementById('sourcesChart'), {
            type: 'bar',
            data: { labels: {{ fuentes_labels|tojson }}, datasets: [{ label: 'Articles', data: {{ fuentes_data|tojson }}, backgroundColor: 'rgba(255,102,102,0.7)', borderColor: '#ff6666', borderWidth: 2, borderRadius: 5 }] },
            options: { responsive: true, indexAxis: 'y', plugins: { legend: { labels: { color: '#ccc' } } }, scales: { x: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, y: { ticks: { color: '#ccc' } } } }
        });
    </script>
</body>
</html>
'''

# ============================================================================
# ============================================================================
# RUTAS DE FLASK
# ============================================================================
# ============================================================================

@app.route('/')
def index():
    return index_paginada(1, 'todo')

@app.route('/page/<int:page>')
def index_paginada(page=1, filtro='todo'):
    global gestor_global, fuentes_global
    
    # Obtener filtro de query string
    filtro = request.args.get('filtro', 'todo')
    
    incidentes = gestor_global.datos['incidentes']
    
    if filtro == '7d':
        limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '30d':
        limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '90d':
        limite = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    
    stats = gestor_global.estadisticas(incidentes)
    periodicos_activos = len([f for f in fuentes_global if f.get('activo', True)])
    
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
    
    total_incidentes = len(incidentes)
    total_paginas = max(1, (total_incidentes + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA)
    pagina = max(1, min(page, total_paginas))
    inicio = (pagina - 1) * ITEMS_POR_PAGINA
    fin = inicio + ITEMS_POR_PAGINA
    incidentes_pagina = incidentes[::-1][inicio:fin]
    
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidentes_pagina=incidentes_pagina,
        periodicos_activos=periodicos_activos,
        filtro=filtro,
        pagina=pagina,
        total_paginas=total_paginas,
        total_incidentes=total_incidentes,
        condados_labels=condados_labels,
        condados_data=condados_data,
        tipos_labels=tipos_labels,
        tipos_data=tipos_data,
        tendencia_labels=tendencia_labels,
        tendencia_data=tendencia_data,
        fuentes_labels=fuentes_labels,
        fuentes_data=fuentes_data,
        ITEMS_POR_PAGINA=ITEMS_POR_PAGINA
    )

@app.route('/actualizar', methods=['POST'])
def actualizar():
    global gestor_global, fuentes_global
    
    cprint(f"\n{'=' * 80}", 'red', bold=True)
    cprint(f"🔪 {t('actualizando')}", 'red', bold=True)
    cprint(f"{'=' * 80}", 'red', bold=True)
    
    verificador = VerificadorFuentes()
    fuentes_verificadas = verificador.verificar_todas(fuentes_global)
    fuentes_global = fuentes_verificadas
    
    extractor = ExtractorNoticias(fuentes_verificadas)
    extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
    
    cprint(f"\n{'=' * 80}", 'green', bold=True)
    cprint(f"✅ PROCESO COMPLETADO", 'green', bold=True)
    cprint(f"{'=' * 80}", 'green', bold=True)
    
    return index_paginada(1, 'todo')

@app.route('/exportar/json')
def exportar_json():
    return Response(gestor_global.exportar_json(), mimetype='application/json', headers={'Content-Disposition': 'attachment; filename=keltic_kraken_export.json'})

@app.route('/exportar/csv')
def exportar_csv():
    return Response(gestor_global.exportar_csv(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=keltic_kraken_export.csv'})

@app.route('/exportar/html')
def exportar_html():
    return Response(gestor_global.exportar_html(), mimetype='text/html', headers={'Content-Disposition': 'attachment; filename=keltic_kraken_report.html'})

# ============================================================================
# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================
# ============================================================================

def mostrar_menu_principal():
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
{Color.YELLOW}│{Color.CYAN}  📋 {t('menu_title')}{' ' * 30}{Color.YELLOW}│{Color.RESET}
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
{Color.YELLOW}│{Color.RED}  [12] 🗑️ {t('cmd_salir')}{' ' * 18}{Color.YELLOW}│{Color.RESET}
{Color.YELLOW}└{'─' * 50}┘{Color.RESET}
""")

def menu():
    global gestor_global, fuentes_global
    
    while True:
        mostrar_menu_principal()
        opcion = input(f"{Color.CYAN}➤ {Color.YELLOW}Opción: {Color.RESET}")
        
        if opcion == '1':
            cprint(f"\n🔍 {t('procesando')}", 'cyan', bold=True)
            verificador = VerificadorFuentes()
            fuentes_global = verificador.verificar_todas(fuentes_global)
            extractor = ExtractorNoticias(fuentes_global)
            nuevas = extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
            cprint(f"\n✅ {len(nuevas)} {t('incidentes')} nuevos registrados", 'green', bold=True)
            input(f"\n{Color.GRAY}Presiona Enter para continuar...{Color.RESET}")
        
        elif opcion == '2':
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"📊 {t('analisis_completo')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
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
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"🔗 {t('conexiones')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
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
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"📈 {t('evolucion_mensual')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
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
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"📰 {t('cmd_ultimos')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
            incidentes = gestor_global.datos['incidentes']
            if incidentes:
                for i, inc in enumerate(incidentes[-20:][::-1], 1):
                    cprint(f"\n{Color.RED}{i:2d}.{Color.RESET} {inc['titulo'][:100]}...", 'white')
                    cprint(f"      📅 {inc['fecha']} | 📍 {inc.get('condado', '?')} | 📰 {inc['fuente']} | 🔪 {inc.get('tipo', '?')}", 'gray')
            else:
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
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"📊 {t('cmd_tipos')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
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
            cprint(f"\n{'=' * 70}", 'red', bold=True)
            cprint(f"📈 {t('estadisticas_avanzadas')}", 'red', bold=True)
            cprint(f"{'=' * 70}", 'red', bold=True)
            
            stats = gestor_global.estadisticas()
            cprint(f"\n{Color.YELLOW}📊 MÉTRICAS AVANZADAS:{Color.RESET}")
            cprint(f"   Densidad de incidentes: {stats['total'] / max(1, len(stats['condados'])):.1f} por condado", 'white')
            cprint(f"   Fuentes por incidente: {stats['total'] / max(1, len(stats['fuentes'])):.2f}", 'white')
            
            if stats['ultimos_30dias'] > 0 and stats['ultimos_90dias'] > 0:
                tendencia = (stats['ultimos_30dias'] / stats['ultimos_90dias'] * 30) if stats['ultimos_90dias'] > 0 else 0
                cprint(f"   Tendencia mensual: {tendencia:.1f} incidentes/mes", 'white')
            
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
# BANNER DE INICIO
# ============================================================================
# ============================================================================

def mostrar_banner_inicial():
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
║   ⚡ Parallel scanning · {MAX_WORKERS} concurrent workers · Non-blocking                                   ║
║                                                                                                   ║
║   ═══════════════════════════════════════════════════════════════════════════════════════════     ║
║                                                                                                   ║
║   🛡️  "Un gran poder conlleva una gran responsabilidad" - Spider-Man                              ║
║                                                                                                   ║
║                                         - By Condor2026                                           ║
║                                         •SpectrumSecurity•                                        ║
║                                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝
{Color.RESET}""")

# ============================================================================
# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================
# ============================================================================

if __name__ == '__main__':
    seleccionar_idioma()
    mostrar_banner_inicial()
    
    gestor_global = GestorDatos()
    fuentes_global = FUENTES_BASE.copy()
    
    stats = gestor_global.estadisticas()
    cprint(f"\n{Color.GREEN}📊 Base de datos: {stats['total']} incidentes almacenados{Color.RESET}")
    cprint(f"{Color.YELLOW}⏳ Última actualización: {gestor_global.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")
    cprint(f"{Color.CYAN}📰 Fuentes configuradas: {len(fuentes_global)} periódicos irlandeses{Color.RESET}")
    cprint(f"{Color.MAGENTA}🔧 Auto-discovery activado | 180+ User-Agents | Guardado después de CADA fuente{Color.RESET}")
    cprint(f"{Color.GREEN}⚡ Escaneo paralelo activado | {MAX_WORKERS} workers simultáneos | Sin bloqueos{Color.RESET}")
    
    print(f"\n{Color.CYAN}┌{'─' * 50}┐{Color.RESET}")
    print(f"{Color.CYAN}│{Color.WHITE}  ¿Cómo deseas ejecutar?{' ' * 27}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}├{'─' * 50}┤{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [1] Modo Terminal (recomendado){' ' * 17}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [2] Modo Web (dashboard con gráficos){' ' * 11}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}└{'─' * 50}┘{Color.RESET}")
    
    modo = input(f"\n{Color.CYAN}➤ {Color.YELLOW}Elige: {Color.RESET}")
    
    if modo == '2':
        cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'green', bold=True)
        cprint(f"   📊 Dashboard con gráficos: Barras, Dona, Línea y Ranking", 'cyan')
        cprint(f"   📄 Paginación: {ITEMS_POR_PAGINA} incidentes por página", 'cyan')
        cprint(f"   🔪 Auto-discovery activado para URLs caídas", 'cyan')
        cprint(f"   💾 Guardado automático después de CADA fuente", 'green')
        cprint(f"   ⚡ Escaneo paralelo con {MAX_WORKERS} workers", 'cyan')
        cprint(f"   {Color.GRAY}Presiona Ctrl+C para volver al menú{Color.RESET}")
        app.run(host='127.0.0.1', port=PUERTO, debug=False, use_reloader=False)
    else:
        menu()
