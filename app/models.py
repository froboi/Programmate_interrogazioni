"""
Modelli del database per l'applicazione di gestione interrogazioni
Utilizza SQLAlchemy per ORM con MySQL
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inizializza SQLAlchemy
db = SQLAlchemy()


class Student(db.Model):
    """
    Modello per rappresentare uno studente
    
    Attributes:
        id (int): ID univoco (auto-incrementale)
        registro_num (int): Numero di registro dello studente
        nome (str): Nome dello studente
        cognome (str): Cognome dello studente
        created_at (datetime): Data di creazione del record
    """
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registro_num = db.Column(db.Integer, nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relazione con le interrogazioni
    interrogazioni = db.relationship('Interrogation', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """
        Converte l'oggetto Student in un dizionario
        
        Returns:
            dict: Rappresentazione in dizionario dello studente
        """
        return {
            'id': self.id,
            'registro_num': self.registro_num,
            'nome': self.nome,
            'cognome': self.cognome,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """
        Rappresentazione testuale dello studente
        
        Returns:
            str: Stringa rappresentativa
        """
        return f'<Student {self.registro_num}: {self.nome} {self.cognome}>'


class Interrogation(db.Model):
    """
    Modello per rappresentare un'interrogazione programmata
    
    Attributes:
        id (int): ID univoco (auto-incrementale)
        materia (str): Nome della materia
        student_id (int): ID dello studente (FK)
        lezione_num (int): Numero della lezione
        data_lezione (date): Data della lezione (opzionale)
        ordine (int): Ordine dell'interrogazione nella lezione
        created_at (datetime): Data di creazione del record
        updated_at (datetime): Data di ultimo aggiornamento
    """
    __tablename__ = 'interrogations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materia = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    lezione_num = db.Column(db.Integer, nullable=False)
    data_lezione = db.Column(db.Date, nullable=True)
    ordine = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """
        Converte l'oggetto Interrogation in un dizionario
        
        Returns:
            dict: Rappresentazione in dizionario dell'interrogazione
        """
        return {
            'id': self.id,
            'materia': self.materia,
            'student_id': self.student_id,
            'student': self.student.to_dict() if self.student else None,
            'lezione_num': self.lezione_num,
            'data_lezione': self.data_lezione.isoformat() if self.data_lezione else None,
            'ordine': self.ordine,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """
        Rappresentazione testuale dell'interrogazione
        
        Returns:
            str: Stringa rappresentativa
        """
        return f'<Interrogation {self.materia} - Lezione {self.lezione_num} - Student {self.student_id}>'


class CalendarConfiguration(db.Model):
    """
    Modello per salvare la configurazione del calendario
    
    Attributes:
        id (int): ID univoco
        materia (str): Nome della materia
        num_lezioni (int): Numero di lezioni settimanali
        distribuzione (str): Distribuzione alunni per lezione (JSON serializzato)
        created_at (datetime): Data di creazione
    """
    __tablename__ = 'calendar_configurations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materia = db.Column(db.String(100), nullable=False)
    num_lezioni = db.Column(db.Integer, nullable=False)
    distribuzione = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """
        Converte l'oggetto CalendarConfiguration in un dizionario
        
        Returns:
            dict: Rappresentazione in dizionario
        """
        return {
            'id': self.id,
            'materia': self.materia,
            'num_lezioni': self.num_lezioni,
            'distribuzione': self.distribuzione,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """
        Rappresentazione testuale
        
        Returns:
            str: Stringa rappresentativa
        """
        return f'<CalendarConfiguration {self.materia} - {self.num_lezioni} lezioni>'
