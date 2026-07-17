# ============================================
# 🦈 KELTIC KRAKEN v4.1 - INSTALLER (Linux/Mac)
# ============================================

set -e

# Colores
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[1;33m'
BLUE='\033[0;94m'
CYAN='\033[0;96m'
NC='\033[0m'

clear

echo -e "${RED}"
echo "╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗"
echo "║   ██╗  ██╗███████╗██╗  ████████╗██╗ ██████╗     ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██║            ║"
echo "║   ██║ ██╔╝██╔════╝██║  ╚══██╔══╝██║██╔════╝     ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║            ║"
echo "║   █████╔╝ █████╗  ██║     ██║   ██║██║          █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║            ║"
echo "║   ██╔═██╗ ██╔══╝  ██║     ██║   ██║██║          ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║            ║"
echo "║   ██║  ██╗███████╗███████╗██║   ██║╚██████╗     ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║            ║"
echo "║   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝            ║"
echo "║                                                                                                               ║"
echo "║  🦈 KELTIC KRAKEN v3.4 - IRELAND CRIME INTELLIGENCE PLATFORM - ULTRA STABLE                                   ║"
echo "║  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════  ║"
echo "║  🌍 Mapa 3D con MapLibre GL · Puntos interactivos · Tooltips con severidad · 32 condados                      ║"
echo "║  ⚡ ESCANEO ESTABLE · Timeouts controlados · Sin bloqueos · URLs 2026                                          ║"
echo "║  📊 Real-time monitoring: Drug trafficking · Gang violence · Organized crime                                  ║"
echo "║  🏴 Covers ALL 32 counties including Northern Ireland                                                         ║"
echo "║  🔄 100+ Rotating User-Agents · Auto-URL discovery · Anti-blocking system                                     ║"
echo "║  📈 Interactive charts · Full statistics dashboard · Web interface                                            ║"
echo "║  🔍 Smart retry mechanism · URL cache · Session persistence                                                   ║"
echo "║  📄 Pagination in web panel · Save after each source · Duplicate removal                                      ║"
echo "║  ⚡ Parallel scanning · Dynamic workers · Non-blocking · Ultra-fast                                            ║"
echo "║  🚀 Cache memorizado · Parsing optimizado · Regex compilados                                                  ║"
echo "║                                                                                                               ║"
echo "║  🛡️ \"Un gran poder conlleva una gran responsabilidad\" - Spider-Man                                          ║"
echo "║                                                                                                               ║"
echo "║                                         - By Condor2026                                                       ║"
echo "║                                         •SpectrumSecurity•                                                    ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
echo -e "\n${BLUE}[1/5] Verificando Python...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} encontrado${NC}"
    if [[ $(echo "$PYTHON_VERSION < 3.8" | bc) -eq 1 ]]; then
        echo -e "${RED}❌ Python 3.8+ requerido${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Python 3 no encontrado${NC}"
    exit 1
fi

# Check PIP
echo -e "\n${BLUE}[2/5] Verificando PIP...${NC}"
if ! command -v pip3 &>/dev/null; then
    echo -e "${YELLOW}⚠️ Instalando PIP...${NC}"
    python3 -m ensurepip --upgrade
fi
echo -e "${GREEN}✅ PIP listo${NC}"

# Create virtual environment
echo -e "\n${BLUE}[3/5] Entorno virtual...${NC}"
read -p "¿Crear entorno virtual? (y/n): " CREATE_VENV

if [[ "$CREATE_VENV" =~ ^[Yy]$ ]]; then
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✅ Entorno virtual creado y activado${NC}"
else
    echo -e "${YELLOW}⚠️ Continuando sin entorno virtual${NC}"
fi

# Install dependencies
echo -e "\n${BLUE}[4/5] Instalando dependencias...${NC}"
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install requests beautifulsoup4 flask flask-cors
fi
echo -e "${GREEN}✅ Dependencias instaladas${NC}"

# Setup files
echo -e "\n${BLUE}[5/5] Configurando archivos...${NC}"
mkdir -p data logs
[ ! -f ".env" ] && [ -f "env.example" ] && cp env.example .env
chmod +x keltic_kraken.py 2>/dev/null || true
echo -e "${GREEN}✅ Estructura creada${NC}"

# Verify
echo -e "\n${BLUE}Verificando...${NC}"
python3 -c "import requests, bs4, flask" 2>/dev/null && echo -e "${GREEN}✅ Todo correcto${NC}" || echo -e "${YELLOW}⚠️ Revisa dependencias${NC}"

# Final message
echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   ✅ INSTALACIÓN COMPLETADA CON ÉXITO!                        ║"
echo "║                                                               ║"
echo "║   Para ejecutar:                                              ║"
echo "║                                                               ║"
echo "║   python3 keltic_kraken.py                                    ║"
echo "║                                                               ║"
echo "║   🌐 Web: http://localhost:5025                               ║"
echo "║                                                               ║"
echo "║   🦈 KELTIC KRAKEN v4.1 READY                                 ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

read -p "¿Ejecutar ahora? (y/n): " RUN_NOW
if [[ "$RUN_NOW" =~ ^[Yy]$ ]]; then
    echo -e "\n${GREEN}🦈 Iniciando...${NC}\n"
    python3 keltic_kraken.py
fi
