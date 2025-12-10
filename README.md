# Programmate Interrogazioni

Una web app semplice per programmare le interrogazioni nelle tue lezioni.

## Caratteristiche

- **Gestione materie**: Inserisci la materia per cui vuoi programmare le interrogazioni
- **Frequenza lezioni**: Specifica quante volte alla settimana hai quella lezione
- **Numero studenti**: Definisci quanti alunni vuoi interrogare per lezione
- **Salvataggio automatico**: I programmi vengono salvati automaticamente nel browser
- **Interfaccia intuitiva**: Design moderno e facile da usare

## Come Utilizzare

### Metodo 1: Aprire direttamente il file HTML

1. Clona o scarica questo repository
2. Apri il file `index.html` con il tuo browser preferito (Chrome, Firefox, Safari, Edge)
3. Inizia a creare i tuoi programmi di interrogazione!

### Metodo 2: Utilizzare un server locale (opzionale)

Se preferisci utilizzare un server locale:

```bash
# Con Python 3
python -m http.server 8000

# Con Python 2
python -m SimpleHTTPServer 8000

# Con Node.js (se hai http-server installato)
npx http-server -p 8000
```

Poi apri il browser all'indirizzo `http://localhost:8000`

## Utilizzo dell'App

1. **Inserisci la materia**: Scrivi il nome della materia (es. Matematica, Italiano, Storia)
2. **Specifica la frequenza**: Indica quante volte alla settimana hai questa lezione (1-7)
3. **Numero di alunni**: Definisci quanti studenti vuoi interrogare per lezione
4. **Salva**: Clicca su "Salva Programma" per salvare la configurazione

I tuoi programmi verranno salvati automaticamente e saranno visibili nella sezione "Programmi Salvati" in fondo alla pagina.

## Requisiti

- Un browser web moderno (Chrome, Firefox, Safari, Edge)
- Nessuna installazione necessaria!
- Nessuna connessione internet richiesta (funziona completamente offline)

## Tecnologie Utilizzate

- HTML5
- CSS3
- JavaScript (Vanilla)
- LocalStorage per il salvataggio dei dati

## Licenza

Vedi il file LICENSE per i dettagli.