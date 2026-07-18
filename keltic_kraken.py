#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Condor2026 / SpectrumSecurity

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Condor2026 / SpectrumSecurity

"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║   ██╗  ██╗███████╗██╗  ████████╗██╗ ██████╗     ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██║            ║
║   ██║ ██╔╝██╔════╝██║  ╚══██╔══╝██║██╔════╝     ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║            ║
║   █████╔╝ █████╗  ██║     ██║   ██║██║          █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║            ║
║   ██╔═██╗ ██╔══╝  ██║     ██║   ██║██║          ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║            ║
║   ██║  ██╗███████╗███████╗██║   ██║╚██████╗     ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║            ║
║   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝            ║
║                                                                                                               ║
║  🦈 KELTIC KRAKEN v3.4 - IRELAND CRIME INTELLIGENCE PLATFORM - ULTRA STABLE                                   ║
║  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════  ║
║  🌍 Mapa 3D con MapLibre GL · Puntos interactivos · Tooltips con severidad · 32 condados                      ║
║  ⚡ ESCANEO ESTABLE · Timeouts controlados · Sin bloqueos · URLs 2026                                          ║
║  📊 Real-time monitoring: Drug trafficking · Gang violence · Organized crime                                  ║
║  🏴 Covers ALL 32 counties including Northern Ireland                                                         ║
║  🔄 100+ Rotating User-Agents · Auto-URL discovery · Anti-blocking system                                     ║
║  📈 Interactive charts · Full statistics dashboard · Web interface                                            ║
║  🔍 Smart retry mechanism · URL cache · Session persistence                                                   ║
║  📄 Pagination in web panel · Save after each source · Duplicate removal                                      ║
║  ⚡ Parallel scanning · Dynamic workers · Non-blocking · Ultra-fast                                            ║
║  🚀 Cache memorizado · Parsing optimizado · Regex compilados                                                  ║
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
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, Response, jsonify, redirect, url_for
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import RLock
from typing import Dict, List, Optional, Any
import logging
from functools import lru_cache
import urllib.parse

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keltic_kraken.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTES GLOBALES
# ============================================================================

VERSION = "4.1"
PUERTO = 5025
ARCHIVO_DATOS = 'keltic_kraken_ireland.json'
ARCHIVO_CACHE = 'url_cache_ireland.json'
ARCHIVO_ESTADO = 'estado_fuentes_ireland.json'
ARCHIVO_BACKUP = 'keltic_kraken_backup.json'
PAGINAS_BUSQUEDA = 2

TIMEOUT = 10
MAX_INTENTOS = 3

DELAY_MIN = 1.5
DELAY_MAX = 3.5
DELAY_ENTRE_FUENTES = 1.5

ITEMS_POR_PAGINA = 15
MAX_WORKERS = 3
TIMEOUT_PAGINA = 10
TIMEOUT_FUENTE = 15
BATCH_SAVE_SIZE = 25
CACHE_TTL_MINUTOS = 15
MAX_CONEXIONES = 8
MAX_CONEXIONES_POR_HOST = 2

# ============================================================================
# COLORES
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
# USER-AGENTS (180+)
# ============================================================================

