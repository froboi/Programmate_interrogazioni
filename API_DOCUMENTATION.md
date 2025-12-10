# API REST - Documentazione Completa

## Base URL
```
http://localhost:5000/api
```

## Autenticazione
Nessuna autenticazione richiesta (applicazione per uso locale/LAN).

---

## 📚 ENDPOINTS STUDENTI

### GET /api/students
Recupera la lista completa di tutti gli studenti.

**Request:**
```http
GET /api/students
```

**Response Success (200):**
```json
{
  "success": true,
  "students": [
    {
      "id": 1,
      "registro_num": 1,
      "nome": "Mario",
      "cognome": "Rossi",
      "created_at": "2025-12-10T10:30:00"
    }
  ],
  "count": 1
}
```

**Response Error (500):**
```json
{
  "success": false,
  "error": "Messaggio di errore"
}
```

---

### POST /api/add-student
Aggiunge un nuovo studente al database.

**Request:**
```http
POST /api/add-student
Content-Type: application/json

{
  "registro_num": 26,
  "nome": "Paolo",
  "cognome": "Verdi"
}
```

**Response Success (201):**
```json
{
  "success": true,
  "message": "Studente aggiunto con successo",
  "student": {
    "id": 26,
    "registro_num": 26,
    "nome": "Paolo",
    "cognome": "Verdi",
    "created_at": "2025-12-10T10:30:00"
  }
}
```

**Response Error (400):**
```json
{
  "success": false,
  "error": "Dati mancanti"
}
```

**Response Error (409):**
```json
{
  "success": false,
  "error": "Studente già esistente"
}
```

---

### DELETE /api/remove-student/{registro_num}
Elimina uno studente specifico tramite numero di registro.

**Request:**
```http
DELETE /api/remove-student/26
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Studente rimosso con successo"
}
```

**Response Error (404):**
```json
{
  "success": false,
  "error": "Studente non trovato"
}
```

---

### POST /api/upload-students
Upload di un file CSV o JSON contenente una lista di studenti.

**Request:**
```http
POST /api/upload-students
Content-Type: multipart/form-data

file: studenti.csv (o studenti.json)
```

**Formato CSV:**
```csv
registro_num,nome,cognome
1,Mario,Rossi
2,Luca,Bianchi
```

**Formato JSON:**
```json
[
  {"registro_num": 1, "nome": "Mario", "cognome": "Rossi"},
  {"registro_num": 2, "nome": "Luca", "cognome": "Bianchi"}
]
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Import completato: 25 studenti importati, 0 saltati",
  "imported": 25,
  "skipped": 0,
  "errors": []
}
```

---

## 📅 ENDPOINTS CALENDARIO

### POST /api/create-calendar
Crea un nuovo calendario di interrogazioni per una materia.

**Request:**
```http
POST /api/create-calendar
Content-Type: application/json

{
  "materia": "Matematica",
  "num_lezioni": 3,
  "distribuzione": [2, 3, 2]
}
```

**Parametri:**
- `materia` (string): Nome della materia
- `num_lezioni` (int): Numero di lezioni settimanali
- `distribuzione` (array): Array di interi che specifica quanti studenti per lezione

**Response Success (200):**
```json
{
  "success": true,
  "message": "Calendario creato con successo",
  "calendario": {
    "1": [
      {
        "id": 1,
        "student": {
          "registro_num": 5,
          "nome": "Mario",
          "cognome": "Rossi"
        }
      }
    ]
  },
  "ai_analysis": {
    "statistics": {...},
    "suggestions": [...],
    "warnings": [...]
  },
  "quality_score": {
    "score": 95,
    "quality": "Eccellente",
    "issues": [],
    "good_points": [...]
  }
}
```

---

### GET /api/get-calendar/{materia}
Recupera il calendario esistente per una materia specifica.

**Request:**
```http
GET /api/get-calendar/Matematica
```

**Response Success (200):**
```json
{
  "success": true,
  "calendario": {
    "1": [...],
    "2": [...],
    "3": [...]
  },
  "total_interrogations": 7
}
```

---

### POST /api/shuffle-assignments
Rimescola le assegnazioni degli studenti mantenendo la distribuzione.

**Request:**
```http
POST /api/shuffle-assignments
Content-Type: application/json

{
  "materia": "Matematica"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Calendario rimescolato con successo",
  "calendario": {...},
  "ai_analysis": {...},
  "quality_score": {...}
}
```

---

### PUT /api/modify-day
Modifica il numero di studenti interrogati in una lezione specifica.

**Request:**
```http
PUT /api/modify-day
Content-Type: application/json

{
  "materia": "Matematica",
  "lezione_num": 2,
  "new_count": 4
}
```

**Parametri:**
- `materia` (string): Nome della materia
- `lezione_num` (int): Numero della lezione da modificare
- `new_count` (int): Nuovo numero di studenti

**Response Success (200):**
```json
{
  "success": true,
  "message": "Lezione 2 aggiornata con successo"
}
```

---

### PUT /api/change-student-in-day
Sostituisce uno studente specifico in una lezione.

**Request:**
```http
PUT /api/change-student-in-day
Content-Type: application/json

{
  "materia": "Matematica",
  "lezione_num": 2,
  "old_student_id": 5,
  "new_registro_num": 10
}
```

**Parametri:**
- `materia` (string): Nome della materia
- `lezione_num` (int): Numero della lezione
- `old_student_id` (int): ID dello studente da sostituire
- `new_registro_num` (int): Numero di registro del nuovo studente

