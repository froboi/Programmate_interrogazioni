# Guida Deploy e Configurazione Avanzata

## 📦 Deploy su Server Locale/LAN

### Opzione 1: Esecuzione Diretta (Sviluppo)

L'applicazione include Flask built-in server, ideale per sviluppo e uso locale.

**Windows:**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Opzione 2: Deploy con Gunicorn (Produzione)

Per un ambiente più robusto, usa Gunicorn (solo Linux/Mac):

**1. Installa Gunicorn:**
```bash
pip install gunicorn
```

**2. Crea un file `wsgi.py`:**
```python
from app import app

if __name__ == "__main__":
    app.run()
```

**3. Avvia con Gunicorn:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

**4. Usa systemd per avvio automatico:**

Crea `/etc/systemd/system/interrogazioni.service`:
```ini
[Unit]
Description=Sistema Interrogazioni Programmate
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Programmate_interrogazioni
Environment="PATH=/path/to/Programmate_interrogazioni/venv/bin"
ExecStart=/path/to/Programmate_interrogazioni/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app

[Install]
WantedBy=multi-user.target
```

Abilita e avvia:
```bash
sudo systemctl enable interrogazioni
sudo systemctl start interrogazioni
```

### Opzione 3: Deploy con Waitress (Windows)

Waitress è un server WSGI puro Python, ideale per Windows:

**1. Installa Waitress:**
```powershell
pip install waitress
```

**2. Crea `serve.py`:**
```python
from waitress import serve
from app import app

if __name__ == '__main__':
    print("Server in esecuzione su http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000, threads=4)
```

**3. Avvia:**
```powershell
python serve.py
```

## 🌐 Configurazione Rete LAN

### Trovare il tuo IP locale

**Windows:**
```powershell
ipconfig
# Cerca "Indirizzo IPv4" nella sezione Ethernet o Wi-Fi
```

**Linux/Mac:**
```bash
hostname -I
# oppure
ip addr show
```

### Aprire la porta nel Firewall

**Windows Firewall:**
```powershell
# PowerShell come Amministratore
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

**Linux (ufw):**
```bash
sudo ufw allow 5000/tcp
sudo ufw reload
```

**Linux (iptables):**
```bash
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables-save
```

### Testare l'accesso LAN

Da un altro dispositivo sulla stessa rete:
```
http://192.168.1.XXX:5000
```

Sostituisci `XXX` con il tuo IP.

## 🗄️ Configurazione MySQL Avanzata

### Ottimizzazione MySQL per l'applicazione

Aggiungi al file `my.cnf` o `my.ini`:

```ini
[mysqld]
# Ottimizzazioni per applicazioni piccole/medie
max_connections = 50
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
query_cache_size = 16M
query_cache_type = 1

# Character set UTF-8
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

### Creare un utente MySQL dedicato

```sql
-- Connettiti come root
mysql -u root -p

-- Crea utente
CREATE USER 'interrogazioni_user'@'localhost' IDENTIFIED BY 'password_sicura';

-- Concedi permessi
GRANT ALL PRIVILEGES ON interrogazioni_db.* TO 'interrogazioni_user'@'localhost';

-- Applica modifiche
FLUSH PRIVILEGES;
```

Aggiorna `.env`:
```env
MYSQL_USER=interrogazioni_user
MYSQL_PASSWORD=password_sicura
```

### Backup Automatico MySQL

**Script Windows (backup.ps1):**
```powershell
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "backups\backup_$date.sql"
mysqldump -u root -p interrogazioni_db > $backupPath
Write-Host "Backup creato: $backupPath"
```

**Script Linux (backup.sh):**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR
mysqldump -u root -p interrogazioni_db > "$BACKUP_DIR/backup_$DATE.sql"
echo "Backup creato: $BACKUP_DIR/backup_$DATE.sql"
```

**Cron job per backup automatico (Linux):**
```bash
# Apri crontab
crontab -e

# Aggiungi (backup ogni giorno alle 2:00 AM)
0 2 * * * /path/to/backup.sh
```

## 🔒 Sicurezza

### Generare una SECRET_KEY sicura

**Python:**
```python
import secrets
print(secrets.token_hex(32))
```

**PowerShell:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
```

### HTTPS con certificato autofirmato (opzionale)

**Generare certificato:**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

**Modificare app.py:**
```python
if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        ssl_context=('cert.pem', 'key.pem')  # Aggiungi questa riga
    )
```

## 🐳 Deploy con Docker (Opzionale)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia applicazione
COPY . .

# Esponi porta
EXPOSE 5000

# Comando avvio
CMD ["python", "app.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=root
      - MYSQL_PASSWORD=rootpassword
      - MYSQL_DATABASE=interrogazioni_db
    depends_on:
      - db
    volumes:
      - ./database:/app/database
      - ./exports:/app/exports

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: interrogazioni_db
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  mysql_data:
```

**Avvio con Docker:**
```bash
docker-compose up -d
```

## 📊 Monitoraggio e Logs

### Logging avanzato

Aggiungi a `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configura logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Applicazione avviata')
```

### Monitorare risorse

**Linux:**
```bash
# CPU e memoria
top -p $(pgrep -f "python app.py")

# Connessioni attive
netstat -an | grep :5000
```

**Windows:**
```powershell
# Task Manager o
Get-Process python | Select-Object CPU,WorkingSet
```

## 🔄 Aggiornamenti

### Procedura di aggiornamento

1. **Backup database:**
   ```bash
   mysqldump -u root -p interrogazioni_db > backup_before_update.sql
   ```

2. **Backup file applicazione:**
   ```bash
   cp -r Programmate_interrogazioni Programmate_interrogazioni_backup
   ```

3. **Pull nuove modifiche:**
   ```bash
   git pull origin main
   ```

4. **Aggiorna dipendenze:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

5. **Migra database (se necessario):**
   ```bash
   # Esegui script di migrazione se presenti
   ```

6. **Riavvia applicazione**

## 🚀 Ottimizzazioni Prestazioni

### Database

- Usa indici su colonne frequentemente cercate
- Esegui `OPTIMIZE TABLE` periodicamente
- Monitora slow query log

### Applicazione

- Abilita caching per query frequenti
- Comprimi risposte HTTP (gzip)
- Minimizza file CSS/JS

### Esempio con caching:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/students')
@cache.cached(timeout=60)  # Cache per 60 secondi
def get_students():
    # ...
```

## 📱 Accesso da Mobile

Per accesso facile da smartphone:

1. Crea un QR code con l'URL:
   ```
   http://TUO_IP:5000
   ```

2. Aggiungi alla home screen del dispositivo

3. Considera PWA per app-like experience

## 🆘 Troubleshooting Deploy

### Porta già in uso
```bash
# Linux
sudo lsof -i :5000
sudo kill -9 PID

# Windows
netstat -ano | findstr :5000
taskkill /PID PID /F
```

### Permessi file (Linux)
```bash
sudo chown -R www-data:www-data /path/to/app
sudo chmod -R 755 /path/to/app
```

### Database connection refused
- Verifica che MySQL sia avviato
- Controlla firewall
- Verifica credenziali in `.env`

---

Per ulteriore supporto, consulta il README.md principale o apri un'issue su GitHub.
