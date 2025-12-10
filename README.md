# 📚 Sistema di Gestione Interrogazioni Programmate

Web Application Flask per la gestione automatizzata delle interrogazioni scolastiche con supporto AI per ottimizzazione e consigli.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Caratteristiche Principali

- ✅ **Gestione Completa Studenti**: Import da CSV/JSON, CRUD operations
- 🎲 **Generazione Casuale Calendario**: Estrazione automatica senza ripetizioni
- 🤖 **AI Advisor**: Consigli intelligenti per ottimizzare le interrogazioni
- 💾 **Dual Database**: Supporto MySQL e TinyDB (locale)
- 📊 **Dashboard Interattiva**: Interfaccia web moderna con Bootstrap 5
- 🔄 **Modifiche Dinamiche**: Cambia studenti, aggiungi/rimuovi giorni
- 📥 **Export Dati**: Esportazione in CSV o JSON
- 🌐 **Accessibile in LAN**: Host su rete locale per accesso condiviso

## 📋 Requisiti di Sistema

### Software Necessario

- **Python**: 3.8 o superiore
- **MySQL**: 8.0 o superiore (o MariaDB 10.5+)
- **Browser**: Chrome, Firefox, Edge (versioni recenti)

### Python Packages

Tutti i pacchetti sono listati in `requirements.txt`:

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
mysqlclient==2.2.0
tinydb==4.8.0
python-dotenv==1.0.0
Werkzeug==3.0.1
```

## 🚀 Installazione

### Windows

#### 1. Clona o scarica il repository

```powershell
git clone https://github.com/tuo-username/Programmate_interrogazioni.git
cd Programmate_interrogazioni
```

#### 2. Crea un ambiente virtuale Python

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Nota**: Se ricevi errori di esecuzione script, esegui:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Installa le dipendenze

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota per mysqlclient su Windows**: Se l'installazione di `mysqlclient` fallisce, scarica il wheel precompilato:
- Vai su https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
- Scarica il file corrispondente (es: `mysqlclient‑2.2.0‑cp311‑cp311‑win_amd64.whl`)
- Installa con: `pip install mysqlclient‑2.2.0‑cp311‑cp311‑win_amd64.whl`

#### 4. Configura MySQL

**Avvia MySQL** (se non è già avviato):
```powershell
# Se installato come servizio Windows
net start MySQL80
```

**Crea il database**:
```powershell
mysql -u root -p
```

Poi esegui lo script SQL:
```sql
SOURCE database/schema.sql;
```

Oppure esegui direttamente:
```powershell
mysql -u root -p < database/schema.sql
```

#### 5. Configura le variabili d'ambiente

Copia il file `.env.example` e rinominalo in `.env`:
```powershell
Copy-Item .env.example .env
```

Modifica `.env` con i tuoi dati:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tua-password-mysql
MYSQL_DATABASE=interrogazioni_db
SECRET_KEY=genera-una-chiave-segreta-casuale
```

#### 6. Avvia l'applicazione

```powershell
python app.py
```

L'applicazione sarà disponibile su:
- **Locale**: http://localhost:5000
- **LAN**: http://TUO_IP:5000 (es: http://192.168.1.100:5000)

Per trovare il tuo IP:
```powershell
ipconfig
# Cerca "Indirizzo IPv4" nella sezione della tua scheda di rete
```

### Linux/Ubuntu

#### 1. Clona il repository

```bash
git clone https://github.com/tuo-username/Programmate_interrogazioni.git
cd Programmate_interrogazioni
```

#### 2. Installa dipendenze di sistema

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server libmysqlclient-dev
```

#### 3. Crea ambiente virtuale

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Installa pacchetti Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configura MySQL

```bash
sudo mysql_secure_installation
sudo mysql -u root -p < database/schema.sql
```

#### 6. Configura variabili d'ambiente

```bash
cp .env.example .env
nano .env  # Modifica con i tuoi dati
```

#### 7. Avvia l'applicazione

```bash
python3 app.py
```

Per eseguire in background:
```bash
nohup python3 app.py > app.log 2>&1 &
```

## 📖 Guida all'Uso

### 1️⃣ Configurazione Iniziale

1. Apri il browser e vai su `http://localhost:5000`
2. Inserisci:
   - **Materia**: Nome della materia (es: "Matematica")
   - **Giorni a Settimana**: Quanti giorni a settimana hai lezione (es: 2)
   - **Distribuzione**: Per ogni giorno, quanti studenti interrogare (es: 3, 3)
