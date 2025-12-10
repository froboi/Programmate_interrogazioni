# 🚀 Quick Start Guide

Guida rapida per avviare l'applicazione in 5 minuti!

## ⚡ Avvio Rapido

### Windows (PowerShell)

```powershell
# 1. Clona/scarica il progetto
cd Programmate_interrogazioni

# 2. Esegui lo script di avvio
.\start.ps1

# 3. Apri il browser su http://localhost:5000
```

### Linux/Mac

```bash
# 1. Clona/scarica il progetto
cd Programmate_interrogazioni

# 2. Rendi eseguibile lo script
chmod +x start.sh

# 3. Esegui lo script di avvio
./start.sh

# 4. Apri il browser su http://localhost:5000
```

## 📝 Primo Utilizzo (3 Step)

### Step 1: Configura Materia
1. Apri `http://localhost:5000`
2. Inserisci nome materia (es: "Matematica")
3. Specifica numero lezioni settimanali (es: 3)
4. Per ogni lezione, indica quanti studenti interrogare

### Step 2: Carica Studenti
1. Clicca "Procedi al Caricamento Studenti"
2. Carica un file CSV o JSON con la lista studenti
3. Usa i file di esempio in `examples/` se non hai un file pronto

### Step 3: Genera Calendario
1. Clicca "Genera Calendario"
2. Visualizza il calendario creato automaticamente
3. Salva, esporta o modifica come preferisci!

## 🔧 Prerequisiti Minimi

Prima di iniziare, assicurati di avere:

✅ **Python 3.8+** installato
```bash
python --version
# Output: Python 3.8.x o superiore
```

✅ **MySQL 8.0+** installato e avviato
```bash
# Windows
net start MySQL80

# Linux
sudo service mysql start
```

✅ **Git** (opzionale, per clonare)
```bash
git --version
```

## 🗄️ Setup Database Veloce

### Opzione 1: Setup Automatico (Consigliato)

Lo script di avvio configura automaticamente tutto!

### Opzione 2: Setup Manuale

```bash
# 1. Accedi a MySQL
mysql -u root -p

# 2. Esegui lo script di creazione
SOURCE database/schema.sql;

# 3. Verifica
SHOW DATABASES;
USE interrogazioni_db;
SHOW TABLES;
```

## ⚙️ Configurazione Base

Il file `.env` viene creato automaticamente, ma puoi personalizzarlo:

```env
# Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tua_password
MYSQL_DATABASE=interrogazioni_db

# Server
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

## 📱 Accesso da Smartphone/Tablet

1. Trova il tuo IP locale:
   ```powershell
   # Windows
   ipconfig
   
   # Linux/Mac
   hostname -I
   ```

2. Sul dispositivo mobile, apri:
   ```
   http://TUO_IP:5000
   ```
   Esempio: `http://192.168.1.100:5000`

3. Aggiungi alla home screen per accesso rapido!

## 🧪 Test Rapido

Verifica che tutto funzioni:

```bash
# Installa requests se non presente
pip install requests

# Esegui i test
python test_app.py
```

## 📦 Esempi Inclusi

Nella cartella `examples/` trovi:

- `studenti_esempio.csv` - 25 studenti in formato CSV
- `studenti_esempio.json` - 25 studenti in formato JSON

Usali per testare rapidamente l'applicazione!

## 🆘 Problemi Comuni

### "Python non trovato"
**Soluzione**: Installa Python da https://www.python.org/downloads/

### "MySQL connection refused"
**Soluzione**: 
```bash
# Windows
net start MySQL80

# Linux
sudo service mysql start
```

### "Port 5000 already in use"
**Soluzione**: Cambia porta nel `.env`:
```env
PORT=5001
```

### "mysqlclient installation failed"
**Windows**: Scarica il wheel precompilato da:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

**Linux**:
```bash
sudo apt install libmysqlclient-dev python3-dev
```

## 💡 Tips & Tricks

### Tip 1: Usa lo Script di Avvio
Lo script `start.ps1` (Windows) o `start.sh` (Linux) fa tutto automaticamente!

### Tip 2: File di Esempio
Non hai una lista studenti? Usa `examples/studenti_esempio.csv`!

### Tip 3: Consigli AI
Clicca "Ottieni Consigli AI" per suggerimenti intelligenti!

### Tip 4: Backup Facile
Usa l'export CSV/JSON per salvare i calendari!

### Tip 5: Rimescola
Non ti piace la distribuzione? Clicca "Rimescola" per rigenerare!

## 🎯 Workflow Consigliato

```
1. Configura Materia → 2. Carica Studenti → 3. Genera Calendario
                                                      ↓
                                                4. Visualizza
                                                      ↓
                                    ← 5. Modifica (se necessario)
                                                      ↓
                                        6. Salva/Esporta
```

## 📚 Prossimi Passi

Dopo il quick start, consulta:

- **README.md** - Documentazione completa
- **API_DOCUMENTATION.md** - Guida API REST
- **DEPLOY.md** - Deploy avanzato e produzione

## 🎉 Buon Lavoro!

Sei pronto! In caso di problemi:
1. Controlla la sezione Troubleshooting nel README.md
2. Verifica i prerequisiti
3. Esegui `python test_app.py` per diagnostica

**Domande?** Apri un'issue su GitHub o consulta la documentazione.

---

**Versione**: 1.0.0  
**Ultimo aggiornamento**: 10 Dicembre 2025