USER_AGENTS = [
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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.129 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
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
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0.1',
    'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36 Edg/125.0.6422.60',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.42 Safari/537.36 Edg/125.0.6422.42',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36 Edg/124.0.6367.118',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36 Edg/124.0.6367.91',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.62 Safari/537.36 Edg/124.0.6367.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36 OPR/110.0.5322.60',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36 OPR/109.0.5322.118',
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
    'Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Android 14; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0',
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_random_delay():
    return random.uniform(DELAY_MIN, DELAY_MAX)

# ============================================================================
# SISTEMA DE DETECCIÓN INTELIGENTE DE DELITOS (COMPACTO)
# ============================================================================

PESOS_DELITOS = {
    'murder': {'palabras': ['murder', 'homicide', 'killed', 'fatal', 'dead', 'death', 'slain', 'shot dead', 'stabbed to death'], 'peso': 10, 'contexto': ['police', 'investigation', 'arrest', 'suspect', 'crime scene', 'victim']},
    'gang_violence': {'palabras': ['kinahan', 'hutch', 'gang', 'feud', 'cartel', 'gangland', 'gangster', 'drug gang'], 'peso': 9, 'contexto': ['shooting', 'attack', 'rival', 'territory']},
    'drugs': {'palabras': ['cocaine', 'heroin', 'cannabis', 'weed', 'meth', 'ecstasy', 'trafficking', 'seizure', 'drugs', 'kilos', 'drug bust', 'drug raid'], 'peso': 8, 'contexto': ['arrest', 'operation', 'garda', 'seized', 'worth', 'street value']},
    'organized_crime': {'palabras': ['mafia', 'organized crime', 'racketeering', 'money laundering', 'extortion', 'syndicate'], 'peso': 8, 'contexto': ['operation', 'arrest', 'investigation', 'network', 'international']},
    'weapon': {'palabras': ['firearm', 'weapon', 'gun', 'pistol', 'rifle', 'shotgun', 'knife', 'blade', 'armed', 'weapons', 'arsenal'], 'peso': 7, 'contexto': ['seized', 'found', 'recovered', 'confiscated']},
    'assault': {'palabras': ['assault', 'stabbed', 'stabbing', 'attack', 'violent', 'brawl', 'fight', 'injured', 'beat', 'beaten'], 'peso': 6, 'contexto': ['hospital', 'injuries', 'victim']},
    'robbery': {'palabras': ['robbery', 'theft', 'burglary', 'raid', 'heist', 'stolen', 'steal', 'thief', 'larceny'], 'peso': 5, 'contexto': ['cash', 'jewelry', 'valuables', 'safe']},
    'garda_op': {'palabras': ['garda', 'gardaí', 'arrested', 'operation', 'raid', 'crackdown', 'task force', 'police', 'detective'], 'peso': 4, 'contexto': ['successful', 'drugs', 'weapons', 'cash']}
}

PALABRAS_FILTRO_NEGATIVO = ['weather', 'sport', 'football', 'rugby', 'gaa', 'music', 'concert', 'festival', 'education', 'school', 'university', 'college', 'business', 'economy', 'stock', 'technology', 'apple', 'google', 'facebook', 'twitter', 'instagram', 'travel', 'holiday', 'tourism', 'hotel', 'restaurant', 'recipe', 'cooking']

def detectar_tipo_inteligente(texto):
    texto_lower = re.sub(r'[^a-zA-Záéíóúñ\s]', ' ', texto.lower())
    neg_count = sum(1 for p in PALABRAS_FILTRO_NEGATIVO if p in texto_lower)
    if neg_count >= 3:
        return 'other'
    
    puntuaciones = defaultdict(int)
    for tipo, config in PESOS_DELITOS.items():
        for palabra in config['palabras']:
            if palabra in texto_lower:
                count = texto_lower.count(palabra)
                puntuaciones[tipo] += config['peso'] * (1 + count * 0.5)
        for ctx_palabra in config.get('contexto', []):
            if ctx_palabra in texto_lower:
                puntuaciones[tipo] += config['peso'] * 0.3
    
    if any(p in texto_lower for p in ['fatal', 'dead', 'killed']) and any(p in texto_lower for p in ['shooting', 'stabbing', 'attack', 'gun']):
        puntuaciones['murder'] += 5
    if any(p in texto_lower for p in ['cocaine', 'heroin', 'cannabis', 'drugs']) and any(p in texto_lower for p in ['€', 'euro', 'worth', 'kilos', 'seized']):
        puntuaciones['drugs'] += 4
    
    if puntuaciones:
        max_score = max(puntuaciones.values())
        if max_score > 0:
            if max_score < 3:
                return 'other'
            return max(puntuaciones.items(), key=lambda x: x[1])[0]
    
    if any(p in texto_lower for p in ['crime', 'criminal', 'arrest', 'police', 'garda', 'incident', 'investigation']):
        return 'other'
    return 'other'

def extraer_condado_inteligente(texto, fuente_condado=None):
    texto_lower = texto.lower()
    for condado in COORDENADAS_CONDADOS.keys():
        if condado.lower() in texto_lower:
            return condado
    if fuente_condado:
        return fuente_condado
    return 'Dublin'

# ============================================================================
# COORDENADAS Y TIPOS
# ============================================================================

COORDENADAS_CONDADOS = {
    'Dublin': {'lat': 53.3498, 'lon': -6.2603}, 'Cork': {'lat': 51.8985, 'lon': -8.4756},
    'Galway': {'lat': 53.2707, 'lon': -9.0568}, 'Limerick': {'lat': 52.6638, 'lon': -8.6267},
    'Waterford': {'lat': 52.2593, 'lon': -7.1101}, 'Kerry': {'lat': 52.1545, 'lon': -9.5661},
    'Clare': {'lat': 52.8210, 'lon': -8.9930}, 'Donegal': {'lat': 54.6549, 'lon': -8.1108},
    'Mayo': {'lat': 53.7607, 'lon': -9.6528}, 'Wexford': {'lat': 52.3343, 'lon': -6.4575},
    'Kildare': {'lat': 53.1598, 'lon': -6.9066}, 'Tipperary': {'lat': 52.4738, 'lon': -8.1614},
    'Westmeath': {'lat': 53.4969, 'lon': -7.3647}, 'Louth': {'lat': 53.9500, 'lon': -6.5000},
    'Sligo': {'lat': 54.2680, 'lon': -8.4694}, 'Laois': {'lat': 52.9943, 'lon': -7.3323},
    'Offaly': {'lat': 53.2630, 'lon': -7.4500}, 'Cavan': {'lat': 53.9908, 'lon': -7.3606},
    'Monaghan': {'lat': 54.2490, 'lon': -6.9670}, 'Roscommon': {'lat': 53.6334, 'lon': -8.1901},
    'Wicklow': {'lat': 52.9850, 'lon': -6.3681}, 'Carlow': {'lat': 52.8308, 'lon': -6.9266},
    'Meath': {'lat': 53.6090, 'lon': -6.6600}, 'Longford': {'lat': 53.7276, 'lon': -7.7990},
    'Leitrim': {'lat': 54.1196, 'lon': -8.0049}, 'Antrim': {'lat': 54.7137, 'lon': -6.2226},
    'Derry': {'lat': 54.9972, 'lon': -7.3092}, 'Down': {'lat': 54.3386, 'lon': -5.9320},
    'Tyrone': {'lat': 54.6074, 'lon': -6.8698}, 'Armagh': {'lat': 54.3486, 'lon': -6.6668},
    'Fermanagh': {'lat': 54.3477, 'lon': -7.6443},
}

TIPOS_CRIMEN = {
    'drugs': {'icono': '💊', 'color': '#ff0000', 'nombre': 'Drug Trafficking'},
    'gang_violence': {'icono': '🔫', 'color': '#ff4444', 'nombre': 'Gang Violence'},
    'murder': {'icono': '💀', 'color': '#000000', 'nombre': 'Murder/Homicide'},
    'assault': {'icono': '👊', 'color': '#ff8c00', 'nombre': 'Assault'},
    'robbery': {'icono': '💰', 'color': '#ffd700', 'nombre': 'Robbery/Theft'},
    'organized_crime': {'icono': '🕴️', 'color': '#800080', 'nombre': 'Organized Crime'},
    'garda_op': {'icono': '👮', 'color': '#0066cc', 'nombre': 'Garda Operation'},
    'weapon': {'icono': '🔪', 'color': '#990000', 'nombre': 'Weapon Offense'},
    'other': {'icono': '❓', 'color': '#666666', 'nombre': 'Other Crime'}
}

PALABRAS_CLAVE_CRIMEN = ['drugs', 'cocaine', 'heroin', 'cannabis', 'weed', 'meth', 'ecstasy', 'trafficking', 'seizure', 'drug bust', 'gang', 'feud', 'kinahan', 'hutch', 'shooting', 'gun attack', 'murder', 'homicide', 'killed', 'fatal', 'assault', 'stabbed', 'stabbing', 'attack', 'violent', 'robbery', 'theft', 'garda', 'gardaí', 'arrested', 'operation', 'raid', 'crackdown', 'organized crime', 'mafia', 'money laundering', 'extortion', 'weapon', 'firearm']

# ============================================================================
# FUENTES DE IRLANDA - 78+ FUENTES (COMPACTO)
# ============================================================================

FUENTES_BASE = [
    {'nombre': 'Irish Times', 'url': 'https://www.irishtimes.com/news/crime-and-law/', 'base': 'https://www.irishtimes.com', 'condado': 'Dublin'},
    {'nombre': 'RTÉ News', 'url': 'https://www.rte.ie/news/crime/', 'base': 'https://www.rte.ie', 'condado': 'Dublin'},
    {'nombre': 'The Journal', 'url': 'https://www.thejournal.ie/crime/', 'base': 'https://www.thejournal.ie', 'condado': 'Dublin'},
    {'nombre': 'Irish Independent', 'url': 'https://www.independent.ie/irish-news/', 'base': 'https://www.independent.ie', 'condado': 'Dublin'},
    {'nombre': 'Irish Examiner', 'url': 'https://www.irishexaminer.com/news/crime/', 'base': 'https://www.irishexaminer.com', 'condado': 'Cork'},
    {'nombre': 'Irish Mirror', 'url': 'https://www.irishmirror.ie/news/irish-news/', 'base': 'https://www.irishmirror.ie', 'condado': 'Dublin'},
    {'nombre': 'Sunday World', 'url': 'https://www.sundayworld.com/news/', 'base': 'https://www.sundayworld.com', 'condado': 'Dublin'},
    {'nombre': 'The Irish Sun', 'url': 'https://www.thesun.ie/news/', 'base': 'https://www.thesun.ie', 'condado': 'Dublin'},
    {'nombre': 'Irish Daily Star', 'url': 'https://www.irishdailystar.ie/news/', 'base': 'https://www.irishdailystar.ie', 'condado': 'Dublin'},
    {'nombre': 'The Irish Post', 'url': 'https://www.irishpost.com/news/', 'base': 'https://www.irishpost.com', 'condado': 'Dublin'},
    {'nombre': 'Dublin Live', 'url': 'https://www.dublinlive.ie/news/', 'base': 'https://www.dublinlive.ie', 'condado': 'Dublin'},
    {'nombre': 'Dublin Gazette', 'url': 'https://dublingazette.com/news/', 'base': 'https://dublingazette.com', 'condado': 'Dublin'},
    {'nombre': 'Dublin People', 'url': 'https://dublinpeople.com/news/', 'base': 'https://dublinpeople.com', 'condado': 'Dublin'},
    {'nombre': 'Cork Beo', 'url': 'https://www.corkbeo.ie/news/', 'base': 'https://www.corkbeo.ie', 'condado': 'Cork'},
    {'nombre': 'Cork Independent', 'url': 'https://corkindependent.com/news/', 'base': 'https://corkindependent.com', 'condado': 'Cork'},
    {'nombre': 'Cork Echo', 'url': 'https://www.echolive.ie/news/', 'base': 'https://www.echolive.ie', 'condado': 'Cork'},
    {'nombre': 'Connacht Tribune', 'url': 'https://www.connachttribune.ie/news/', 'base': 'https://www.connachttribune.ie', 'condado': 'Galway'},
    {'nombre': 'Galway Advertiser', 'url': 'https://www.galwayadvertiser.ie/news/', 'base': 'https://www.galwayadvertiser.ie', 'condado': 'Galway'},
    {'nombre': 'Galway Bay FM', 'url': 'https://galwaybayfm.ie/news/', 'base': 'https://galwaybayfm.ie', 'condado': 'Galway'},
    {'nombre': 'Limerick Post', 'url': 'https://www.limerickpost.ie/news/', 'base': 'https://www.limerickpost.ie', 'condado': 'Limerick'},
    {'nombre': 'Limerick Live', 'url': 'https://www.limericklive.ie/news/', 'base': 'https://www.limericklive.ie', 'condado': 'Limerick'},
    {'nombre': 'Waterford News', 'url': 'https://www.waterford-news.ie/news/', 'base': 'https://www.waterford-news.ie', 'condado': 'Waterford'},
    {'nombre': 'Waterford Live', 'url': 'https://www.waterfordlive.ie/news/', 'base': 'https://www.waterfordlive.ie', 'condado': 'Waterford'},
    {'nombre': 'Kerryman', 'url': 'https://www.kerryman.ie/news/', 'base': 'https://www.kerryman.ie', 'condado': 'Kerry'},
    {'nombre': 'Clare Champion', 'url': 'https://www.clarechampion.ie/news/', 'base': 'https://www.clarechampion.ie', 'condado': 'Clare'},
    {'nombre': 'Clare Echo', 'url': 'https://www.clareecho.ie/news/', 'base': 'https://www.clareecho.ie', 'condado': 'Clare'},
    {'nombre': 'Donegal Daily', 'url': 'https://donegaldaily.com/news/', 'base': 'https://donegaldaily.com', 'condado': 'Donegal'},
    {'nombre': 'Donegal News', 'url': 'https://donegalnews.com/news/', 'base': 'https://donegalnews.com', 'condado': 'Donegal'},
    {'nombre': 'Mayo News', 'url': 'https://www.mayonews.ie/news/', 'base': 'https://www.mayonews.ie', 'condado': 'Mayo'},
    {'nombre': 'Mayo Advertiser', 'url': 'https://www.mayoadvertiser.ie/news/', 'base': 'https://www.mayoadvertiser.ie', 'condado': 'Mayo'},
    {'nombre': 'Kildare Now', 'url': 'https://kildarenow.com/news/', 'base': 'https://kildarenow.com', 'condado': 'Kildare'},
    {'nombre': 'Leinster Leader', 'url': 'https://www.leinsterleader.ie/news/', 'base': 'https://www.leinsterleader.ie', 'condado': 'Kildare'},
    {'nombre': 'Tipperary Live', 'url': 'https://www.tipperarylive.ie/news/', 'base': 'https://www.tipperarylive.ie', 'condado': 'Tipperary'},
    {'nombre': 'Wexford People', 'url': 'https://www.wexfordpeople.ie/news/', 'base': 'https://www.wexfordpeople.ie', 'condado': 'Wexford'},
    {'nombre': 'Westmeath Independent', 'url': 'https://www.westmeathindependent.ie/news/', 'base': 'https://www.westmeathindependent.ie', 'condado': 'Westmeath'},
    {'nombre': 'Louth Live', 'url': 'https://www.louthlive.ie/news/', 'base': 'https://www.louthlive.ie', 'condado': 'Louth'},
    {'nombre': 'Sligo Champion', 'url': 'https://www.sligochampion.ie/news/', 'base': 'https://www.sligochampion.ie', 'condado': 'Sligo'},
    {'nombre': 'Laois Today', 'url': 'https://www.laoistoday.ie/news/', 'base': 'https://www.laoistoday.ie', 'condado': 'Laois'},
    {'nombre': 'Offaly Express', 'url': 'https://www.offalyexpress.ie/news/', 'base': 'https://www.offalyexpress.ie', 'condado': 'Offaly'},
    {'nombre': 'Cavan Echo', 'url': 'https://cavanecho.ie/news/', 'base': 'https://cavanecho.ie', 'condado': 'Cavan'},
    {'nombre': 'Monaghan News', 'url': 'https://monaghannews.com/news/', 'base': 'https://monaghannews.com', 'condado': 'Monaghan'},
    {'nombre': 'Roscommon Herald', 'url': 'https://www.roscommonherald.ie/news/', 'base': 'https://www.roscommonherald.ie', 'condado': 'Roscommon'},
    {'nombre': 'Wicklow News', 'url': 'https://wicklownews.net/news/', 'base': 'https://wicklownews.net', 'condado': 'Wicklow'},
    {'nombre': 'Carlow Live', 'url': 'https://www.carlowlive.ie/news/', 'base': 'https://www.carlowlive.ie', 'condado': 'Carlow'},
    {'nombre': 'Meath Chronicle', 'url': 'https://www.meathchronicle.ie/news/', 'base': 'https://www.meathchronicle.ie', 'condado': 'Meath'},
    {'nombre': 'Longford Leader', 'url': 'https://www.longfordleader.ie/news/', 'base': 'https://www.longfordleader.ie', 'condado': 'Longford'},
    {'nombre': 'Leitrim Observer', 'url': 'https://www.leitrimobserver.ie/news/', 'base': 'https://www.leitrimobserver.ie', 'condado': 'Leitrim'},
    {'nombre': 'Belfast Live', 'url': 'https://www.belfastlive.co.uk/news/', 'base': 'https://www.belfastlive.co.uk', 'condado': 'Antrim'},
    {'nombre': 'Irish News', 'url': 'https://www.irishnews.com/news/', 'base': 'https://www.irishnews.com', 'condado': 'Antrim'},
    {'nombre': 'News Letter', 'url': 'https://www.newsletter.co.uk/news/', 'base': 'https://www.newsletter.co.uk', 'condado': 'Antrim'},
    {'nombre': 'Belfast Telegraph', 'url': 'https://www.belfasttelegraph.co.uk/news/', 'base': 'https://www.belfasttelegraph.co.uk', 'condado': 'Antrim'},
    {'nombre': 'Derry Journal', 'url': 'https://www.derryjournal.com/news/', 'base': 'https://www.derryjournal.com', 'condado': 'Derry'},
    {'nombre': 'Derry Now', 'url': 'https://www.derrynow.com/news/', 'base': 'https://www.derrynow.com', 'condado': 'Derry'},
    {'nombre': 'Armagh I', 'url': 'https://armaghi.com/news/', 'base': 'https://armaghi.com', 'condado': 'Armagh'},
    {'nombre': 'Armagh Guardian', 'url': 'https://www.armaghguardian.co.uk/news/', 'base': 'https://www.armaghguardian.co.uk', 'condado': 'Armagh'},
    {'nombre': 'Down News', 'url': 'https://www.downnews.co.uk/news/', 'base': 'https://www.downnews.co.uk', 'condado': 'Down'},
    {'nombre': 'Newry Times', 'url': 'https://www.newrytimes.com/news/', 'base': 'https://www.newrytimes.com', 'condado': 'Down'},
    {'nombre': 'Fermanagh Herald', 'url': 'https://www.fermanaghherald.com/news/', 'base': 'https://www.fermanaghherald.com', 'condado': 'Fermanagh'},
    {'nombre': 'Tyrone News', 'url': 'https://www.tyronenews.com/news/', 'base': 'https://www.tyronenews.com', 'condado': 'Tyrone'},
]

URLS_ALTERNATIVAS = ['/news', '/crime', '/latest-news', '/breaking-news', '/irish-news', '/news/crime', '/crime-news']

# ============================================================================
# GESTOR DE DATOS (CON RLock)
# ============================================================================

class GestorDatos:
    def __init__(self):
        self.archivo = ARCHIVO_DATOS
        self.datos = self.cargar()
        self.lock = RLock()
    
    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key in ['incidentes', 'ultima_actualizacion', 'estadisticas_historicas']:
                        if key not in data:
                            data[key] = [] if key == 'incidentes' else {} if key == 'estadisticas_historicas' else None
                    return data
            except Exception as e:
                logger.error(f"Error cargando {self.archivo}: {e}")
                return {'incidentes': [], 'ultima_actualizacion': None, 'estadisticas_historicas': {}}
        return {'incidentes': [], 'ultima_actualizacion': None, 'estadisticas_historicas': {}}
    
    def guardar(self):
        try:
            with self.lock:
                self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(self.datos, f, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            return False
    
    def agregar_incidentes(self, nuevos):
        if not nuevos:
            return 0
        with self.lock:
            ids_existentes = {inc['id'] for inc in self.datos['incidentes']}
            contador = 0
            for n in nuevos:
                if n['id'] not in ids_existentes:
                    coords = COORDENADAS_CONDADOS.get(n.get('condado', ''), {'lat': 53.0, 'lon': -8.0})
                    n['lat'] = coords['lat']
                    n['lon'] = coords['lon']
                    n['severidad'] = self.calcular_severidad(n.get('tipo', 'other'), n.get('titulo', ''))
                    n['color'] = TIPOS_CRIMEN.get(n.get('tipo', 'other'), {}).get('color', '#666666')
                    n['url_referencia'] = n.get('url_referencia', '')
                    self.datos['incidentes'].append(n)
                    ids_existentes.add(n['id'])
                    contador += 1
            if contador > 0:
                self.guardar()
            return contador
    
    def calcular_severidad(self, tipo, titulo):
        severidad_base = {'murder': 10, 'gang_violence': 9, 'drugs': 8, 'organized_crime': 8, 'weapon': 7, 'assault': 6, 'robbery': 5, 'garda_op': 4, 'other': 3}
        score = severidad_base.get(tipo, 3)
        if any(p in titulo.lower() for p in ['fatal', 'killed', 'murder', 'dead', 'death', 'massive', 'multiple']):
            score = min(10, score + 2)
        return score
    
    def estadisticas(self, incidentes=None):
        if incidentes is None:
            incidentes = self.datos['incidentes']
        stats = {'total': len(incidentes), 'condados': defaultdict(int), 'tipos': defaultdict(int), 
                 'fuentes': defaultdict(int), 'ultimos_7dias': 0, 'ultimos_30dias': 0, 
                 'ultimos_90dias': 0, 'tendencia': defaultdict(int)}
        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
        for inc in incidentes:
            if inc.get('condado'): stats['condados'][inc['condado']] += 1
            if inc.get('tipo'): stats['tipos'][inc['tipo']] += 1
            if inc.get('fuente'): stats['fuentes'][inc['fuente']] += 1
            fecha = inc.get('fecha', '')
            if fecha:
                if fecha >= hace_7d: stats['ultimos_7dias'] += 1
                if fecha >= hace_30d: stats['ultimos_30dias'] += 1
                if fecha >= hace_90d: stats['ultimos_90dias'] += 1
                if len(fecha) >= 7: stats['tendencia'][fecha[:7]] += 1
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
            limpios = []
            dup = 0
            for inc in self.datos['incidentes']:
                if inc['id'] not in ids_vistos:
                    ids_vistos.add(inc['id'])
                    limpios.append(inc)
                else:
                    dup += 1
            self.datos['incidentes'] = limpios
            if dup > 0:
                self.guardar()
            return dup
    
    def exportar_json(self):
        return json.dumps(self.datos, indent=2, ensure_ascii=False)
    
    def exportar_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Título', 'Fecha', 'Condado', 'Tipo', 'Fuente', 'Severidad', 'URL'])
        for inc in self.datos['incidentes']:
            writer.writerow([inc['id'], inc['titulo'].replace('\n', ' '), inc['fecha'], 
                           inc.get('condado', ''), inc.get('tipo', ''), inc['fuente'], 
                           inc.get('severidad', 0), inc.get('url_referencia', '')])
        return output.getvalue()
    
    def exportar_html(self):
        stats = self.estadisticas()
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>KELTIC KRAKEN - Ireland Crime Report</title>
<style>
body{{background:#0a0a0a;color:#e0e0e0;font-family:'Segoe UI',sans-serif;padding:20px}}
h1{{color:#ff4444;text-align:center}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:20px 0}}
.stat-card{{background:#1a1a1a;padding:15px;border-radius:8px;text-align:center;border-left:4px solid #ff4444}}
.stat-number{{font-size:2em;color:#ff4444;font-weight:bold}}
table{{width:100%;border-collapse:collapse;margin:20px 0}}
th,td{{border:1px solid #333;padding:8px;text-align:left}}
th{{background:#333;color:#ff4444}}
</style>
</head>
<body>
<h1>🦈 KELTIC KRAKEN - Ireland Crime Report</h1>
<p style="text-align:center">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<div class="stats">
<div class="stat-card"><div>Total Crimes</div><div class="stat-number">{stats['total']}</div></div>
<div class="stat-card"><div>Last 7 Days</div><div class="stat-number">{stats['ultimos_7dias']}</div></div>
<div class="stat-card"><div>Last 30 Days</div><div class="stat-number">{stats['ultimos_30dias']}</div></div>
<div class="stat-card"><div>Sources</div><div class="stat-number">{len(stats['fuentes'])}</div></div>
</div>
<h2>Top Counties</h2>
<table><tr><th>County</th><th>Crimes</th></tr>"""
        for condado, cnt in sorted(stats['condados'].items(), key=lambda x: x[1], reverse=True)[:10]:
            html += f"<tr><td>{condado}</td><td>{cnt}</td></tr>"
        html += "</table><h2>Crime Types</h2><table><tr><th>Type</th><th>Icon</th><th>Count</th></tr>"
        for tip, cnt in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
            icono = TIPOS_CRIMEN.get(tip, {}).get('icono', '❓')
            nombre = TIPOS_CRIMEN.get(tip, {}).get('nombre', tip)
            html += f"<tr><td>{nombre}</td><td>{icono}</td><td>{cnt}</td></tr>"
        html += "</table></body></html>"
        return html
    
    # ================================================================
    # NUEVA FUNCIÓN: REPARAR DATOS EXISTENTES
    # ================================================================
    def reparar_datos_existentes(self):
        """Repara los datos existentes asegurando que todos tengan coordenadas y colores"""
        with self.lock:
            incidentes = self.datos['incidentes']
            reparados = 0
            sin_coordenadas = 0
            
            for inc in incidentes:
                # 1. REPARAR COORDENADAS
                if 'lat' not in inc or 'lon' not in inc or inc.get('lat') == 0 or inc.get('lon') == 0:
                    condado = inc.get('condado', 'Dublin')
                    coords = COORDENADAS_CONDADOS.get(condado, {'lat': 53.3498, 'lon': -6.2603})
                    inc['lat'] = coords['lat']
                    inc['lon'] = coords['lon']
                    sin_coordenadas += 1
                    reparados += 1
                
                # 2. REPARAR COLOR
                tipo = inc.get('tipo', 'other')
                color_correcto = TIPOS_CRIMEN.get(tipo, {}).get('color', '#666666')
                if inc.get('color') != color_correcto:
                    inc['color'] = color_correcto
                    reparados += 1
                
                # 3. REPARAR SEVERIDAD
                if 'severidad' not in inc or inc.get('severidad') == 0:
                    inc['severidad'] = self.calcular_severidad(
                        inc.get('tipo', 'other'), 
                        inc.get('titulo', '')
                    )
                    reparados += 1
            
            if reparados > 0:
                self.guardar()
            
            return reparados, sin_coordenadas

# ============================================================================
# DETECTOR Y VERIFICADOR DE URLs
# ============================================================================

class DetectorURLs:
    def __init__(self):
        self.cache_urls = {}
        self.session = self._crear_sesion()
    
    def _crear_sesion(self):
        session = requests.Session()
        retry = Retry(total=0, read=0, connect=0)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def detectar_url(self, fuente):
        nombre = fuente['nombre']
        base = fuente['base']
        if nombre in self.cache_urls:
            return self.cache_urls[nombre]
        for alt in URLS_ALTERNATIVAS:
            url_test = base.rstrip('/') + alt
            try:
                headers = {'User-Agent': get_random_ua(), 'Connection': 'close'}
                r = self.session.get(url_test, timeout=3, headers=headers, allow_redirects=True)
                if r.status_code == 200:
                    self.cache_urls[nombre] = url_test
                    return url_test
            except:
                continue
        return fuente['url']

class VerificadorFuentes:
    def __init__(self):
        self.estado_file = ARCHIVO_ESTADO
        self.estado = self.cargar_estado()
        self.detector = DetectorURLs()
    
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
    
    def verificar_todas(self, fuentes, mostrar_progreso=True):
        if mostrar_progreso:
            cprint(f"\n{'='*80}", 'red', bold=True)
            cprint(f"🔍 Verificando fuentes...", 'red', bold=True)
            cprint(f"{'='*80}", 'red', bold=True)
        
        verificadas = []
        activas = 0
        total = len(fuentes)
        
        for i, fuente in enumerate(fuentes, 1):
            if mostrar_progreso:
                pct = (i/total)*100
                barra = '█' * int(i*40/total) + '░' * (40 - int(i*40/total))
                sys.stdout.write(f"\r   📊 Progreso: [{barra}] {i}/{total} ({pct:.1f}%)")
                sys.stdout.flush()
                cprint(f"\n📰 [{i}/{total}] {fuente['nombre']}", 'yellow', bold=True, end=' ')
            else:
                cprint(f"\n📰 {fuente['nombre']}", 'yellow', bold=True, end=' ')
            
            try:
                headers = {'User-Agent': get_random_ua(), 'Connection': 'close'}
                r = requests.get(fuente['url'], timeout=5, headers=headers, allow_redirects=True)
                if r.status_code == 200:
                    fuente['activo'] = True
                    activas += 1
                    cprint(f"✅ OK", 'green')
                    verificadas.append(fuente)
                    continue
            except:
                pass
            
            cprint(f"🔍 Buscando alternativa...", 'yellow', end=' ')
            url_alt = self.detector.detectar_url(fuente)
            if url_alt and url_alt != fuente['url']:
                try:
                    headers = {'User-Agent': get_random_ua(), 'Connection': 'close'}
                    r = requests.get(url_alt, timeout=5, headers=headers, allow_redirects=True)
                    if r.status_code == 200:
                        fuente['url'] = url_alt
                        fuente['activo'] = True
                        activas += 1
                        cprint(f"✅ OK (alternativa)", 'green')
                        verificadas.append(fuente)
                        continue
                except:
                    pass
            
            fuente['activo'] = False
            cprint(f"❌ INACTIVE", 'red')
            verificadas.append(fuente)
        
        if mostrar_progreso:
            print()
            cprint(f"\n{'='*80}", 'green', bold=True)
            cprint(f"📊 RESULTADOS: {activas} de {total} fuentes activas", 'green', bold=True)
            cprint(f"{'='*80}", 'green', bold=True)
        
        self.guardar_estado()
        return verificadas

# ============================================================================
# EXTRACTOR DE NOTICIAS
# ============================================================================

class ExtractorNoticias:
    def __init__(self, fuentes):
        self.fuentes = fuentes
        self.session = self._crear_sesion()
        self.total_incidentes = 0
        self.incidentes_por_fuente = {}
    
    def _crear_sesion(self):
        session = requests.Session()
        retry = Retry(total=1, read=1, connect=1, backoff_factor=0.3, status_forcelist=[429])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def fetch_url(self, url):
        for _ in range(MAX_INTENTOS):
            try:
                headers = {'User-Agent': get_random_ua(), 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'close'}
                response = self.session.get(url, timeout=TIMEOUT, headers=headers, allow_redirects=True)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    time.sleep(get_random_delay()*2)
                else:
                    time.sleep(get_random_delay())
            except:
                time.sleep(get_random_delay())
        return None
    
    def extraer_de_fuente(self, fuente, paginas=PAGINAS_BUSQUEDA):
        incidentes = []
        url_base = fuente['url']
        
        for pagina in range(1, paginas + 1):
            if pagina == 1:
                url = url_base
            else:
                patrones = [url_base.rstrip('/') + f'/page/{pagina}/', url_base.rstrip('/') + f'?page={pagina}', url_base.rstrip('/') + f'&page={pagina}']
                url = None
                for pat in patrones[:3]:
                    if self.fetch_url(pat):
                        url = pat
                        break
                if not url:
                    break
            
            try:
                cprint(f"   📄 Página {pagina}... ", 'gray', end='')
                response = self.fetch_url(url)
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    elementos = soup.find_all('article') + soup.find_all('div', class_=re.compile(r'article|story|post|news|entry', re.I)) + soup.find_all(['h1', 'h2', 'h3', 'h4'])
                    
                    enlaces = {a.get_text().strip()[:100]: a['href'] for a in soup.find_all('a', href=True) if len(a.get_text().strip()) > 30}
                    for k, v in enlaces.items():
                        if v.startswith('/'):
                            enlaces[k] = fuente['base'].rstrip('/') + v
                        elif not v.startswith('http'):
                            enlaces[k] = fuente['base'].rstrip('/') + '/' + v.lstrip('/')
                    
                    encontrados = 0
                    for elem in elementos[:25]:
                        texto = elem.get_text().strip()
                        if len(texto) < 40:
                            continue
                        tl = texto.lower()
                        if any(kw in tl for kw in PALABRAS_CLAVE_CRIMEN):
                            fecha = soup.find('time')
                            fecha_str = datetime.now().strftime('%Y-%m-%d')
                            if fecha and fecha.get('datetime'):
                                fecha_str = fecha.get('datetime')[:10]
                            
                            tipo = detectar_tipo_inteligente(texto)
                            condado = extraer_condado_inteligente(texto, fuente['condado'])
                            url_ref = ''
                            for key, val in enlaces.items():
                                if key in texto[:100]:
                                    url_ref = val
                                    break
                            
                            if tipo != 'other' or any(p in tl for p in ['crime', 'criminal', 'arrest', 'garda', 'police']):
                                incidentes.append({
                                    'id': hashlib.md5(texto.encode()).hexdigest()[:16],
                                    'titulo': texto[:500],
                                    'fecha': fecha_str,
                                    'condado': condado,
                                    'tipo': tipo,
                                    'fuente': fuente['nombre'],
                                    'url_referencia': url_ref
                                })
                                encontrados += 1
                    
                    cprint(f"✓ {encontrados} encontrados", 'green')
                    if encontrados == 0 and pagina > 2:
                        break
                else:
                    cprint(f"✗ Sin respuesta", 'red')
                    break
            except Exception as e:
                cprint(f"✗ Error: {str(e)[:30]}", 'red')
            time.sleep(get_random_delay() * 1.5)
        
        self.incidentes_por_fuente[fuente['nombre']] = len(incidentes)
        return incidentes
    
    def extraer_todas(self, paginas=PAGINAS_BUSQUEDA):
        cprint(f"\n{'='*80}", 'red', bold=True)
        cprint(f"🦈 KELTIC KRAKEN - Actualizando datos criminales", 'red', bold=True)
        cprint(f"{'='*80}", 'red', bold=True)
        
        todas = []
        fuentes_activas = [f for f in self.fuentes if f.get('activo', True)]
        total_act = len(fuentes_activas)
        
        if total_act == 0:
            cprint(f"\n⚠️ Sin fuentes activas", 'yellow')
            return todas
        
        for idx, fuente in enumerate(fuentes_activas, 1):
            pct = (idx/total_act)*100
            barra = '█' * int(idx*40/total_act) + '░' * (40 - int(idx*40/total_act))
            sys.stdout.write(f"\r   🔪 Analizando: [{barra}] {idx}/{total_act} ({pct:.1f}%)")
            sys.stdout.flush()
            cprint(f"\n\n📰 {fuente['nombre']}", 'yellow', bold=True)
            cprint(f"   📍 Condado: {fuente['condado']}", 'gray', dim=True)
            incidentes_f = self.extraer_de_fuente(fuente, paginas)
            todas.extend(incidentes_f)
            cprint(f"   📊 Total fuente: {len(incidentes_f)} incidentes", 'cyan')
            if idx < total_act:
                delay = random.uniform(DELAY_ENTRE_FUENTES, DELAY_ENTRE_FUENTES * 2)
                cprint(f"   ⏳ Esperando {delay:.1f}s...", 'gray', dim=True)
                time.sleep(delay)
        
        print()
        unicos = {}
        for c in todas:
            if c['id'] not in unicos:
                unicos[c['id']] = c
        resultado = list(unicos.values())
        
        cprint(f"\n{'='*80}", 'green', bold=True)
        cprint(f"🦈 Proceso finalizado: {len(resultado)} incidentes", 'green', bold=True)
        cprint(f"{'='*80}", 'green', bold=True)
        self.total_incidentes = len(resultado)
        return resultado

# ============================================================================
# SERVIDOR WEB - HTML CON POPUPS AUTOCERRANTES Y MAPA EXPANDIBLE
# ============================================================================

app = Flask(__name__)
gestor_global = None
fuentes_global = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦈 KELTIC KRAKEN v4.1 - Ireland Crime Intelligence</title>
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Poppins',sans-serif;background:#0a0a0f;color:#e8e8e8;min-height:100vh;padding:20px}
        ::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:#14141a;border-radius:10px}
        ::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#006633,#ff4444);border-radius:10px}
        .container{max-width:1600px;margin:0 auto}
        @keyframes flagWave{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        @keyframes glowPulse{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:0.8;transform:scale(1.05)}}
        .header{background:linear-gradient(135deg,#006633 0%,#006633 28%,#ffffff 28%,#ffffff 52%,#ff8833 52%,#ff8833 72%,#006633 72%,#006633 100%);background-size:300% 100%;animation:flagWave 10s ease-in-out infinite;padding:30px;border-radius:28px;text-align:center;margin-bottom:30px;border:2px solid rgba(255,68,68,0.3);box-shadow:0 0 60px rgba(255,68,68,0.15);position:relative;overflow:hidden}
        .header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at center,rgba(255,255,255,0.08) 0%,transparent 70%);animation:glowPulse 6s ease-in-out infinite}
        .header-content{position:relative;z-index:2;background:rgba(0,0,0,0.7);padding:20px 40px;border-radius:20px;backdrop-filter:blur(12px);display:inline-block;border:1px solid rgba(255,255,255,0.1)}
        .header h1{font-family:'Orbitron',monospace;font-size:3.5em;font-weight:900;letter-spacing:6px;background:linear-gradient(135deg,#ffffff,#ff8833);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 30px rgba(255,68,68,0.3))}
        .header .subtitle{color:#ffffff;font-size:1em;letter-spacing:3px;opacity:0.8;margin-top:5px;font-weight:300;text-transform:uppercase}
        .header .badge-version{display:inline-block;background:rgba(255,68,68,0.25);border:1px solid rgba(255,68,68,0.4);padding:4px 18px;border-radius:30px;font-size:0.7em;color:#ff6b6b;margin-top:8px;font-weight:600}
        .clock-container{text-align:center;margin:10px 0 20px;font-family:'Orbitron',monospace;font-size:0.9em;color:#6a6a7a;letter-spacing:2px}
        .clock-container span{color:#ff4444}
        
        .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:15px;margin-bottom:25px}
        .stat-card{background:linear-gradient(145deg,#12121a,#1a1a24);padding:18px 15px;border-radius:16px;text-align:center;border-left:4px solid #ff4444;transition:all 0.3s ease;position:relative;overflow:hidden;cursor:pointer}
        .stat-card:hover{transform:translateY(-4px) scale(1.02);box-shadow:0 10px 30px rgba(0,0,0,0.4)}
        .stat-card .stat-icon{font-size:1.4em;display:block;margin-bottom:2px}
        .stat-card .stat-number{font-size:2.2em;font-weight:800;background:linear-gradient(135deg,#ff4444,#ff8833);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2;font-family:'Orbitron',monospace}
        .stat-card .stat-label{color:#9a9aaa;font-size:0.7em;margin-top:2px;font-weight:500;text-transform:uppercase;letter-spacing:0.5px}
        
        .btn-group{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:20px}
        .btn{background:#1a1a24;color:#e8e8e8;border:2px solid #2a2a3a;padding:8px 20px;border-radius:40px;font-size:0.8em;font-weight:600;cursor:pointer;transition:all 0.25s ease;text-decoration:none;display:inline-flex;align-items:center;gap:6px;font-family:'Poppins',sans-serif}
        .btn:hover{background:#ff4444;border-color:#ff4444;color:#fff;transform:scale(1.04);box-shadow:0 0 25px rgba(255,68,68,0.2)}
        .btn-primary{background:#ff4444;border-color:#ff4444;color:#fff}
        .btn-primary:hover{background:#ff6666;border-color:#ff6666;box-shadow:0 0 30px rgba(255,68,68,0.3)}
        .btn-green{border-color:#006633;color:#4ade80}
        .btn-green:hover{background:#006633;border-color:#006633;color:#fff}
        .btn-blue{border-color:#0066cc;color:#4da6ff}
        .btn-blue:hover{background:#0066cc;border-color:#0066cc;color:#fff}
        .btn-purple{border-color:#800080;color:#cc66cc}
        .btn-purple:hover{background:#800080;border-color:#800080;color:#fff}
        .btn-orange{border-color:#ff8c00;color:#ffaa33}
        .btn-orange:hover{background:#ff8c00;border-color:#ff8c00;color:#fff}
        
        .filtros{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-bottom:20px}
        .filtro-btn{background:#14141c;color:#aaa;border:2px solid #252535;padding:6px 16px;border-radius:30px;text-decoration:none;font-size:0.8em;font-weight:500;transition:all 0.25s ease;font-family:'Poppins',sans-serif;cursor:pointer}
        .filtro-btn:hover{background:#2a2a3a;color:#fff;border-color:#ff4444}
        .filtro-btn.active{background:#ff4444;color:#fff;border-color:#ff4444;box-shadow:0 0 20px rgba(255,68,68,0.15)}
        
        .dashboard-grid{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-bottom:30px}
        .map-container{background:#0a0a0a;border-radius:18px;overflow:hidden;border:1px solid #252535;height:600px;position:relative;transition:all 0.3s ease}
        .map-container:hover{border-color:#ff4444;box-shadow:0 0 30px rgba(255,68,68,0.05)}
        .map-container.fullscreen{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;border-radius:0}
        .map-container.fullscreen .map-fullscreen-btn{position:absolute;top:20px;right:80px;z-index:100}
        #map3d{width:100%;height:100%}
        
        .map-legend{position:absolute;bottom:20px;left:20px;background:rgba(0,0,0,0.85);padding:15px 20px;border-radius:12px;border:1px solid #333;z-index:10;backdrop-filter:blur(10px);max-width:200px}
        .map-legend-item{display:flex;align-items:center;gap:10px;margin:3px 0;font-size:0.7em;color:#ccc}
        .map-legend-color{width:12px;height:12px;border-radius:50%;border:1px solid rgba(255,255,255,0.3);flex-shrink:0}
        
        .map-controls{position:absolute;top:20px;right:20px;z-index:10;display:flex;flex-direction:column;gap:8px}
        .map-control-btn{background:rgba(0,0,0,0.8);color:#fff;border:1px solid #444;border-radius:8px;padding:8px 12px;cursor:pointer;font-size:0.7em;transition:all 0.3s ease;backdrop-filter:blur(5px);font-family:'Poppins',sans-serif;min-width:60px;text-align:center}
        .map-control-btn:hover{background:#ff4444;border-color:#ff4444}
        
        .stats-col{display:flex;flex-direction:column;gap:15px}
        .charts-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;margin-bottom:25px}
        .chart-container{background:linear-gradient(145deg,#12121a,#1a1a24);border-radius:18px;padding:18px 16px 14px;border:1px solid #252535;transition:all 0.3s ease}
        .chart-container:hover{border-color:#ff4444;box-shadow:0 0 30px rgba(255,68,68,0.05)}
        .chart-title{color:#ff4444;font-size:0.95em;font-weight:700;text-align:center;margin-bottom:12px;letter-spacing:1px;text-transform:uppercase}
        .chart-container canvas{max-height:200px}
        
        .leaderboard{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-bottom:25px}
        .leader-card{background:linear-gradient(145deg,#12121a,#1a1a24);border-radius:18px;padding:18px 20px;border:1px solid #252535;transition:all 0.3s ease}
        .leader-card:hover{border-color:#ff4444}
        .leader-card h4{color:#9a9aaa;font-size:0.7em;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;font-weight:600}
        .leader-item{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1a1a24;font-size:0.85em}
        .leader-item:last-child{border-bottom:none}
        .leader-item .rank{color:#5a5a6a;font-weight:600;margin-right:10px;min-width:20px}
        .leader-item .name{color:#e8e8e8;flex:1}
        .leader-item .count{color:#ff4444;font-weight:700}
        .leader-item .rank.gold{color:#fbbf24}
        .leader-item .rank.silver{color:#9ca3af}
        .leader-item .rank.bronze{color:#d97706}
        
        .pagination{display:flex;justify-content:center;align-items:center;gap:12px;margin:15px 0 20px}
        .page-link{background:#1a1a24;color:#ff4444;padding:6px 16px;border-radius:10px;text-decoration:none;border:1px solid #2a2a3a;font-weight:600;transition:all 0.2s ease;font-size:0.85em}
        .page-link:hover{background:#ff4444;color:#fff;border-color:#ff4444;transform:scale(1.05)}
        .page-info{color:#9a9aaa;font-size:0.85em}
        
        .crime-list{background:linear-gradient(145deg,#12121a,#1a1a24);border-radius:18px;padding:18px 20px;border:1px solid #252535}
        .crime-list-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;flex-wrap:wrap;gap:10px}
        .crime-list-title{color:#ff4444;font-size:1.1em;font-weight:700;display:flex;align-items:center;gap:10px}
        .crime-list-title .badge-count{background:#2a2a3a;color:#9a9aaa;font-size:0.6em;padding:2px 12px;border-radius:30px;font-weight:400}
        
        .crime-card{background:#0d0d15;margin-bottom:10px;padding:14px 18px;border-radius:12px;border-left:4px solid #ff4444;transition:all 0.25s ease;cursor:pointer;position:relative}
        .crime-card:hover{background:#16161f;transform:translateX(6px);border-left-color:#006633;box-shadow:0 4px 20px rgba(0,0,0,0.3)}
        .crime-card .crime-title{font-weight:600;font-size:0.95em;color:#f0f0f0;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
        .crime-card .crime-title .title-text{cursor:pointer;flex:1}
        .crime-card .crime-title .title-text:hover{color:#ff4444}
        .crime-card .crime-title .url-link{color:#4da6ff;font-size:0.7em;text-decoration:none;padding:2px 8px;border-radius:12px;border:1px solid #0066cc;display:inline-flex;align-items:center;gap:4px}
        .crime-card .crime-title .url-link:hover{background:#0066cc;color:#fff}
        .crime-card .crime-meta{display:flex;flex-wrap:wrap;gap:8px;font-size:0.7em;color:#8a8a9a;align-items:center}
        .crime-card .crime-meta .badge{background:#14141c;padding:2px 10px;border-radius:20px;border:1px solid #252535}
        .crime-card .crime-meta .badge-tipo{font-weight:600;border-color:#ff4444;color:#ff4444}
        .severity-bar{height:3px;background:#1a1a24;border-radius:4px;margin-top:6px;overflow:hidden}
        .severity-fill{height:100%;border-radius:4px;transition:width 0.8s ease;background:linear-gradient(90deg,#006633,#ff4444)}
        
        .crime-popup .maplibregl-popup-content{background:rgba(10,10,10,0.95);color:#e0e0e0;padding:15px 20px;border-radius:12px;border:1px solid #ff4444;max-width:320px;backdrop-filter:blur(10px);box-shadow:0 0 30px rgba(255,0,0,0.2)}
        .crime-popup .maplibregl-popup-tip{border-top-color:rgba(10,10,10,0.95)}
        .popup-title{color:#ff4444;font-size:1em;font-weight:bold;margin-bottom:8px;cursor:pointer}
        .popup-title:hover{text-decoration:underline}
        .popup-meta{display:grid;grid-template-columns:1fr 1fr;gap:5px 15px;font-size:0.8em;color:#aaa;margin:8px 0}
        .popup-meta strong{color:#fff}
        .popup-severity{margin-top:8px;padding-top:8px;border-top:1px solid #333;font-size:0.85em}
        .popup-severity .sev-label{color:#ff6666;font-weight:bold}
        .popup-url{margin-top:8px;padding-top:8px;border-top:1px solid #333;font-size:0.7em}
        .popup-url a{color:#4da6ff;text-decoration:none}
        .popup-url a:hover{text-decoration:underline}
        
        .search-box{display:flex;gap:10px;margin-bottom:20px;justify-content:center}
        .search-box input{background:#1a1a24;border:2px solid #2a2a3a;border-radius:30px;padding:10px 20px;color:#e8e8e8;font-family:'Poppins',sans-serif;width:100%;max-width:400px;outline:none;transition:all 0.3s ease}
        .search-box input:focus{border-color:#ff4444;box-shadow:0 0 20px rgba(255,68,68,0.1)}
        .search-box input::placeholder{color:#5a5a6a}
        .search-box button{background:#ff4444;border:none;color:#fff;padding:10px 20px;border-radius:30px;cursor:pointer;font-weight:600;transition:all 0.3s ease}
        .search-box button:hover{background:#ff6666;transform:scale(1.05)}
        
        .footer{text-align:center;padding:20px;margin-top:30px;color:#5a5a6a;font-size:0.75em;border-top:1px solid #1a1a24;letter-spacing:0.5px}
        .footer a{color:#ff4444;text-decoration:none}
        .footer a:hover{text-decoration:underline}
        @keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
        .stat-card,.chart-container,.leader-card,.crime-card{animation:fadeInUp 0.5s ease forwards}
        
        @media(max-width:1200px){.dashboard-grid{grid-template-columns:1fr}.map-container{height:450px}}
        @media(max-width:768px){.header h1{font-size:2em;letter-spacing:3px}.header-content{padding:15px 20px}.stats-grid{grid-template-columns:repeat(3,1fr)}.charts-row{grid-template-columns:1fr}.map-container{height:350px}}
        @media(max-width:480px){.stats-grid{grid-template-columns:1fr 1fr}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🦈 KELTIC KRAKEN</h1>
                <div class="subtitle">Ireland Crime Intelligence · v{{ version }}</div>
                <div class="badge-version">🌍 {{ stats.total }} crímenes · {{ periodicos_activos }} fuentes</div>
            </div>
        </div>
        
        <div class="clock-container">
            <i class="fas fa-clock"></i> <span id="clock">--:--:--</span>
            <span style="margin-left:15px;">📅 <span id="date">--/--/----</span></span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card" onclick="window.location.href='/'"><span class="stat-icon">📊</span><div class="stat-number">{{ stats.total }}</div><div class="stat-label">Total Crímenes</div></div>
            <div class="stat-card" onclick="window.location.href='/page/1?filtro=7d'"><span class="stat-icon">⚡</span><div class="stat-number">{{ stats.ultimos_7dias }}</div><div class="stat-label">Últimos 7 días</div></div>
            <div class="stat-card" onclick="window.location.href='/page/1?filtro=30d'"><span class="stat-icon">🔥</span><div class="stat-number">{{ stats.ultimos_30dias }}</div><div class="stat-label">Últimos 30 días</div></div>
            <div class="stat-card"><span class="stat-icon">📰</span><div class="stat-number">{{ periodicos_activos }}</div><div class="stat-label">Fuentes Activas</div></div>
            <div class="stat-card"><span class="stat-icon">🏴</span><div class="stat-number">{{ stats.condados|length }}</div><div class="stat-label">Condados</div></div>
            <div class="stat-card"><span class="stat-icon">🔪</span><div class="stat-number">{{ stats.tipos|length }}</div><div class="stat-label">Tipos Detectados</div></div>
        </div>
        
        <div class="btn-group">
            <form action="/actualizar" method="post" style="display:inline">
                <button class="btn btn-primary"><i class="fas fa-sync-alt"></i> Actualizar</button>
            </form>
            <button class="btn btn-blue" onclick="window.location.href='/page/1?filtro=todo'"><i class="fas fa-list"></i> Todo</button>
            <button class="btn btn-orange" onclick="window.location.href='/estadisticas'"><i class="fas fa-chart-pie"></i> Estadísticas</button>
            <a href="/exportar/json" class="btn btn-green"><i class="fas fa-file-code"></i> JSON</a>
            <a href="/exportar/csv" class="btn btn-green"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/exportar/html" class="btn btn-green"><i class="fas fa-file-alt"></i> HTML</a>
            <button class="btn btn-purple" onclick="window.location.reload();"><i class="fas fa-redo-alt"></i> Recargar</button>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Buscar crímenes, condados, tipos..." onkeyup="filterCrimes()">
            <button onclick="filterCrimes()"><i class="fas fa-search"></i> Buscar</button>
        </div>
        
        <div class="filtros">
            <a href="/page/1?filtro=todo" class="filtro-btn {% if filtro == 'todo' %}active{% endif %}">📅 Todo</a>
            <a href="/page/1?filtro=7d" class="filtro-btn {% if filtro == '7d' %}active{% endif %}">⚡ 7d</a>
            <a href="/page/1?filtro=30d" class="filtro-btn {% if filtro == '30d' %}active{% endif %}">🔥 30d</a>
            <a href="/page/1?filtro=90d" class="filtro-btn {% if filtro == '90d' %}active{% endif %}">📊 90d</a>
            <a href="/page/1?filtro=alta" class="filtro-btn {% if filtro == 'alta' %}active{% endif %}">💀 Alta Severidad</a>
        </div>
        
        <div class="dashboard-grid">
            <div class="map-container" id="mapContainer">
                <div id="map3d"></div>
                <div class="map-legend">
                    <div style="color:#ff4444;font-weight:bold;font-size:0.8em;margin-bottom:6px;">🔪 TIPOS</div>
                    {% for tipo, info in tipos_crimen.items() %}
                    <div class="map-legend-item">
                        <span class="map-legend-color" style="background:{{ info.color }};"></span>
                        {{ info.icono }} {{ info.nombre }}
                    </div>
                    {% endfor %}
                </div>
                <div class="map-controls">
                    <button class="map-control-btn" onclick="resetMapView()">🔄 Reset</button>
                    <button class="map-control-btn" onclick="toggle3D()">🎯 3D</button>
                    <button class="map-control-btn" onclick="toggleGlobe()">🌍 Globo</button>
                    <button class="map-control-btn" onclick="autoRotate()">🔄 Auto</button>
                    <button class="map-control-btn map-fullscreen-btn" onclick="toggleFullscreen()">⛶ Full</button>
                </div>
            </div>
            <div class="stats-col">
                <div class="leaderboard" style="grid-template-columns:1fr;">
                    <div class="leader-card">
                        <h4><i class="fas fa-trophy" style="color:#fbbf24;"></i> Top Condados</h4>
                        {% set dept_list = stats.condados.items()|list|sort(attribute='1', reverse=true) %}
                        {% for condado, count in dept_list[:5] %}
                        <div class="leader-item">
                            <span class="rank {% if loop.index == 1 %}gold{% elif loop.index == 2 %}silver{% elif loop.index == 3 %}bronze{% endif %}">{{ loop.index }}</span>
                            <span class="name">{{ condado }}</span>
                            <span class="count">{{ count }}</span>
                        </div>
                        {% else %}
                        <div class="leader-item"><span class="name" style="color:#5a5a6a;">Sin datos</span></div>
                        {% endfor %}
                    </div>
                    <div class="leader-card">
                        <h4><i class="fas fa-skull" style="color:#ff4444;"></i> Top Tipos</h4>
                        {% set tipo_list = stats.tipos.items()|list|sort(attribute='1', reverse=true) %}
                        {% for tipo, count in tipo_list[:5] %}
                        <div class="leader-item">
                            <span class="rank {% if loop.index == 1 %}gold{% elif loop.index == 2 %}silver{% elif loop.index == 3 %}bronze{% endif %}">{{ loop.index }}</span>
                            <span class="name">{{ tipo|upper }}</span>
                            <span class="count">{{ count }}</span>
                        </div>
                        {% else %}
                        <div class="leader-item"><span class="name" style="color:#5a5a6a;">Sin datos</span></div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="charts-row">
            <div class="chart-container"><div class="chart-title">📍 CONDADOS</div><canvas id="countyChart"></canvas></div>
            <div class="chart-container"><div class="chart-title">🔪 TIPOS DE CRIMEN</div><canvas id="typeChart"></canvas></div>
            <div class="chart-container"><div class="chart-title">📈 EVOLUCIÓN MENSUAL</div><canvas id="trendChart"></canvas></div>
            <div class="chart-container"><div class="chart-title">📰 FUENTES PRINCIPALES</div><canvas id="sourcesChart"></canvas></div>
        </div>
        
        <div class="pagination">
            {% if page > 1 %}
            <a href="/page/{{ page-1 }}?filtro={{ filtro }}" class="page-link"><i class="fas fa-chevron-left"></i> Anterior</a>
            {% endif %}
            <span class="page-info">Página {{ page }} / {{ total_pages }}</span>
            {% if page < total_pages %}
            <a href="/page/{{ page+1 }}?filtro={{ filtro }}" class="page-link">Siguiente <i class="fas fa-chevron-right"></i></a>
            {% endif %}
        </div>
        
        <div class="crime-list">
            <div class="crime-list-header">
                <div class="crime-list-title">
                    <i class="fas fa-skull"></i> Últimos crímenes
                    <span class="badge-count">{{ total_incidentes }} crímenes</span>
                </div>
                <div>
                    <span style="color:#6a6a7a;font-size:0.8em;">
                        <i class="fas fa-link"></i> Click en el título 🔗 o en "Fuente" para abrir
                    </span>
                </div>
            </div>
            {% for c in crimes_paginados %}
            <div class="crime-card" data-search="{{ c.titulo }} {{ c.condado }} {{ c.tipo }} {{ c.fuente }}">
                <div class="crime-title">
                    <span class="title-text" onclick="abrirUrl('{{ c.url_referencia }}')">
                        {{ c.titulo[:170] }}{% if c.titulo|length > 170 %}...{% endif %}
                    </span>
                    {% if c.url_referencia %}
                    <a href="{{ c.url_referencia }}" target="_blank" class="url-link" onclick="event.stopPropagation();">
                        <i class="fas fa-external-link-alt"></i> Fuente
                    </a>
                    {% endif %}
                </div>
                <div class="crime-meta">
                    <span class="badge"><i class="fas fa-map-marker-alt"></i> {{ c.condado or '?' }}</span>
                    <span class="badge"><i class="fas fa-calendar-alt"></i> {{ c.fecha }}</span>
                    <span class="badge"><i class="fas fa-newspaper"></i> {{ c.fuente|truncate(20) }}</span>
                    <span class="badge badge-tipo"><i class="fas fa-tag"></i> {{ c.tipo|upper }}</span>
                    <span class="badge"><i class="fas fa-fire"></i> Severidad: {{ c.severidad }}/10</span>
                </div>
                <div class="severity-bar">
                    <div class="severity-fill" style="width: {{ c.severidad * 10 }}%;"></div>
                </div>
            </div>
            {% else %}
            <div style="text-align:center;padding:40px 0;color:#5a5a6a;">
                <i class="fas fa-search" style="font-size:2.5em;display:block;margin-bottom:12px;color:#3a3a4a;"></i>
                Sin datos. Ejecuta "Actualizar" para cargar crímenes
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p><i class="fas fa-shield-alt" style="color:#ff4444;"></i> KELTIC KRAKEN v{{ version }} · {{ periodicos_activos }} fuentes · {{ stats.total }} crímenes</p>
            <p style="margin-top:4px;font-size:0.7em;color:#3a3a4a;">
                🛡️ "Un gran poder conlleva una gran responsabilidad" · By Condor2026 · SpectrumSecurity
            </p>
        </div>
    </div>
    
    <script>
        // ============================================================
        // FUNCIÓN PARA ABRIR URL
        // ============================================================
        function abrirUrl(url) {
            if (url && url !== '') {
                window.open(url, '_blank');
            }
        }
        
        // ============================================================
        // MAPA CON POPUPS AUTOCERRANTES
        // ============================================================
        const crimeData = {{ datos_mapa|tojson }};
        let is3D = true, isGlobe = false, isAutoRotate = false;
        let map, popupActual;
        let autoRotateInterval;
        
        function initMap() {
            map = new maplibregl.Map({
                container: 'map3d',
                style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
                center: [-8.0, 53.2],
                zoom: 6.5,
                pitch: 50,
                bearing: 10,
                antialias: true,
                renderWorldCopies: true,
                projection: 'mercator'
            });
            
            map.addControl(new maplibregl.NavigationControl(), 'top-right');
            map.on('load', addCrimePoints);
        }
        
        function addCrimePoints() {
            const features = crimeData.map(c => ({
                type: 'Feature',
                geometry: { type: 'Point', coordinates: [c.lon || -8.0, c.lat || 53.0] },
                properties: {
                    titulo: c.titulo || 'Sin título',
                    condado: c.condado || 'Desconocido',
                    fecha: c.fecha || 'N/A',
                    tipo: c.tipo || 'other',
                    fuente: c.fuente || 'Desconocida',
                    color: c.color || '#666666',
                    severity: c.severidad || 3,
                    id: c.id,
                    url: c.url_referencia || ''
                }
            }));
            
            map.addSource('crimes', {
                type: 'geojson',
                data: { type: 'FeatureCollection', features: features },
                cluster: true,
                clusterMaxZoom: 14,
                clusterRadius: 50
            });
            
            map.addLayer({
                id: 'clusters',
                type: 'circle',
                source: 'crimes',
                filter: ['has', 'point_count'],
                paint: {
                    'circle-color': ['step', ['get', 'point_count'], '#ff4444', 10, '#ff6b6b', 50, '#ff8c42'],
                    'circle-radius': ['step', ['get', 'point_count'], 15, 10, 20, 50, 30],
                    'circle-opacity': 0.8,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff'
                }
            });
            
            map.addLayer({
                id: 'cluster-count',
                type: 'symbol',
                source: 'crimes',
                filter: ['has', 'point_count'],
                layout: {
                    'text-field': '{point_count_abbreviated}',
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                    'text-size': 12,
                    'text-color': '#ffffff'
                }
            });
            
            map.addLayer({
                id: 'crime-points',
                type: 'circle',
                source: 'crimes',
                filter: ['!', ['has', 'point_count']],
                paint: {
                    'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 6, 8, 10, 12, 16],
                    'circle-color': ['get', 'color'],
                    'circle-opacity': 0.85,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff',
                    'circle-blur': 0.1
                }
            });
            
            map.on('click', 'crime-points', showCrimePopup);
            map.on('mouseenter', 'crime-points', () => { map.getCanvas().style.cursor = 'pointer'; });
            map.on('mouseleave', 'crime-points', () => { map.getCanvas().style.cursor = ''; });
        }
        
        function showCrimePopup(e) {
            // CERRAR POPUP ANTERIOR
            if (popupActual) {
                popupActual.remove();
                popupActual = null;
            }
            
            const f = e.features[0];
            const p = f.properties;
            const sc = p.severity > 7 ? '#ff0000' : p.severity > 4 ? '#ff8c00' : '#00cc00';
            
            let urlHtml = '';
            if (p.url) {
                urlHtml = `<div class="popup-url">🔗 <a href="${p.url}" target="_blank">Ver fuente original</a></div>`;
            }
            
            popupActual = new maplibregl.Popup({
                offset: [0, -15],
                className: 'crime-popup',
                closeButton: true,
                closeOnClick: true
            })
            .setLngLat(f.geometry.coordinates)
            .setHTML(`
                <div class="popup-title" onclick="abrirUrl('${p.url}')">🔪 ${p.titulo.substring(0,80)}${p.titulo.length>80?'...':''}</div>
                <div class="popup-meta">
                    <span><strong>📍</strong> ${p.condado}</span>
                    <span><strong>📅</strong> ${p.fecha}</span>
                    <span><strong>🔪</strong> ${p.tipo.toUpperCase()}</span>
                    <span><strong>📰</strong> ${p.fuente}</span>
                </div>
                <div class="popup-severity">
                    <span class="sev-label">⚡ Severidad:</span>
                    <span style="color:${sc};font-weight:bold;">${p.severity}/10</span>
                    <span class="severity-bar" style="display:inline-block;width:80px;margin-left:8px;">
                        <span class="severity-fill" style="width:${p.severity*10}%;background:${sc};"></span>
                    </span>
                </div>
                ${urlHtml}
            `)
            .addTo(map);
        }
        
        function resetMapView() {
            map.flyTo({ center: [-8.0, 53.2], zoom: 6.5, pitch: is3D ? 50 : 0, bearing: is3D ? 10 : 0, duration: 1000 });
            if (popupActual) { popupActual.remove(); popupActual = null; }
        }
        
        function toggle3D() {
            is3D = !is3D;
            map.flyTo({ pitch: is3D ? 50 : 0, bearing: is3D ? 10 : 0, duration: 800 });
        }
        
        function toggleGlobe() {
            isGlobe = !isGlobe;
            map.setProjection(isGlobe ? 'globe' : 'mercator');
            map.flyTo({ center: [-8.0, 53.2], zoom: isGlobe ? 3 : 6.5, pitch: isGlobe ? 0 : 50, duration: 1500 });
        }
        
        function autoRotate() {
            isAutoRotate = !isAutoRotate;
            if (isAutoRotate) {
                let bearing = 0;
                autoRotateInterval = setInterval(() => {
                    bearing = (bearing + 0.3) % 360;
                    map.setBearing(bearing);
                }, 50);
            } else {
                clearInterval(autoRotateInterval);
            }
        }
        
        function toggleFullscreen() {
            const container = document.getElementById('mapContainer');
            container.classList.toggle('fullscreen');
            setTimeout(() => map.resize(), 300);
        }
        
        // ESC para salir de fullscreen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.getElementById('mapContainer').classList.remove('fullscreen');
                setTimeout(() => map.resize(), 300);
            }
        });
        
        document.addEventListener('DOMContentLoaded', initMap);
        
        // ============================================================
        // RELOJ
        // ============================================================
        function updateClock() {
            const n = new Date();
            document.getElementById('clock').textContent = n.toLocaleTimeString('es');
            document.getElementById('date').textContent = n.toLocaleDateString('es', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
        }
        updateClock();
        setInterval(updateClock, 1000);
        
        // ============================================================
        // BÚSQUEDA EN TIEMPO REAL
        // ============================================================
        function filterCrimes() {
            const input = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.crime-card');
            let visible = 0;
            cards.forEach(card => {
                const searchData = card.getAttribute('data-search').toLowerCase();
                if (input === '' || searchData.includes(input)) {
                    card.style.display = 'block';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            const badge = document.querySelector('.badge-count');
            if (badge) badge.textContent = visible + ' crímenes visibles';
        }
        
        // ============================================================
        // GRÁFICOS
        // ============================================================
        new Chart(document.getElementById('countyChart'), {
            type: 'bar',
            data: {
                labels: {{ condados_labels|tojson }},
                datasets: [{
                    label: 'Crímenes',
                    data: {{ condados_data|tojson }},
                    backgroundColor: 'rgba(255,68,68,0.7)',
                    borderColor: '#ff4444',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#ccc' } }, tooltip: { backgroundColor: '#111', titleColor: '#ff4444' } },
                scales: { y: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, x: { ticks: { color: '#ccc', rotation: 45 } } }
            }
        });
        
        new Chart(document.getElementById('typeChart'), {
            type: 'doughnut',
            data: {
                labels: {{ tipos_labels|tojson }},
                datasets: [{
                    data: {{ tipos_data|tojson }},
                    backgroundColor: ['#ff0000','#ff4444','#000000','#ff8c00','#ffd700','#800080','#0066cc','#990000','#666666'],
                    borderWidth: 2,
                    borderColor: '#1a1a1a'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#ccc' } }, tooltip: { backgroundColor: '#111', titleColor: '#ff4444' } }
            }
        });
        
        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels: {{ tendencia_labels|tojson }},
                datasets: [{
                    label: 'Crímenes por mes',
                    data: {{ tendencia_data|tojson }},
                    borderColor: '#ff4444',
                    backgroundColor: 'rgba(255,68,68,0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ff4444',
                    pointBorderColor: '#fff',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#ccc' } }, tooltip: { backgroundColor: '#111', titleColor: '#ff4444' } },
                scales: { y: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, x: { ticks: { color: '#ccc', rotation: 45 } } }
            }
        });
        
        new Chart(document.getElementById('sourcesChart'), {
            type: 'bar',
            data: {
                labels: {{ fuentes_labels|tojson }},
                datasets: [{
                    label: 'Artículos',
                    data: {{ fuentes_data|tojson }},
                    backgroundColor: 'rgba(255,102,102,0.7)',
                    borderColor: '#ff6666',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: { legend: { labels: { color: '#ccc' } }, tooltip: { backgroundColor: '#111', titleColor: '#ff6666' } },
                scales: { x: { ticks: { color: '#ccc' }, grid: { color: '#333' } }, y: { ticks: { color: '#ccc' } } }
            }
        });
    </script>
</body>
</html>
"""

# ============================================================================
# RUTAS DE FLASK - CORREGIDAS
# ============================================================================

@app.route('/')
def index():
    return index_paginada(1, 'todo')

@app.route('/page/<int:page>')
def index_paginada(page=1, filtro='todo'):
    global gestor_global, fuentes_global
    
    filtro = request.args.get('filtro', 'todo')
    
    incidentes = gestor_global.datos['incidentes']
    
    # APLICAR FILTROS
    if filtro == '7d':
        limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '30d':
        limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == '90d':
        limite = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= limite]
    elif filtro == 'alta':
        incidentes = [i for i in incidentes if i.get('severidad', 0) >= 7]
    
    # ============================================================
    # 🔥 CORRECCIÓN 1: Asegurar colores correctos en TODOS los incidentes
    # ============================================================
    for inc in incidentes:
        tipo = inc.get('tipo', 'other')
        inc['color'] = TIPOS_CRIMEN.get(tipo, {}).get('color', '#666666')
        # Asegurar coordenadas también
        if 'lat' not in inc or 'lon' not in inc:
            condado = inc.get('condado', 'Dublin')
            coords = COORDENADAS_CONDADOS.get(condado, {'lat': 53.3498, 'lon': -6.2603})
            inc['lat'] = coords['lat']
            inc['lon'] = coords['lon']
    
    stats = gestor_global.estadisticas(incidentes)
    periodicos_activos = len([f for f in fuentes_global if f.get('activo', True)])
    
    condados_labels = list(stats['condados'].keys())[:8]
    condados_data = list(stats['condados'].values())[:8]
    tipos_labels = [f"{TIPOS_CRIMEN.get(t, {}).get('icono', '❓')} {t.upper()}" for t in list(stats['tipos'].keys())[:6]]
    tipos_data = list(stats['tipos'].values())[:6]
    
    tendencia_items = list(stats['tendencia'].items())[-12:]
    tendencia_labels = [item[0] for item in tendencia_items]
    tendencia_data = [item[1] for item in tendencia_items]
    
    fuentes_top = dict(sorted(stats['fuentes'].items(), key=lambda x: x[1], reverse=True)[:5])
    fuentes_labels = list(fuentes_top.keys())
    fuentes_data = list(fuentes_top.values())
    
    total_incidentes = len(incidentes)
    total_pages = max(1, (total_incidentes + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA)
    page = max(1, min(page, total_pages))
    start = (page - 1) * ITEMS_POR_PAGINA
    paginated = incidentes[::-1][start:start + ITEMS_POR_PAGINA]
    
    # ============================================================
    # 🔥 CORRECCIÓN 2: AUMENTAR LÍMITE DE PUNTOS EN EL MAPA
    # ============================================================
    # Ahora mostramos hasta 3000 puntos en el mapa con colores correctos
    LIMITE_MAPA = 3000
    if len(incidentes) > LIMITE_MAPA:
        datos_mapa = incidentes[-LIMITE_MAPA:]
    else:
        datos_mapa = incidentes
    
    # Asegurar que todos los puntos del mapa tengan color y coordenadas
    for punto in datos_mapa:
        if 'color' not in punto:
            tipo = punto.get('tipo', 'other')
            punto['color'] = TIPOS_CRIMEN.get(tipo, {}).get('color', '#666666')
        if 'lat' not in punto or 'lon' not in punto:
            condado = punto.get('condado', 'Dublin')
            coords = COORDENADAS_CONDADOS.get(condado, {'lat': 53.3498, 'lon': -6.2603})
            punto['lat'] = coords['lat']
            punto['lon'] = coords['lon']
    
    return render_template_string(HTML_TEMPLATE, version=VERSION,
                                  stats=stats, periodicos_activos=periodicos_activos,
                                  filtro=filtro, page=page, total_pages=total_pages,
                                  total_incidentes=total_incidentes,
                                  condados_labels=condados_labels, condados_data=condados_data,
                                  tipos_labels=tipos_labels, tipos_data=tipos_data,
                                  tendencia_labels=tendencia_labels, tendencia_data=tendencia_data,
                                  fuentes_labels=fuentes_labels, fuentes_data=fuentes_data,
                                  crimes_paginados=paginated, datos_mapa=datos_mapa,
                                  tipos_crimen=TIPOS_CRIMEN)

@app.route('/actualizar', methods=['POST'])
def actualizar():
    global gestor_global, fuentes_global
    cprint(f"\n{'='*80}", 'red', bold=True)
    cprint(f"🦈 Actualizando datos...", 'red', bold=True)
    cprint(f"{'='*80}", 'red', bold=True)
    
    verificador = VerificadorFuentes()
    fuentes_global = verificador.verificar_todas(fuentes_global, mostrar_progreso=False)
    extractor = ExtractorNoticias(fuentes_global)
    nuevos = extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
    agregados = gestor_global.agregar_incidentes(nuevos)
    gestor_global.guardar()
    cprint(f"\n✅ {agregados} incidentes nuevos", 'green', bold=True)
    cprint(f"💾 Datos guardados en {ARCHIVO_DATOS}", 'cyan', dim=True)
    return redirect(url_for('index'))

@app.route('/estadisticas')
def estadisticas():
    stats = gestor_global.estadisticas()
    return render_template_string("""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>Estadísticas - KELTIC KRAKEN</title>
    <style>
        body{background:#0a0a0f;color:#e8e8e8;font-family:'Poppins',sans-serif;padding:20px}
        .container{max-width:1200px;margin:0 auto}
        h1{color:#ff4444;text-align:center}
        .back{color:#4da6ff;text-decoration:none;display:inline-block;margin:20px 0}
        .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:20px 0}
        .stat-box{background:#1a1a24;padding:20px;border-radius:12px;text-align:center}
        .stat-box .num{font-size:2.5em;font-weight:bold;color:#ff4444;font-family:'Orbitron',monospace}
        .stat-box .label{color:#9a9aaa;font-size:0.8em;margin-top:5px}
        table{width:100%;border-collapse:collapse;margin:20px 0}
        th,td{border:1px solid #333;padding:8px;text-align:left}
        th{background:#333;color:#ff4444}
        .bar-bg{background:#1a1a24;height:20px;border-radius:10px;overflow:hidden;margin:5px 0}
        .bar-fill{height:100%;background:linear-gradient(90deg,#006633,#ff4444);border-radius:10px}
        .total-crimes{font-size:3em;color:#ff4444;text-align:center;margin:20px 0}
    </style>
    </head>
    <body>
    <div class="container">
        <a href="/" class="back">← Volver al mapa</a>
        <h1>📊 ESTADÍSTICAS COMPLETAS</h1>
        <div class="total-crimes">🦈 {{ stats.total }} crímenes totales</div>
        <div class="stat-grid">
            <div class="stat-box"><div class="num">{{ stats.ultimos_7dias }}</div><div class="label">Últimos 7 días</div></div>
            <div class="stat-box"><div class="num">{{ stats.ultimos_30dias }}</div><div class="label">Últimos 30 días</div></div>
            <div class="stat-box"><div class="num">{{ stats.ultimos_90dias }}</div><div class="label">Últimos 90 días</div></div>
            <div class="stat-box"><div class="num">{{ stats.condados|length }}</div><div class="label">Condados afectados</div></div>
            <div class="stat-box"><div class="num">{{ stats.tipos|length }}</div><div class="label">Tipos de crimen</div></div>
            <div class="stat-box"><div class="num">{{ stats.fuentes|length }}</div><div class="label">Fuentes activas</div></div>
        </div>
        <h2>📍 Condados</h2>
        {% set max_county = stats.condados.values()|max %}
        {% for condado, count in stats.condados.items()|sort(attribute='1', reverse=true) %}
        <div>{{ condado }} ({{ count }})</div>
        <div class="bar-bg"><div class="bar-fill" style="width:{{ (count/max_county*100)|round }}%"></div></div>
        {% endfor %}
        <h2>🔪 Tipos</h2>
        {% set max_type = stats.tipos.values()|max %}
        {% for tipo, count in stats.tipos.items()|sort(attribute='1', reverse=true) %}
        <div>{{ tipo|upper }} ({{ count }})</div>
        <div class="bar-bg"><div class="bar-fill" style="width:{{ (count/max_type*100)|round }}%"></div></div>
        {% endfor %}
    </div>
    </body></html>
    """, stats=stats)

@app.route('/exportar/json')
def exportar_json():
    return Response(gestor_global.exportar_json(), mimetype='application/json',
                    headers={'Content-Disposition': 'attachment; filename=keltic_kraken.json'})

@app.route('/exportar/csv')
def exportar_csv():
    return Response(gestor_global.exportar_csv(), mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=keltic_kraken.csv'})

@app.route('/exportar/html')
def exportar_html():
    return Response(gestor_global.exportar_html(), mimetype='text/html',
                    headers={'Content-Disposition': 'attachment; filename=keltic_kraken.html'})

@app.route('/reparar')
def reparar_datos():
    """Ruta web para reparar datos"""
    global gestor_global
    reparados, sin_coords = gestor_global.reparar_datos_existentes()
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>Reparación de Datos</title>
    <style>body{{background:#0a0a0f;color:#e8e8e8;font-family:'Poppins',sans-serif;padding:40px;text-align:center}}
    h1{{color:#ff4444}}.ok{{color:#4ade80}}.info{{color:#4da6ff}}
    </style>
    </head>
    <body>
    <h1>🔧 REPARACIÓN COMPLETADA</h1>
    <p class="ok">✅ Reparados {reparados} incidentes</p>
    <p class="info">📍 {sin_coords} incidentes tenían coordenadas faltantes</p>
    <p><a href="/" style="color:#ff4444;">← Volver al mapa</a></p>
    </body></html>
    """

# ============================================================================
# MENÚ PRINCIPAL Y MAIN
# ============================================================================

def mostrar_banner_inicial():
    total_fuentes = len(FUENTES_BASE)
    print(f"""
{Color.RED}
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║   ██╗  ██╗███████╗██╗  ████████╗██╗ ██████╗     ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██║            ║
║   ██║ ██╔╝██╔════╝██║  ╚══██╔══╝██║██╔════╝     ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║            ║
║   █████╔╝ █████╗  ██║     ██║   ██║██║          █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║            ║
║   ██╔═██╗ ██╔══╝  ██║     ██║   ██║██║          ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║            ║
║   ██║  ██╗███████╗███████╗██║   ██║╚██████╗     ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║            ║ 
║   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝            ║ 
║                                                                                                               ║
║  🦈 KELTIC KRAKEN v3.4 - IRELAND CRIME INTELLIGENCE PLATFORM - ULTRA STABLE                                   ║
║  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════  ║
║  🌍 Mapa 3D con MapLibre GL · Puntos interactivos · Tooltips con severidad · 32 condados                      ║
║  ⚡ ESCANEO ESTABLE · Timeouts controlados · Sin bloqueos · URLs 2026                                          ║
║  📊 Real-time monitoring: Drug trafficking · Gang violence · Organized crime                                  ║
║  🏴 Covers ALL 32 counties including Northern Ireland                                                         ║
║  🔄 100+ Rotating User-Agents · Auto-URL discovery · Anti-blocking system                                     ║
║  📈 Interactive charts · Full statistics dashboard · Web interface                                            ║
║  🔍 Smart retry mechanism · URL cache · Session persistence                                                   ║
║  📄 Pagination in web panel · Save after each source · Duplicate removal                                      ║
║  ⚡ Parallel scanning · Dynamic workers · Non-blocking · Ultra-fast                                            ║
║  🚀 Cache memorizado · Parsing optimizado · Regex compilados                                                  ║
║                                                                                                               ║
║  🛡️ "Un gran poder conlleva una gran responsabilidad" - Spider-Man                                            ║
║                                                                                                               ║
║                                         - By Condor2026                                                       ║
║                                         •SpectrumSecurity•                                                    ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Color.RESET}""")

def mostrar_menu_principal():
    stats = gestor_global.estadisticas()
    activas = len([f for f in fuentes_global if f.get('activo', True)])
    print(f"""
{Color.RED}{'=' * 55}{Color.RESET}
{Color.BOLD}{Color.WHITE}  🦈 KELTIC KRAKEN v{VERSION}{Color.RESET}
{Color.RED}{'=' * 55}{Color.RESET}
  📊 Total crímenes: {stats['total']}
  📰 Fuentes activas: {activas} / {len(fuentes_global)}
  🏴 Condados afectados: {len(stats['condados'])}
{Color.RED}{'=' * 55}{Color.RESET}
{Color.YELLOW}{'=' * 55}{Color.RESET}
{Color.CYAN}  📋 MENÚ PRINCIPAL{Color.RESET}
{Color.YELLOW}{'=' * 55}{Color.RESET}
{Color.GREEN}  1. 🔍 Buscar crímenes en Irlanda
{Color.GREEN}  2. 📊 Análisis completo criminalidad
{Color.GREEN}  3. 🔗 Patrones y tendencias delictivas
{Color.GREEN}  4. 📈 Evolución mensual de crímenes
{Color.GREEN}  5. 🌐 Iniciar servidor web (mapa globo 3D)
{Color.GREEN}  6. 📰 Últimos 20 crímenes
{Color.GREEN}  7. 📥 Exportar datos
{Color.GREEN}  8. 🔍 Verificar fuentes
{Color.GREEN}  9. 📊 Distribución por tipo de crimen
{Color.GREEN} 10. 📈 Estadísticas avanzadas
{Color.GREEN} 11. 🧹 Limpiar duplicados
{Color.YELLOW} 12. 🔧 REPARAR DATOS (¡NUEVO!){Color.RESET}
{Color.RED} 13. 🗑️ Salir{Color.RESET}
{Color.YELLOW}{'=' * 55}{Color.RESET}
""")

def menu():
    global gestor_global, fuentes_global
    while True:
        mostrar_menu_principal()
        opc = input(f"{Color.CYAN}➤ {Color.YELLOW}Opción: {Color.RESET}")
        
        if opc == '1':
            cprint(f"\n🔍 Procesando...", 'cyan', bold=True)
            verificador = VerificadorFuentes()
            fuentes_global = verificador.verificar_todas(fuentes_global, mostrar_progreso=True)
            extractor = ExtractorNoticias(fuentes_global)
            nuevos = extractor.extraer_todas(paginas=PAGINAS_BUSQUEDA)
            agregados = gestor_global.agregar_incidentes(nuevos)
            cprint(f"\n✅ {agregados} incidentes nuevos", 'green', bold=True)
            gestor_global.guardar()
            cprint(f"💾 Datos guardados en {ARCHIVO_DATOS}", 'cyan', dim=True)
            cprint(f"\n✅ PROCESO FINALIZADO", 'green', bold=True)
            cprint(f"↩️ Volviendo al menú principal...", 'yellow')
            time.sleep(2)
        
        elif opc == '2':
            stats = gestor_global.estadisticas()
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📊 ANÁLISIS COMPLETO CRIMINALIDAD", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            cprint(f"\n📈 Total crímenes: {stats['total']}", 'white')
            cprint(f"   7d: {stats['ultimos_7dias']} | 30d: {stats['ultimos_30dias']} | 90d: {stats['ultimos_90dias']}", 'white')
            cprint(f"\n📍 TOP condados:", 'yellow')
            for condado, cnt in sorted(stats['condados'].items(), key=lambda x: x[1], reverse=True)[:10]:
                barra = '█' * min(int(cnt / max(stats['condados'].values()) * 30), 30) if stats['condados'] else ''
                cprint(f"   {condado:25} {cnt:4} {barra}", 'cyan')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '3':
            stats = gestor_global.estadisticas()
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"🔗 PATRONES DELICTIVOS", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            cprint(f"\n📰 TOP fuentes:", 'yellow')
            for f, cnt in sorted(stats['fuentes'].items(), key=lambda x: x[1], reverse=True)[:10]:
                barra = '█' * min(int(cnt / max(stats['fuentes'].values()) * 30), 30) if stats['fuentes'] else ''
                cprint(f"   {f:30} {cnt:4} {barra}", 'cyan')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '4':
            evolucion = gestor_global.evolucion_mensual()
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📈 EVOLUCIÓN DE CRÍMENES", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            if evolucion:
                max_val = max(evolucion.values())
                for mes, cnt in list(evolucion.items())[-12:]:
                    barra = '█' * int(cnt / max_val * 30) if max_val > 0 else ''
                    cprint(f"   {mes}  {cnt:4} {barra}", 'cyan')
            else:
                cprint(f"   {Color.GRAY}Sin datos suficientes{Color.RESET}")
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '5':
            cprint(f"\n🌐 Servidor web: http://localhost:{PUERTO}", 'green', bold=True)
            cprint(f"   🗺️ Mapa globo 3D con {len(gestor_global.datos['incidentes'])} puntos", 'cyan')
            cprint(f"   🔗 Click en títulos abre la fuente original", 'cyan')
            cprint(f"   ⛶ Botón FULL para pantalla completa", 'cyan')
            cprint(f"   🎯 Popups autocerrantes al hacer click en otro punto", 'cyan')
            cprint(f"   📊 Gráficos interactivos con Chart.js", 'cyan')
            cprint(f"   📄 Paginación: {ITEMS_POR_PAGINA} por página", 'cyan')
            cprint(f"   {Color.GRAY}Ctrl+C para volver al menú{Color.RESET}")
            app.run(host='127.0.0.1', port=PUERTO, debug=False, use_reloader=False)
        
        elif opc == '6':
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📰 ÚLTIMOS 20 CRÍMENES", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            crimes = gestor_global.datos['incidentes'][-20:][::-1]
            if crimes:
                for i, c in enumerate(crimes, 1):
                    tipo_nombre = TIPOS_CRIMEN.get(c.get('tipo', 'other'), {}).get('nombre', c.get('tipo', 'other'))
                    icono = TIPOS_CRIMEN.get(c.get('tipo', 'other'), {}).get('icono', '❓')
                    url_info = f" 🔗 {c.get('url_referencia', 'Sin enlace')[:50]}" if c.get('url_referencia') else ''
                    cprint(f"\n{i:2d}. {icono} {c['titulo'][:100]}...", 'white')
                    cprint(f"      📅 {c['fecha']} | 📍 {c.get('condado','?')} | 📰 {c['fuente']} | 💀 Severidad: {c.get('severidad',0)}/10{url_info}", 'gray')
            else:
                cprint(f"   {Color.GRAY}Sin datos suficientes{Color.RESET}")
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '7':
            cprint(f"\n📥 EXPORTANDO DATOS", 'cyan', bold=True)
            cprint(f"\n{Color.YELLOW}Formatos: 1=JSON 2=CSV 3=HTML{Color.RESET}")
            fmt = input(f"{Color.CYAN}➤ Elige: {Color.RESET}")
            if fmt == '1':
                with open('keltic_export.json', 'w', encoding='utf-8') as f:
                    f.write(gestor_global.exportar_json())
                cprint(f"✅ Exportado a keltic_export.json", 'green')
            elif fmt == '2':
                with open('keltic_export.csv', 'w', encoding='utf-8') as f:
                    f.write(gestor_global.exportar_csv())
                cprint(f"✅ Exportado a keltic_export.csv", 'green')
            elif fmt == '3':
                with open('keltic_export.html', 'w', encoding='utf-8') as f:
                    f.write(gestor_global.exportar_html())
                cprint(f"✅ Exportado a keltic_export.html", 'green')
            else:
                cprint(f"❌ Opción no válida", 'red')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '8':
            cprint(f"\n🔍 VERIFICANDO FUENTES", 'cyan', bold=True)
            verificador = VerificadorFuentes()
            fuentes_global = verificador.verificar_todas(fuentes_global)
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '9':
            stats = gestor_global.estadisticas()
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📊 DISTRIBUCIÓN POR TIPO DE CRIMEN", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            if stats['tipos']:
                for tip, cnt in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                    icono = TIPOS_CRIMEN.get(tip, {}).get('icono', '❓')
                    nombre = TIPOS_CRIMEN.get(tip, {}).get('nombre', tip)
                    barra = '█' * min(int(cnt / max(stats['tipos'].values()) * 30), 30) if stats['tipos'] else ''
                    cprint(f"   {icono} {nombre:20} {cnt:4} {barra}", 'cyan')
            else:
                cprint(f"   {Color.GRAY}Sin datos suficientes{Color.RESET}")
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '10':
            stats = gestor_global.estadisticas()
            cprint(f"\n{'='*70}", 'red', bold=True)
            cprint(f"📈 ESTADÍSTICAS AVANZADAS", 'red', bold=True)
            cprint(f"{'='*70}", 'red', bold=True)
            cprint(f"\n📊 Total crímenes: {stats['total']}", 'white')
            cprint(f"   Últimos 7 días: {stats['ultimos_7dias']}", 'white')
            cprint(f"   Últimos 30 días: {stats['ultimos_30dias']}", 'white')
            cprint(f"   Últimos 90 días: {stats['ultimos_90dias']}", 'white')
            cprint(f"\n🔪 Tipos detectados: {len(stats['tipos'])}", 'yellow')
            cprint(f"📍 Condados afectados: {len(stats['condados'])}", 'yellow')
            cprint(f"📰 Fuentes activas: {len(stats['fuentes'])}", 'yellow')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '11':
            cprint(f"\n🧹 LIMPIANDO BASE", 'cyan', bold=True)
            duplicados = gestor_global.limpiar_duplicados()
            cprint(f"✅ Eliminados {duplicados} duplicados", 'green')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '12':
            cprint(f"\n🔧 REPARANDO DATOS EXISTENTES...", 'yellow', bold=True)
            reparados, sin_coords = gestor_global.reparar_datos_existentes()
            cprint(f"\n✅ Reparados {reparados} incidentes", 'green', bold=True)
            if sin_coords > 0:
                cprint(f"   📍 {sin_coords} incidentes tenían coordenadas faltantes", 'cyan')
            cprint(f"📊 Total en base: {len(gestor_global.datos['incidentes'])}", 'white')
            cprint(f"🔄 Reinicia el servidor web para ver los cambios en el mapa", 'yellow')
            input(f"\n{Color.GRAY}Enter para continuar...{Color.RESET}")
        
        elif opc == '13':
            cprint(f"\n👋 ¡Hasta pronto!", 'red', bold=True)
            break
        
        else:
            cprint(f"\n❌ Opción no válida", 'red')
            time.sleep(1)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print(f"{Color.GREEN}🌍 Idioma: Español{Color.RESET}")
    
    mostrar_banner_inicial()
    
    gestor_global = GestorDatos()
    fuentes_global = FUENTES_BASE.copy()
    
    stats = gestor_global.estadisticas()
    cprint(f"\n{Color.GREEN}📊 Base de datos: {stats['total']} incidentes almacenados{Color.RESET}")
    cprint(f"{Color.YELLOW}⏳ Última actualización: {gestor_global.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")
    cprint(f"{Color.CYAN}📰 Fuentes configuradas: {len(fuentes_global)} periódicos irlandeses{Color.RESET}")
    cprint(f"{Color.MAGENTA}🌍 Mapa globo 3D interactivo con {stats['total']} puntos{Color.RESET}")
    cprint(f"{Color.GREEN}🔗 Enlaces funcionales - Click en título abre fuente{Color.RESET}")
    cprint(f"{Color.BLUE}⛶ Botón FULL para pantalla completa{Color.RESET}")
    cprint(f"{Color.YELLOW}🎯 Popups autocerrantes al hacer click en otro punto{Color.RESET}")
    
    # Reparar datos automáticamente al inicio
    if stats['total'] > 0:
        cprint(f"\n{Color.YELLOW}🔧 Verificando integridad de datos...{Color.RESET}")
        reparados, sin_coords = gestor_global.reparar_datos_existentes()
        if reparados > 0:
            cprint(f"{Color.GREEN}✅ Reparados {reparados} incidentes automáticamente{Color.RESET}")
            if sin_coords > 0:
                cprint(f"{Color.CYAN}   📍 {sin_coords} con coordenadas faltantes fueron asignadas{Color.RESET}")
    
    print(f"\n{Color.CYAN}┌{'─' * 50}┐{Color.RESET}")
    print(f"{Color.CYAN}│{Color.WHITE}  ¿Cómo deseas ejecutar?{' ' * 27}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}├{'─' * 50}┤{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [1] Modo Terminal (recomendado){' ' * 17}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}│{Color.GREEN}  [2] Modo Web (mapa globo 3D interactivo){' ' * 10}{Color.CYAN}│{Color.RESET}")
    print(f"{Color.CYAN}└{'─' * 50}┘{Color.RESET}")
    
    modo = input(f"\n{Color.CYAN}➤ {Color.YELLOW}Elige: {Color.RESET}")
    
    if modo == '2':
        cprint(f"\n🌐 Servidor web: http://localhost:{PUERTO}", 'green', bold=True)
        cprint(f"   🌍 Mapa globo 3D con {len(gestor_global.datos['incidentes'])} puntos", 'cyan')
        cprint(f"   🔗 Click en títulos abre la fuente original", 'cyan')
        cprint(f"   ⛶ Botón FULL para pantalla completa", 'cyan')
        cprint(f"   🎯 Popups autocerrantes al hacer click en otro punto", 'cyan')
        cprint(f"   📊 Gráficos interactivos con Chart.js", 'cyan')
        cprint(f"   {Color.GRAY}Presiona Ctrl+C para volver al menú{Color.RESET}")
        app.run(host='127.0.0.1', port=PUERTO, debug=False, use_reloader=False)
    else:
        menu()