3. Il sistema calcolerà automaticamente tutte le lezioni necessarie per interrogare tutti gli studenti
4. **Esempio**: 23 studenti, 2 giorni/settimana, 3 studenti/giorno = 8 lezioni totali in 4 settimane

### 2️⃣ Caricamento Studenti

1. Clicca su "Upload Studenti" nella navbar
2. Carica un file CSV o JSON con la lista studenti
3. Formato richiesto:
   - **CSV**: `registro_num,nome,cognome`
   - **JSON**: `[{"registro_num": 1, "nome": "Mario", "cognome": "Rossi"}]`
4. Vedi esempi nella cartella `examples/`

### 3️⃣ Generazione Calendario

1. Dopo aver caricato gli studenti, clicca "Genera Calendario"
2. Il sistema:
   - Calcola automaticamente quante lezioni servono per interrogare tutti gli studenti
   - Estrae casualmente gli studenti senza ripetizioni
   - Distribuisce gli studenti secondo i giorni settimanali configurati
   - Ripete il ciclo settimanale finché tutti gli studenti non sono stati interrogati
3. Visualizza il calendario completo generato

### 4️⃣ Modifiche e Ottimizzazione

- **Rimescola**: Rigenera il calendario mantenendo la distribuzione
- **Modifica Lezione**: Cambia il numero di studenti in una lezione
- **Cambia Studente**: Sostituisci uno studente specifico
- **Consigli AI**: Ottieni suggerimenti per migliorare il calendario

### 5️⃣ Salvataggio ed Esportazione

- **Salva MySQL**: Salva permanentemente nel database
- **Salva TinyDB**: Salva in file JSON locale
- **Esporta CSV/JSON**: Scarica il calendario per uso offline

## 🔌 API REST - Documentazione

### Studenti

#### GET `/api/students`
Recupera tutti gli studenti.

**Response**:
```json
{
  "success": true,
  "students": [...],
  "count": 25
}
```

#### POST `/api/add-student`
Aggiunge un nuovo studente.

**Request Body**:
```json
{
  "registro_num": 26,
  "nome": "Paolo",
  "cognome": "Verdi"
}
```

#### DELETE `/api/remove-student/<registro_num>`
Elimina uno studente per numero di registro.

#### POST `/api/upload-students`
Upload file CSV o JSON con lista studenti.

**Form Data**:
- `file`: File CSV o JSON

### Calendario

#### POST `/api/create-calendar`
Crea un nuovo calendario.

**Request Body**:
```json
{
  "materia": "Matematica",
  "num_lezioni": 3,
  "distribuzione": [2, 3, 2]
}
```

#### GET `/api/get-calendar/<materia>`
Recupera il calendario per una materia.

#### POST `/api/shuffle-assignments`
Rimescola le assegnazioni.

**Request Body**:
```json
{
  "materia": "Matematica"
}
```

#### PUT `/api/modify-day`
Modifica il numero di studenti in una lezione.

**Request Body**:
```json
{
  "materia": "Matematica",
  "lezione_num": 2,
  "new_count": 4
}
```

#### PUT `/api/change-student-in-day`
Cambia uno studente specifico.

**Request Body**:
```json
{
  "materia": "Matematica",
  "lezione_num": 2,
  "old_student_id": 5,
  "new_registro_num": 10
}
```

### Salvataggio

#### POST `/api/save-to-db`
Salva su MySQL.

#### POST `/api/save-to-tinydb`
Salva su TinyDB.

#### POST `/api/export`
Esporta calendario.

**Request Body**:
```json
{
  "materia": "Matematica",
  "format": "csv"
}
```

### AI Advisor

#### POST `/api/ai-advice`
Ottiene consigli AI.

**Request Body**:
```json
{
  "materia": "Matematica",
  "advice_type": "general"
}
```

