"""
Script di test per verificare il funzionamento delle funzionalità principali
Esegui con: python test_app.py
"""

import requests
import json
import sys

# Configurazione
BASE_URL = "http://localhost:5000/api"
TEST_MATERIA = "Test_Matematica"

# Colori per output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, message=""):
    """Stampa il risultato di un test"""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if message:
        print(f"   {message}")

def test_connection():
    """Test 1: Verifica connessione al server"""
    try:
        response = requests.get(f"{BASE_URL}/students", timeout=5)
        passed = response.status_code == 200
        print_test("Connessione al server", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Connessione al server", False, f"Errore: {str(e)}")
        return False

def test_add_student():
    """Test 2: Aggiunta studente"""
    try:
        student_data = {
            "registro_num": 999,
            "nome": "Test",
            "cognome": "Studente"
        }
        response = requests.post(f"{BASE_URL}/add-student", json=student_data)
        passed = response.status_code in [200, 201, 409]  # 409 se già esiste
        data = response.json()
        print_test("Aggiunta studente", passed, f"Message: {data.get('message', 'OK')}")
        return passed
    except Exception as e:
        print_test("Aggiunta studente", False, f"Errore: {str(e)}")
        return False

def test_get_students():
    """Test 3: Recupero lista studenti"""
    try:
        response = requests.get(f"{BASE_URL}/students")
        passed = response.status_code == 200
        data = response.json()
        count = data.get('count', 0)
        print_test("Recupero lista studenti", passed, f"Studenti trovati: {count}")
        return passed and count > 0
    except Exception as e:
        print_test("Recupero lista studenti", False, f"Errore: {str(e)}")
        return False

def test_create_calendar():
    """Test 4: Creazione calendario"""
    try:
        calendar_data = {
            "materia": TEST_MATERIA,
            "num_lezioni": 3,
            "distribuzione": [2, 2, 2]
        }
        response = requests.post(f"{BASE_URL}/create-calendar", json=calendar_data)
        passed = response.status_code == 200
        data = response.json()
        
        if passed:
            calendario = data.get('calendario', {})
            total = sum(len(studenti) for studenti in calendario.values())
            print_test("Creazione calendario", passed, f"Interrogazioni create: {total}")
        else:
            print_test("Creazione calendario", passed, f"Errore: {data.get('error', 'Unknown')}")
        
        return passed
    except Exception as e:
        print_test("Creazione calendario", False, f"Errore: {str(e)}")
        return False

def test_get_calendar():
    """Test 5: Recupero calendario"""
    try:
        response = requests.get(f"{BASE_URL}/get-calendar/{TEST_MATERIA}")
        passed = response.status_code == 200
        data = response.json()
        total = data.get('total_interrogations', 0)
        print_test("Recupero calendario", passed, f"Interrogazioni: {total}")
        return passed
    except Exception as e:
        print_test("Recupero calendario", False, f"Errore: {str(e)}")
        return False

def test_shuffle():
    """Test 6: Rimescola calendario"""
    try:
        response = requests.post(f"{BASE_URL}/shuffle-assignments", 
                                json={"materia": TEST_MATERIA})
        passed = response.status_code == 200
        data = response.json()
        print_test("Rimescola calendario", passed, data.get('message', ''))
        return passed
    except Exception as e:
        print_test("Rimescola calendario", False, f"Errore: {str(e)}")
        return False

def test_ai_advice():
    """Test 7: Consigli AI"""
    try:
        response = requests.post(f"{BASE_URL}/ai-advice", 
                                json={"materia": TEST_MATERIA, "advice_type": "quality"})
        passed = response.status_code == 200
        data = response.json()
        
        if passed and 'advice' in data:
            score = data['advice'].get('score', 0)
            quality = data['advice'].get('quality', 'N/A')
            print_test("Consigli AI", passed, f"Quality Score: {score}/100 ({quality})")
        else:
            print_test("Consigli AI", passed)
        
        return passed
    except Exception as e:
        print_test("Consigli AI", False, f"Errore: {str(e)}")
        return False

def test_save_db():
    """Test 8: Salvataggio database"""
    try:
        response = requests.post(f"{BASE_URL}/save-to-db")
        passed = response.status_code == 200
        data = response.json()
        print_test("Salvataggio MySQL", passed, data.get('message', ''))
        return passed
    except Exception as e:
        print_test("Salvataggio MySQL", False, f"Errore: {str(e)}")
        return False

def test_save_tinydb():
    """Test 9: Salvataggio TinyDB"""
    try:
        response = requests.post(f"{BASE_URL}/save-to-tinydb")
        passed = response.status_code == 200
        data = response.json()
        print_test("Salvataggio TinyDB", passed, data.get('message', ''))
        return passed
    except Exception as e:
        print_test("Salvataggio TinyDB", False, f"Errore: {str(e)}")
        return False

def cleanup():
    """Cleanup: Rimuove dati di test"""
    try:
        # Rimuovi studente di test
        requests.delete(f"{BASE_URL}/remove-student/999")
        print(f"\n{Colors.BLUE}Cleanup completato{Colors.END}")
    except:
        pass

def main():
    """Esegue tutti i test"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print("TEST SUITE - Sistema Interrogazioni Programmate")
    print(f"{'='*50}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Server URL: {BASE_URL}{Colors.END}\n")
    
    # Lista test
    tests = [
        ("Connessione", test_connection),
        ("Aggiunta Studente", test_add_student),
        ("Lista Studenti", test_get_students),
        ("Crea Calendario", test_create_calendar),
        ("Recupera Calendario", test_get_calendar),
        ("Rimescola", test_shuffle),
        ("AI Advisor", test_ai_advice),
        ("Salva MySQL", test_save_db),
        ("Salva TinyDB", test_save_tinydb),
    ]
    
    results = []
    
    # Esegui test
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print_test(name, False, f"Eccezione: {str(e)}")
            results.append(False)
        print()  # Linea vuota tra test
    
    # Cleanup
    cleanup()
    
    # Risultati finali
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.BLUE}{'='*50}")
    print("RISULTATI FINALI")
    print(f"{'='*50}{Colors.END}\n")
    
    color = Colors.GREEN if percentage >= 80 else Colors.YELLOW if percentage >= 60 else Colors.RED
    print(f"Test passati: {color}{passed}/{total} ({percentage:.0f}%){Colors.END}")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}🎉 Tutti i test superati! L'applicazione funziona correttamente.{Colors.END}")
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}⚠ Alcuni test falliti, ma l'applicazione è funzionante.{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ Molti test falliti. Controlla la configurazione.{Colors.END}")
    
    print(f"\n{Colors.BLUE}Suggerimenti:{Colors.END}")
    print("- Assicurati che il server sia avviato (python app.py)")
    print("- Verifica che MySQL sia configurato correttamente")
    print("- Controlla il file .env per le credenziali")
    print("- Consulta README.md per troubleshooting\n")
    
    return 0 if percentage >= 80 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrotti dall'utente{Colors.END}")
        cleanup()
        sys.exit(1)