**Response Success (200):**
```json
{
  "success": true,
  "message": "Studente sostituito con successo",
  "interrogation": {...}
}
```

---

## 💾 ENDPOINTS SALVATAGGIO

### POST /api/save-to-db
Forza il salvataggio di tutti i dati su MySQL.

**Request:**
```http
POST /api/save-to-db
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Dati salvati su MySQL"
}
```

---

### POST /api/save-to-tinydb
Salva tutti i dati su TinyDB (database locale JSON).

**Request:**
```http
POST /api/save-to-tinydb
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Dati salvati su TinyDB"
}
```

---

### POST /api/export
Esporta il calendario in formato CSV o JSON.

**Request:**
```http
POST /api/export
Content-Type: application/json

{
  "materia": "Matematica",
  "format": "csv"
}
```

**Parametri:**
- `materia` (string): Nome della materia da esportare
- `format` (string): "csv" o "json"

**Response Success (200):**
Restituisce il file per il download.

**Formato CSV esportato:**
```csv
Materia,Lezione,Ordine,Registro,Nome,Cognome,Data
Matematica,1,1,5,Mario,Rossi,
Matematica,1,2,8,Anna,Verdi,
```

**Formato JSON esportato:**
```json
{
  "materia": "Matematica",
  "exported_at": "2025-12-10T10:30:00",
  "interrogations": [...]
}
```

---

## 🤖 ENDPOINTS AI ADVISOR

### POST /api/ai-advice
Ottiene consigli e analisi AI sul calendario.

**Request:**
```http
POST /api/ai-advice
Content-Type: application/json

{
  "materia": "Matematica",
  "advice_type": "general"
}
```

**Parametri:**
- `materia` (string): Nome della materia
- `advice_type` (string): Tipo di consiglio
  - `"general"`: Consigli generali
  - `"distribution"`: Analisi distribuzione
  - `"quality"`: Valutazione qualità
  - `"study_time"`: Consigli sui tempi di studio

**Response Success (200) - general:**
```json
{
  "success": true,
  "advice": {
    "advice": [
      {
        "category": "Equità",
        "tip": "Assicurati che ogni studente sia interrogato con la stessa frequenza",
        "importance": "alta"
      }
    ],
    "priority_tips": [...]
  }
}
```

**Response Success (200) - distribution:**
```json
{
  "success": true,
  "advice": {
    "statistics": {
      "total_interrogations": 7,
      "lessons": 3,
      "avg_per_lesson": 2.3,
      "max_per_lesson": 3,
      "min_per_lesson": 2
    },
    "suggestions": [
      {
        "type": "balanced",
        "message": "Buona distribuzione!"
      }
    ],
    "warnings": []
  }
}
```

**Response Success (200) - quality:**
```json
{
  "success": true,
  "advice": {
    "score": 95,
    "quality": "Eccellente",
    "issues": [],
    "good_points": [
      "Nessuna duplicazione di studenti",
      "Buon bilanciamento del carico"
    ],
    "recommendations": [
      "Il calendario è ottimale! Puoi procedere con il salvataggio"
    ]
  }
}
```

---

## ❌ CODICI DI STATO HTTP

- `200 OK`: Richiesta completata con successo
- `201 Created`: Risorsa creata con successo
- `400 Bad Request`: Dati della richiesta non validi
- `404 Not Found`: Risorsa non trovata
- `409 Conflict`: Conflitto (es: studente già esistente)
- `500 Internal Server Error`: Errore del server

---

## 📝 NOTE IMPORTANTI

1. **Formato Date**: Tutte le date sono in formato ISO 8601 (es: `2025-12-10T10:30:00`)

2. **Content-Type**: Per richieste POST/PUT con body JSON, usa sempre:
   ```
   Content-Type: application/json
   ```

3. **File Upload**: Per upload file, usa:
   ```
   Content-Type: multipart/form-data
   ```

4. **Errori**: Tutte le risposte di errore seguono il formato:
   ```json
   {
     "success": false,
     "error": "Descrizione dell'errore"
   }
   ```

5. **Estrazione Casuale**: L'algoritmo garantisce che ogni studente appaia una sola volta nel calendario.

---

## 🔧 ESEMPI DI USO CON cURL

**Aggiungere uno studente:**
```bash
curl -X POST http://localhost:5000/api/add-student \
  -H "Content-Type: application/json" \
  -d '{"registro_num": 26, "nome": "Paolo", "cognome": "Verdi"}'
```

**Creare un calendario:**
```bash
curl -X POST http://localhost:5000/api/create-calendar \
  -H "Content-Type: application/json" \
  -d '{"materia": "Matematica", "num_lezioni": 3, "distribuzione": [2,3,2]}'
```

**Ottenere consigli AI:**
```bash
curl -X POST http://localhost:5000/api/ai-advice \
  -H "Content-Type: application/json" \
  -d '{"materia": "Matematica", "advice_type": "quality"}'
```

---

## 🧪 ESEMPI CON JavaScript (Fetch API)

**Caricare studenti:**
```javascript
fetch('http://localhost:5000/api/add-student', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    registro_num: 26,
    nome: 'Paolo',
    cognome: 'Verdi'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Recuperare calendario:**
```javascript
fetch('http://localhost:5000/api/get-calendar/Matematica')
  .then(response => response.json())
  .then(data => console.log(data.calendario));
```

---

Per ulteriori informazioni o supporto, consulta il README.md del progetto.