**Tipi di consiglio**: `general`, `distribution`, `quality`, `study_time`

## 🏗️ Struttura Progetto

```
Programmate_interrogazioni/
├── app.py                      # Applicazione Flask principale
├── requirements.txt            # Dipendenze Python
├── .env.example               # Template variabili d'ambiente
├── .gitignore                 # File da ignorare in Git
│
├── app/
│   └── models.py              # Modelli database SQLAlchemy
│
├── config/
│   └── config.py              # Configurazioni applicazione
│
├── database/
│   ├── schema.sql             # Script creazione database MySQL
│   └── local_db.json          # Database TinyDB (generato)
│
├── utils/
│   ├── database_manager.py    # Gestione TinyDB
│   └── ai_advisor.py          # Modulo AI per consigli
│
├── templates/
│   ├── base.html              # Template base
│   ├── index.html             # Homepage configurazione
│   ├── upload.html            # Pagina upload studenti
│   └── calendar.html          # Pagina calendario
│
├── static/
│   ├── css/
│   │   └── style.css          # Stili personalizzati
│   └── js/
│       └── script.js          # JavaScript frontend
│
├── examples/
│   ├── studenti_esempio.csv   # Esempio file CSV
│   └── studenti_esempio.json  # Esempio file JSON
│
├── exports/                    # Esportazioni (generato)
└── uploads/                    # Upload temporanei (generato)
```

## 🔧 Troubleshooting

### Problema: Errore connessione MySQL

**Soluzione**:
1. Verifica che MySQL sia avviato: `net start MySQL80` (Windows) o `sudo service mysql start` (Linux)
2. Controlla credenziali nel file `.env`
3. Verifica che il database esista: `SHOW DATABASES;` in MySQL

### Problema: Port 5000 già in uso

**Soluzione**:
Modifica la porta nel file `.env`:
```env
PORT=5001
```

### Problema: Impossibile installare mysqlclient

**Soluzione Windows**:
- Installa Visual C++ Build Tools
- Oppure usa il wheel precompilato (vedi sezione installazione)

**Soluzione Linux**:
```bash
sudo apt install libmysqlclient-dev python3-dev
```

### Problema: L'app non è accessibile da altri dispositivi in LAN

**Soluzione**:
1. Verifica che `HOST=0.0.0.0` nel file `.env`
2. Disabilita temporaneamente il firewall o aggiungi un'eccezione per la porta 5000
3. Usa l'IP corretto (non localhost)

## 🎨 Personalizzazione

### Cambiare i colori del tema

Modifica le variabili CSS in `static/css/style.css`:

```css
:root {
    --primary-color: #0d6efd;  /* Cambia con il tuo colore */
    --success-color: #198754;
    /* ... */
}
```

### Aggiungere nuovi consigli AI

Modifica `utils/ai_advisor.py` e aggiungi nuove funzioni nella classe `AIAdvisor`.

### Personalizzare l'algoritmo di estrazione

Modifica la funzione `create_random_calendar()` in `app.py`.

## 📊 Backup e Manutenzione

### Backup Database MySQL

```bash
mysqldump -u root -p interrogazioni_db > backup.sql
```

### Restore Database

```bash
mysql -u root -p interrogazioni_db < backup.sql
```

### Backup TinyDB

Copia semplicemente il file:
```bash
cp database/local_db.json database/local_db_backup.json
```

## 🤝 Contribuire

Contributi sono benvenuti! Per favore:

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 👨‍💻 Autore

Sviluppato con ❤️ per facilitare la gestione delle interrogazioni scolastiche.

## 🆘 Supporto

Per problemi o domande:
- Apri un'issue su GitHub
- Consulta la documentazione API
- Controlla la sezione Troubleshooting

## 🔮 Roadmap Futura

- [ ] Autenticazione multi-utente
- [ ] Calendario con date reali
- [ ] Notifiche email agli studenti
- [ ] Statistiche avanzate
- [ ] App mobile companion
- [ ] Integrazione con registro elettronico
- [ ] Export PDF stampabile
- [ ] Tema scuro/chiaro

---

**Buon insegnamento! 📚✨**
