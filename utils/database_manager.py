"""
Gestione database TinyDB per salvataggio locale
Fornisce funzioni per operazioni CRUD su database locale JSON
"""
from tinydb import TinyDB, Query
import os
import json
from datetime import datetime


class TinyDBManager:
    """
    Classe per gestire le operazioni con TinyDB
    """
    
    def __init__(self, db_path='database/local_db.json'):
        """
        Inizializza il database TinyDB
        
        Args:
            db_path (str): Percorso del file database JSON
        """
        # Crea la directory se non esiste
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db = TinyDB(db_path)
        self.students_table = self.db.table('students')
        self.interrogations_table = self.db.table('interrogations')
        self.configurations_table = self.db.table('configurations')
    
    # ========== OPERAZIONI STUDENTI ==========
    
    def add_student(self, registro_num, nome, cognome):
        """
        Aggiunge uno studente al database
        
        Args:
            registro_num (int): Numero di registro
            nome (str): Nome dello studente
            cognome (str): Cognome dello studente
            
        Returns:
            int: ID del documento inserito
        """
        student = {
            'registro_num': registro_num,
            'nome': nome,
            'cognome': cognome,
            'created_at': datetime.now().isoformat()
        }
        return self.students_table.insert(student)
    
    def get_all_students(self):
        """
        Recupera tutti gli studenti
        
        Returns:
            list: Lista di tutti gli studenti
        """
        return self.students_table.all()
    
    def get_student_by_registro(self, registro_num):
        """
        Cerca uno studente per numero di registro
        
        Args:
            registro_num (int): Numero di registro
            
        Returns:
            dict: Dati dello studente o None
        """
        Student = Query()
        return self.students_table.get(Student.registro_num == registro_num)
    
    def update_student(self, registro_num, nome=None, cognome=None):
        """
        Aggiorna i dati di uno studente
        
        Args:
            registro_num (int): Numero di registro
            nome (str, optional): Nuovo nome
            cognome (str, optional): Nuovo cognome
            
        Returns:
            list: Lista di IDs aggiornati
        """
        Student = Query()
        updates = {}
        if nome:
            updates['nome'] = nome
        if cognome:
            updates['cognome'] = cognome
        
        return self.students_table.update(updates, Student.registro_num == registro_num)
    
    def delete_student(self, registro_num):
        """
        Elimina uno studente
        
        Args:
            registro_num (int): Numero di registro
            
        Returns:
            list: Lista di IDs eliminati
        """
        Student = Query()
        return self.students_table.remove(Student.registro_num == registro_num)
    
    def clear_students(self):
        """
        Elimina tutti gli studenti
        
        Returns:
            None
        """
        self.students_table.truncate()
    
    def import_students_bulk(self, students_list):
        """
        Importa una lista di studenti in blocco
        
        Args:
            students_list (list): Lista di dizionari con dati studenti
            
        Returns:
            list: Lista di IDs inseriti
        """
        for student in students_list:
            student['created_at'] = datetime.now().isoformat()
        return self.students_table.insert_multiple(students_list)
    
    # ========== OPERAZIONI INTERROGAZIONI ==========
    
    def add_interrogation(self, materia, registro_num, lezione_num, ordine, data_lezione=None):
        """
        Aggiunge un'interrogazione
        
        Args:
            materia (str): Nome della materia
            registro_num (int): Numero di registro dello studente
            lezione_num (int): Numero della lezione
            ordine (int): Ordine dell'interrogazione
            data_lezione (str, optional): Data della lezione
            
        Returns:
            int: ID del documento inserito
        """
        interrogation = {
            'materia': materia,
            'registro_num': registro_num,
            'lezione_num': lezione_num,
            'ordine': ordine,
            'data_lezione': data_lezione,
            'created_at': datetime.now().isoformat()
        }
        return self.interrogations_table.insert(interrogation)
    
    def get_all_interrogations(self):
        """
        Recupera tutte le interrogazioni
        
        Returns:
            list: Lista di tutte le interrogazioni
        """
        return self.interrogations_table.all()
    
    def get_interrogations_by_materia(self, materia):
        """
        Recupera interrogazioni per materia
        
        Args:
            materia (str): Nome della materia
            
        Returns:
            list: Lista di interrogazioni
        """
        Interrogation = Query()
        return self.interrogations_table.search(Interrogation.materia == materia)
    
    def get_interrogations_by_lezione(self, lezione_num):
        """
        Recupera interrogazioni per numero lezione
        
        Args:
            lezione_num (int): Numero della lezione
            
        Returns:
            list: Lista di interrogazioni
        """
        Interrogation = Query()
        return self.interrogations_table.search(Interrogation.lezione_num == lezione_num)
    
    def update_interrogation(self, doc_id, **kwargs):
        """
        Aggiorna un'interrogazione
        
        Args:
            doc_id (int): ID del documento
            **kwargs: Campi da aggiornare
            
        Returns:
            list: Lista di IDs aggiornati
        """
        return self.interrogations_table.update(kwargs, doc_ids=[doc_id])
    
    def delete_interrogation(self, doc_id):
        """
        Elimina un'interrogazione
        
        Args:
            doc_id (int): ID del documento
            
        Returns:
            list: Lista di IDs eliminati
        """
        return self.interrogations_table.remove(doc_ids=[doc_id])
    
    def clear_interrogations(self):
        """
        Elimina tutte le interrogazioni
        
        Returns:
            None
        """
        self.interrogations_table.truncate()
    
    def import_interrogations_bulk(self, interrogations_list):
        """
        Importa una lista di interrogazioni in blocco
        
        Args:
            interrogations_list (list): Lista di dizionari con dati interrogazioni
            
        Returns:
            list: Lista di IDs inseriti
        """
        for interrogation in interrogations_list:
            interrogation['created_at'] = datetime.now().isoformat()
        return self.interrogations_table.insert_multiple(interrogations_list)
    
    # ========== OPERAZIONI CONFIGURAZIONI ==========
    
    def save_configuration(self, materia, num_lezioni, distribuzione):
        """
        Salva una configurazione del calendario
        
        Args:
            materia (str): Nome della materia
            num_lezioni (int): Numero di lezioni
            distribuzione (dict/list): Distribuzione alunni
            
        Returns:
            int: ID del documento inserito
        """
        config = {
            'materia': materia,
            'num_lezioni': num_lezioni,
            'distribuzione': json.dumps(distribuzione) if not isinstance(distribuzione, str) else distribuzione,
            'created_at': datetime.now().isoformat()
        }
        return self.configurations_table.insert(config)
    
    def get_latest_configuration(self):
        """
        Recupera l'ultima configurazione salvata
        
        Returns:
            dict: Ultima configurazione o None
        """
        configs = self.configurations_table.all()
        return configs[-1] if configs else None
    
    def get_all_configurations(self):
        """
        Recupera tutte le configurazioni
        
        Returns:
            list: Lista di configurazioni
        """
        return self.configurations_table.all()
    
    # ========== UTILITÀ ==========
    
    def export_to_json(self, filepath):
        """
        Esporta l'intero database in un file JSON
        
        Args:
            filepath (str): Percorso del file di output
            
        Returns:
            bool: True se successo
        """
        try:
            data = {
                'students': self.students_table.all(),
                'interrogations': self.interrogations_table.all(),
                'configurations': self.configurations_table.all()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Errore durante l'esportazione: {e}")
            return False
    
    def import_from_json(self, filepath):
        """
        Importa dati da un file JSON
        
        Args:
            filepath (str): Percorso del file di input
            
        Returns:
            bool: True se successo
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'students' in data:
                self.students_table.insert_multiple(data['students'])
            
            if 'interrogations' in data:
                self.interrogations_table.insert_multiple(data['interrogations'])
            
            if 'configurations' in data:
                self.configurations_table.insert_multiple(data['configurations'])
            
            return True
        except Exception as e:
            print(f"Errore durante l'importazione: {e}")
            return False
    
    def close(self):
        """
        Chiude il database
        
        Returns:
            None
        """
        self.db.close()
