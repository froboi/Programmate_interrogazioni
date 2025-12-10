# Changelog

Tutte le modifiche notevoli a questo progetto verranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2025-12-10

### Aggiunto
- Sistema completo di gestione interrogazioni programmate
- Backend Flask con architettura REST API
- Frontend responsive con Bootstrap 5
- Supporto dual database (MySQL + TinyDB)
- Modulo AI Advisor per consigli intelligenti
- Import studenti da CSV e JSON
- Estrazione casuale senza ripetizioni
- Modifiche dinamiche calendario (rimescola, cambia studenti, modifica giorni)
- Export calendario in CSV e JSON
- Dashboard con statistiche e metriche
- Valutazione qualità calendario con scoring
- Documentazione completa API
- Script di avvio automatico per Windows e Linux
- File di esempio (CSV e JSON)
- Sistema di logging
- Gestione errori robusta
- Interfaccia utente intuitiva
- Supporto accessibilità rete LAN
- Configurazione tramite variabili d'ambiente
- Models SQLAlchemy per ORM
- CRUD operations complete
- Modali interattive per modifiche
- Alert e notifiche dinamiche
- Progress indicators
- Tooltips e popover informativi
- Responsive design per mobile
- Print-friendly styles

### Funzionalità AI
- Analisi distribuzione studenti
- Suggerimenti ottimizzazione calendario
- Valutazione qualità con scoring 0-100
- Consigli sui tempi di studio
- Rilevamento duplicazioni
- Bilanciamento automatico
- Best practices per interrogazioni

### Sicurezza
- Protezione XSS
- Validazione input lato server
- Sanitizzazione dati
- Gestione errori sicura
- Secret key configurabile

### Performance
- Query ottimizzate
- Indici database
- Lazy loading
- AJAX per operazioni asincrone
- Debounce/throttle per eventi frequenti

### Documentazione
- README.md completo
- API_DOCUMENTATION.md dettagliata
- DEPLOY.md con guida deploy
- Commenti inline in tutto il codice
- Esempi pratici
- Troubleshooting guide

## [Unreleased]

### Da Fare
- Autenticazione utenti multipli
- Gestione calendario con date reali
- Notifiche email automatiche
- Statistiche avanzate e grafici
- Export PDF stampabile
- Integrazione registro elettronico
- App mobile companion
- Tema scuro/chiaro
- Multi-lingua (i18n)
- Unit tests completi
- CI/CD pipeline
- Docker compose production-ready
- Backup automatico schedulato
- Gestione classi multiple
- Storia modifiche calendario
- Undo/Redo operations
- Drag & drop per riordinare
- Filtri e ricerca avanzata
- Dashboard analytics
- Report generazione automatica

---

## Legenda Tipi di Modifiche

- **Aggiunto**: nuove funzionalità
- **Modificato**: cambiamenti a funzionalità esistenti
- **Deprecato**: funzionalità che saranno rimosse
- **Rimosso**: funzionalità rimosse
- **Corretto**: bug fix
- **Sicurezza**: vulnerabilità corrette
