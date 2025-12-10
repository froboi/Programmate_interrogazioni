# Programmate Interrogazioni

Una semplice applicazione web per programmare le interrogazioni in classe.

## Funzionalità

L'applicazione ti permette di:
- Inserire la materia da programmare
- Specificare quante volte alla settimana c'è quella lezione
- Definire quanti alunni interrogare per lezione

## Come usare l'applicazione

### Metodo 1: Aprire direttamente il file HTML
1. Naviga nella cartella del progetto
2. Apri il file `index.html` con il tuo browser preferito (Chrome, Firefox, Safari, Edge, etc.)

### Metodo 2: Usare un server locale (raccomandato)

#### Con Python (se installato):
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Poi apri il browser all'indirizzo: `http://localhost:8000`

#### Con Node.js (se installato):
```bash
# Installa http-server globalmente (solo la prima volta)
npm install -g http-server

# Avvia il server
http-server -p 8000
```

Poi apri il browser all'indirizzo: `http://localhost:8000`

#### Con PHP (se installato):
```bash
php -S localhost:8000
```

Poi apri il browser all'indirizzo: `http://localhost:8000`

## Struttura del progetto

```
Programmate_interrogazioni/
├── index.html      # Pagina principale dell'applicazione
├── styles.css      # Stili CSS
├── script.js       # Logica JavaScript
└── README.md       # Questo file
```

## Requisiti

- Un browser web moderno (Chrome, Firefox, Safari, Edge)
- Nessuna dipendenza esterna richiesta

## Sviluppo futuro

Questa è la versione iniziale dell'applicazione. Le prossime funzionalità potrebbero includere:
- Gestione dell'elenco degli studenti
- Calendario delle interrogazioni
- Salvataggio dei dati
- E altro ancora...