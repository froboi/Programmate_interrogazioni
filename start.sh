#!/bin/bash

# Script Bash per avviare l'applicazione su Linux/Mac
# Interrogazioni Programmate - Avvio Automatico

echo "========================================"
echo "  Sistema Interrogazioni Programmate   "
echo "========================================"
echo ""

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Controlla Python
echo -e "${YELLOW}[1/5] Controllo Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python trovato: $PYTHON_VERSION${NC}"
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✓ Python trovato: $PYTHON_VERSION${NC}"
    PYTHON_CMD=python
else
    echo -e "${RED}✗ Python non trovato! Installa Python 3.8+${NC}"
    exit 1
fi

# Controlla virtual environment
echo -e "${YELLOW}[2/5] Controllo ambiente virtuale...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Ambiente virtuale trovato${NC}"
    echo -e "${CYAN}Attivazione ambiente virtuale...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}! Ambiente virtuale non trovato, lo creo ora...${NC}"
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓ Ambiente virtuale creato e attivato${NC}"
fi

# Installa dipendenze
echo -e "${YELLOW}[3/5] Controllo dipendenze...${NC}"
if [ -f "requirements.txt" ]; then
    echo -e "${CYAN}Installazione/aggiornamento dipendenze...${NC}"
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Dipendenze installate${NC}"
else
    echo -e "${RED}✗ File requirements.txt non trovato!${NC}"
    exit 1
fi

# Controlla .env
echo -e "${YELLOW}[4/5] Controllo configurazione...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ File .env trovato${NC}"
else
    echo -e "${YELLOW}! File .env non trovato, copio da .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ File .env creato${NC}"
        echo -e "${YELLOW}⚠ ATTENZIONE: Configura il file .env con i tuoi dati MySQL!${NC}"
        echo -e "${CYAN}Premi Enter quando hai configurato .env...${NC}"
        read
    else
        echo -e "${RED}✗ File .env.example non trovato!${NC}"
        exit 1
    fi
fi

# Avvia applicazione
echo -e "${YELLOW}[5/5] Avvio applicazione...${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Applicazione in esecuzione!          ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}Accedi all'applicazione:${NC}"
echo -e "  Locale:  http://localhost:5000"

# Trova IP locale
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    echo -e "  LAN:     http://$LOCAL_IP:5000"
fi

echo ""
echo -e "${YELLOW}Premi CTRL+C per fermare il server${NC}"
echo ""

# Avvia Flask
$PYTHON_CMD app.py

# Cleanup
echo ""
echo -e "${YELLOW}Applicazione terminata.${NC}"
