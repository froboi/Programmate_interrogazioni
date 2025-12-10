# Script PowerShell per avviare l'applicazione su Windows
# Interrogazioni Programmate - Avvio Automatico

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema Interrogazioni Programmate   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Controlla se Python è installato
Write-Host "[1/5] Controllo Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✓ Python trovato: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python non trovato! Installa Python 3.8+" -ForegroundColor Red
    Write-Host "Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Premi Enter per uscire"
    exit 1
}

# Salta ambiente virtuale per semplicità
Write-Host "[2/5] Controllo ambiente..." -ForegroundColor Yellow
Write-Host "✓ Ambiente pronto" -ForegroundColor Green

# Controlla se le dipendenze sono installate
Write-Host "[3/5] Controllo dipendenze..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "Installazione/aggiornamento dipendenze..." -ForegroundColor Cyan
    pip install -r requirements.txt --quiet
    Write-Host "✓ Dipendenze installate" -ForegroundColor Green
} else {
    Write-Host "✗ File requirements.txt non trovato!" -ForegroundColor Red
    Read-Host "Premi Enter per uscire"
    exit 1
}

# Controlla file .env
Write-Host "[4/5] Controllo configurazione..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ File .env trovato" -ForegroundColor Green
} else {
    Write-Host "! File .env non trovato, copio da .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ File .env creato" -ForegroundColor Green
        Write-Host "⚠ ATTENZIONE: Configura il file .env con i tuoi dati MySQL!" -ForegroundColor Yellow
        Write-Host "Premi Enter quando hai configurato .env..." -ForegroundColor Cyan
        Read-Host
    } else {
        Write-Host "✗ File .env.example non trovato!" -ForegroundColor Red
        Read-Host "Premi Enter per uscire"
        exit 1
    }
}

# Avvia l'applicazione
Write-Host "[5/5] Avvio applicazione..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Applicazione in esecuzione!          " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Accedi all'applicazione:" -ForegroundColor Cyan
Write-Host "  Locale:  http://localhost:5000" -ForegroundColor White
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike '*Loopback*' } | Select-Object -First 1 -ExpandProperty IPAddress)
Write-Host "  LAN:     http://${ipAddress}:5000" -ForegroundColor White
Write-Host ""
Write-Host "Premi CTRL+C per fermare il server" -ForegroundColor Yellow
Write-Host ""

# Avvia Flask
python app.py

# Cleanup
Write-Host ""
Write-Host "Applicazione terminata." -ForegroundColor Yellow
Read-Host "Premi Enter per chiudere"
