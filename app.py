"""
Applicazione Flask principale per gestione interrogazioni programmate
Fornisce API REST per gestione studenti e calendario interrogazioni
"""
# Usa PyMySQL al posto di mysqlclient su Windows
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import csv
import random
from datetime import datetime
from io import StringIO
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm

# Import moduli personalizzati
from app.models import db, Student, Interrogation, CalendarConfiguration
from config.config import get_config
from utils.database_manager import TinyDBManager
from utils.ai_advisor import AIAdvisor

# Inizializza Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Inizializza estensioni
CORS(app)
db.init_app(app)

# Inizializza gestori
tinydb_manager = TinyDBManager(app.config['TINYDB_PATH'])
ai_advisor = AIAdvisor()

# Crea directory necessarie
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
os.makedirs('uploads', exist_ok=True)


# ==================== UTILITY FUNCTIONS ====================

def allowed_file(filename):
    """
    Verifica se il file ha un'estensione permessa
    
    Args:
        filename (str): Nome del file
        
    Returns:
        bool: True se permesso
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def generate_pdf_calendar(filepath, materia, interrogations):
    """
    Genera un file PDF con il calendario delle interrogazioni
    
    Args:
        filepath (str): Percorso del file PDF da creare
        materia (str): Nome della materia
        interrogations (list): Lista di oggetti Interrogation
    """
    # Crea documento PDF
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Elementi del documento
    elements = []
    styles = getSampleStyleSheet()
    
    # Titolo
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=1  # Center
    )
    title = Paragraph(f"Calendario Interrogazioni<br/>{materia}", title_style)
    elements.append(title)
    
    # Data di generazione
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    date_text = Paragraph(f"Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}", date_style)
    elements.append(date_text)
    elements.append(Spacer(1, 1*cm))
    
    # Raggruppa interrogazioni per lezione
    lezioni = {}
    for interr in interrogations:
        if interr.lezione_num not in lezioni:
            lezioni[interr.lezione_num] = []
        lezioni[interr.lezione_num].append(interr)
    
    # Crea tabelle per ogni lezione
    for lezione_num in sorted(lezioni.keys()):
        # Titolo lezione
        lezione_style = ParagraphStyle(
            'LessonTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=10
        )
        lezione_title = Paragraph(f"Lezione {lezione_num}", lezione_style)
        elements.append(lezione_title)
        
        # Dati tabella
        table_data = [['Ordine', 'Registro', 'Nome', 'Cognome', 'Data Lezione']]
        
        for interr in sorted(lezioni[lezione_num], key=lambda x: x.ordine):
            table_data.append([
                str(interr.ordine),
                str(interr.student.registro_num),
                interr.student.nome,
                interr.student.cognome,
                interr.data_lezione.strftime('%d/%m/%Y') if interr.data_lezione else 'N/A'
            ])
        
        # Crea tabella
        table = Table(table_data, colWidths=[2*cm, 2.5*cm, 4*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),  # Centra ordine e registro
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*cm))
    
    # Statistiche finali
    elements.append(Spacer(1, 1*cm))
    stats_style = ParagraphStyle(
        'StatsStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333')
    )
    
    total_interr = len(interrogations)
    total_lezioni = len(lezioni)
    studenti_unici = len(set(i.student_id for i in interrogations))
    
    stats_text = f"""
    <b>Statistiche:</b><br/>
    • Totale interrogazioni: {total_interr}<br/>
    • Numero lezioni: {total_lezioni}<br/>
    • Studenti coinvolti: {studenti_unici}
    """
    
    stats = Paragraph(stats_text, stats_style)
    elements.append(stats)
    
    # Genera il PDF
    doc.build(elements)


def parse_csv(file_path):
    """
    Parsifica un file CSV e restituisce lista studenti
    
    Args:
        file_path (str): Percorso del file CSV
        
    Returns:
        list: Lista di dizionari con dati studenti
    """
    students = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            # Prova a rilevare il delimitatore
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row in reader:
                # Supporta vari formati di nomi colonne
                registro_num = row.get('registro_num') or row.get('numero_registro') or row.get('numero')
                nome = row.get('nome') or row.get('name')
                cognome = row.get('cognome') or row.get('surname') or row.get('lastname')
                
                if registro_num and nome and cognome:
                    students.append({
                        'registro_num': int(registro_num),
                        'nome': nome.strip(),
                        'cognome': cognome.strip()
                    })
        
        return students
    except Exception as e:
        raise Exception(f"Errore nel parsing CSV: {str(e)}")


def parse_json(file_path):
    """
    Parsifica un file JSON e restituisce lista studenti
    
    Args:
        file_path (str): Percorso del file JSON
        
    Returns:
        list: Lista di dizionari con dati studenti
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            
            # Supporta sia array diretto che oggetto con chiave 'students'
            if isinstance(data, list):
                students = data
            elif isinstance(data, dict) and 'students' in data:
                students = data['students']
            else:
                raise Exception("Formato JSON non valido")
            
            # Valida e normalizza i dati
            validated_students = []
            for student in students:
                registro_num = student.get('registro_num') or student.get('numero_registro') or student.get('numero')
                nome = student.get('nome') or student.get('name')
                cognome = student.get('cognome') or student.get('surname') or student.get('lastname')
                
                if registro_num and nome and cognome:
                    validated_students.append({
                        'registro_num': int(registro_num),
                        'nome': nome.strip(),
                        'cognome': cognome.strip()
                    })
            
            return validated_students
    except Exception as e:
        raise Exception(f"Errore nel parsing JSON: {str(e)}")


def create_random_calendar(students, lessons_per_week, distribution_per_lesson):
    """
    Crea un calendario casuale di interrogazioni
    
    Args:
        students (list): Lista di studenti
        lessons_per_week (int): Numero di giorni a settimana con interrogazioni
        distribution_per_lesson (list): Numero di studenti per ciascun giorno della settimana
        
    Returns:
        dict: Calendario con struttura {lezione_num: [studenti]}
    """
    # Shuffle studenti per casualità (nessuno verrà ripetuto)
    available_students = students.copy()
    random.shuffle(available_students)
    
    total_students = len(available_students)
    
    # Calcola quanti studenti interroghiamo ogni settimana
    students_per_week = sum(distribution_per_lesson)
    
    # Calcola il numero totale di lezioni necessarie per interrogare tutti
    # Cicliamo la distribuzione settimanale finché non finiamo gli studenti
    calendario = {}
    student_index = 0
    lezione_num = 1
    week = 1
    
    while student_index < total_students:
        # Per ogni giorno della settimana
        for day_index in range(lessons_per_week):
            if student_index >= total_students:
                break
                
            num_students_needed = distribution_per_lesson[day_index]
            
            # Estrai studenti per questa lezione
            students_for_lesson = []
            for i in range(num_students_needed):
                if student_index < total_students:
                    students_for_lesson.append(available_students[student_index])
                    student_index += 1
            
            if students_for_lesson:  # Solo se ci sono studenti
                calendario[lezione_num] = students_for_lesson
                lezione_num += 1
        
        week += 1
    
    return calendario


# ==================== ROUTES - PAGINE ====================

@app.route('/')
def index():
    """
    Homepage - Configurazione calendario
    
    Returns:
        HTML: Template della homepage
    """
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    """
    Pagina upload studenti
    
    Returns:
        HTML: Template upload
    """
    return render_template('upload.html')


@app.route('/calendar')
def calendar_page():
    """
    Pagina visualizzazione calendario
    
    Returns:
        HTML: Template calendario
    """
    return render_template('calendar.html')


# ==================== API - STUDENTI ====================

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Recupera tutti gli studenti
    
    Returns:
        JSON: Lista studenti
    """
    try:
        students = Student.query.all()
        return jsonify({
            'success': True,
            'students': [student.to_dict() for student in students],
            'count': len(students)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/add-student', methods=['POST'])
def add_student():
    """
    Aggiunge un nuovo studente
    
    Request Body:
        registro_num (int): Numero di registro
        nome (str): Nome
        cognome (str): Cognome
        
    Returns:
        JSON: Conferma operazione
    """
    try:
        data = request.get_json()
        
        # Validazione
        if not all(k in data for k in ['registro_num', 'nome', 'cognome']):
            return jsonify({'success': False, 'error': 'Dati mancanti'}), 400
        
        # Controlla se già esistente
        existing = Student.query.filter_by(registro_num=data['registro_num']).first()
        if existing:
            return jsonify({'success': False, 'error': 'Studente già esistente'}), 409
        
        # Crea nuovo studente
        student = Student(
            registro_num=data['registro_num'],
            nome=data['nome'],
            cognome=data['cognome']
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Salva anche su TinyDB
        tinydb_manager.add_student(data['registro_num'], data['nome'], data['cognome'])
        
        return jsonify({
            'success': True,
            'message': 'Studente aggiunto con successo',
            'student': student.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/remove-student/<int:registro_num>', methods=['DELETE'])
def remove_student(registro_num):
    """
    Rimuove uno studente
    
    Args:
        registro_num (int): Numero di registro
        
    Returns:
        JSON: Conferma operazione
    """
    try:
        student = Student.query.filter_by(registro_num=registro_num).first()
        
        if not student:
            return jsonify({'success': False, 'error': 'Studente non trovato'}), 404
        
        db.session.delete(student)
        db.session.commit()
        
        # Rimuovi anche da TinyDB
        tinydb_manager.delete_student(registro_num)
        
        return jsonify({
            'success': True,
            'message': 'Studente rimosso con successo'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/upload-students', methods=['POST'])
def upload_students():
    """
    Upload file CSV o JSON con lista studenti
    
    Returns:
        JSON: Risultato upload
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Nessun file caricato'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nome file vuoto'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Formato file non permesso'}), 400
        
        # Salva file temporaneamente
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Parse file
        if filename.endswith('.csv'):
            students = parse_csv(filepath)
        else:
            students = parse_json(filepath)
        
        # Importa studenti nel database
        imported_count = 0
        skipped_count = 0
        errors = []
        
        for student_data in students:
            try:
                # Controlla se esiste già
                existing = Student.query.filter_by(registro_num=student_data['registro_num']).first()
                if existing:
                    skipped_count += 1
                    continue
                
                # Crea nuovo studente
                student = Student(**student_data)
                db.session.add(student)
                
                # Aggiungi anche a TinyDB
                tinydb_manager.add_student(
                    student_data['registro_num'],
                    student_data['nome'],
                    student_data['cognome']
                )
                
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Errore studente {student_data.get('registro_num', '?')}: {str(e)}")
        
        db.session.commit()
        
        # Rimuovi file temporaneo
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Import completato: {imported_count} studenti importati, {skipped_count} saltati',
            'imported': imported_count,
            'skipped': skipped_count,
            'errors': errors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== API - CALENDARIO ====================

@app.route('/api/create-calendar', methods=['POST'])
def create_calendar():
    """
    Crea un nuovo calendario di interrogazioni
    
    Request Body:
        materia (str): Nome materia
        num_lezioni (int): Numero lezioni settimanali
        distribuzione (list): Numero studenti per lezione
        
    Returns:
        JSON: Calendario creato
    """
    try:
        data = request.get_json()
        
        # Validazione
        if not all(k in data for k in ['materia', 'num_lezioni', 'distribuzione']):
            return jsonify({'success': False, 'error': 'Dati mancanti'}), 400
        
        materia = data['materia']
        giorni_settimana = data['num_lezioni']  # Giorni a settimana con interrogazioni
        distribuzione = data['distribuzione']  # Studenti per ciascun giorno
        
        # Recupera studenti
        students = Student.query.all()
        students_list = [s.to_dict() for s in students]
        
        if not students_list:
            return jsonify({'success': False, 'error': 'Nessuno studente disponibile'}), 400
        
        # Calcola numero totale lezioni necessarie
        total_students = len(students_list)
        students_per_week = sum(distribuzione)
        
        # Calcola settimane necessarie e totale lezioni
        weeks_needed = (total_students + students_per_week - 1) // students_per_week
        num_lezioni_totali = weeks_needed * giorni_settimana
        
        # Crea calendario casuale (interroga tutti gli studenti una volta)
        calendario = create_random_calendar(students_list, giorni_settimana, distribuzione)
        
        # Salva interrogazioni nel database
        Interrogation.query.filter_by(materia=materia).delete()  # Pulisci vecchie
        
        for lezione_num, students_in_lesson in calendario.items():
            for ordine, student in enumerate(students_in_lesson, 1):
                interrogation = Interrogation(
                    materia=materia,
                    student_id=student['id'],
                    lezione_num=lezione_num,
                    ordine=ordine
                )
                db.session.add(interrogation)
        
        # Salva configurazione
        config = CalendarConfiguration(
            materia=materia,
            num_lezioni=len(calendario),  # Numero totale di lezioni effettive
            distribuzione=json.dumps(distribuzione)
        )
        db.session.add(config)
        db.session.commit()
        
        # Ottieni consigli AI
        ai_analysis = ai_advisor.analyze_distribution(calendario)
        quality_score = ai_advisor.evaluate_schedule_quality(calendario, len(students_list))
        
        return jsonify({
            'success': True,
            'message': 'Calendario creato con successo',
            'calendario': calendario,
            'ai_analysis': ai_analysis,
            'quality_score': quality_score
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shuffle-assignments', methods=['POST'])
def shuffle_assignments():
    """
    Rimescola le assegnazioni mantenendo la distribuzione
    
    Request Body:
        materia (str): Nome materia
        
    Returns:
        JSON: Nuovo calendario
    """
    try:
        data = request.get_json()
        materia = data.get('materia')
        
        if not materia:
            return jsonify({'success': False, 'error': 'Materia non specificata'}), 400
        
        # Recupera configurazione esistente
        config = CalendarConfiguration.query.filter_by(materia=materia).order_by(
            CalendarConfiguration.created_at.desc()
        ).first()
        
        if not config:
            return jsonify({'success': False, 'error': 'Configurazione non trovata'}), 404
        
        # Ricarica parametri
        distribuzione = json.loads(config.distribuzione)
        giorni_settimana = len(distribuzione)  # Numero giorni a settimana
        
        # Recupera studenti
        students = Student.query.all()
        students_list = [s.to_dict() for s in students]
        
        # Crea nuovo calendario (calcola automaticamente le lezioni necessarie)
        calendario = create_random_calendar(students_list, giorni_settimana, distribuzione)
        
        # Aggiorna database
        Interrogation.query.filter_by(materia=materia).delete()
        
        for lezione_num, students_in_lesson in calendario.items():
            for ordine, student in enumerate(students_in_lesson, 1):
                interrogation = Interrogation(
                    materia=materia,
                    student_id=student['id'],
                    lezione_num=lezione_num,
                    ordine=ordine
                )
                db.session.add(interrogation)
        
        db.session.commit()
        
        # AI analysis
        ai_analysis = ai_advisor.analyze_distribution(calendario)
        quality_score = ai_advisor.evaluate_schedule_quality(calendario, len(students_list))
        
        return jsonify({
            'success': True,
            'message': 'Calendario rimescolato con successo',
            'calendario': calendario,
            'ai_analysis': ai_analysis,
            'quality_score': quality_score
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/get-calendar/<materia>', methods=['GET'])
def get_calendar(materia):
    """
    Recupera il calendario per una materia
    
    Args:
        materia (str): Nome materia
        
    Returns:
        JSON: Calendario
    """
    try:
        interrogations = Interrogation.query.filter_by(materia=materia).order_by(
            Interrogation.lezione_num, Interrogation.ordine
        ).all()
        
        # Organizza per lezione
        calendario = {}
        for interr in interrogations:
            if interr.lezione_num not in calendario:
                calendario[interr.lezione_num] = []
            calendario[interr.lezione_num].append(interr.to_dict())
        
        return jsonify({
            'success': True,
            'calendario': calendario,
            'total_interrogations': len(interrogations)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/modify-day', methods=['PUT'])
def modify_day():
    """
    Modifica il numero di studenti in un giorno specifico
    
    Request Body:
        materia (str): Nome materia
        lezione_num (int): Numero lezione
        new_count (int): Nuovo numero studenti
        
    Returns:
        JSON: Risultato modifica
    """
    try:
        data = request.get_json()
        materia = data.get('materia')
        lezione_num = data.get('lezione_num')
        new_count = data.get('new_count')
        
        # Recupera interrogazioni del giorno
        current_interr = Interrogation.query.filter_by(
            materia=materia,
            lezione_num=lezione_num
        ).all()
        
        current_count = len(current_interr)
        
        if new_count < current_count:
            # Rimuovi eccedenti
            to_remove = current_count - new_count
            for i in range(to_remove):
                db.session.delete(current_interr[-(i+1)])
        
        elif new_count > current_count:
            # Aggiungi nuovi slot
            # Trova studenti non ancora assegnati
            all_students = Student.query.all()
            assigned_ids = [interr.student_id for interr in Interrogation.query.filter_by(materia=materia).all()]
            available_students = [s for s in all_students if s.id not in assigned_ids]
            
            to_add = new_count - current_count
            random.shuffle(available_students)
            
            for i in range(min(to_add, len(available_students))):
                new_interr = Interrogation(
                    materia=materia,
                    student_id=available_students[i].id,
                    lezione_num=lezione_num,
                    ordine=current_count + i + 1
                )
                db.session.add(new_interr)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Lezione {lezione_num} aggiornata con successo'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/change-student-in-day', methods=['PUT'])
def change_student_in_day():
    """
    Cambia uno studente specifico in un giorno
    
    Request Body:
        materia (str): Nome materia
        lezione_num (int): Numero lezione
        old_student_id (int): ID studente da sostituire
        new_registro_num (int): Numero registro nuovo studente
        
    Returns:
        JSON: Risultato modifica
    """
    try:
        data = request.get_json()
        materia = data.get('materia')
        lezione_num = data.get('lezione_num')
        old_student_id = data.get('old_student_id')
        new_registro_num = data.get('new_registro_num')
        
        # Trova interrogazione da modificare
        interrogation = Interrogation.query.filter_by(
            materia=materia,
            lezione_num=lezione_num,
            student_id=old_student_id
        ).first()
        
        if not interrogation:
            return jsonify({'success': False, 'error': 'Interrogazione non trovata'}), 404
        
        # Trova nuovo studente
        new_student = Student.query.filter_by(registro_num=new_registro_num).first()
        
        if not new_student:
            return jsonify({'success': False, 'error': 'Nuovo studente non trovato'}), 404
        
        # Aggiorna
        interrogation.student_id = new_student.id
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Studente sostituito con successo',
            'interrogation': interrogation.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== API - SALVATAGGIO ED ESPORTAZIONE ====================

@app.route('/api/save-to-db', methods=['POST'])
def save_to_db():
    """
    Forza il salvataggio su MySQL (già fatto automaticamente)
    
    Returns:
        JSON: Conferma
    """
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Dati salvati su MySQL'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/save-to-tinydb', methods=['POST'])
def save_to_tinydb():
    """
    Salva tutto su TinyDB
    
    Returns:
        JSON: Conferma
    """
    try:
        # Esporta studenti
        students = Student.query.all()
        tinydb_manager.clear_students()
        for student in students:
            tinydb_manager.add_student(
                student.registro_num,
                student.nome,
                student.cognome
            )
        
        # Esporta interrogazioni
        interrogations = Interrogation.query.all()
        tinydb_manager.clear_interrogations()
        for interr in interrogations:
            tinydb_manager.add_interrogation(
                interr.materia,
                interr.student.registro_num,
                interr.lezione_num,
                interr.ordine,
                interr.data_lezione.isoformat() if interr.data_lezione else None
            )
        
        return jsonify({
            'success': True,
            'message': 'Dati salvati su TinyDB'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_data():
    """
    Esporta il calendario in CSV, JSON o PDF
    
    Request Body:
        materia (str): Nome materia
        format (str): 'csv', 'json' o 'pdf'
        
    Returns:
        File: File scaricabile
    """
    try:
        data = request.get_json()
        materia = data.get('materia')
        format_type = data.get('format', 'csv')
        
        # Recupera interrogazioni
        interrogations = Interrogation.query.filter_by(materia=materia).order_by(
            Interrogation.lezione_num, Interrogation.ordine
        ).all()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'csv':
            # Esporta CSV
            filename = f'calendario_{materia}_{timestamp}.csv'
            filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Materia', 'Lezione', 'Ordine', 'Registro', 'Nome', 'Cognome', 'Data'])
                
                for interr in interrogations:
                    writer.writerow([
                        interr.materia,
                        interr.lezione_num,
                        interr.ordine,
                        interr.student.registro_num,
                        interr.student.nome,
                        interr.student.cognome,
                        interr.data_lezione.isoformat() if interr.data_lezione else ''
                    ])
            
            return send_file(filepath, as_attachment=True, download_name=filename)
        
        elif format_type == 'pdf':
            # Esporta PDF
            filename = f'calendario_{materia}_{timestamp}.pdf'
            filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
            
            # Crea il PDF
            generate_pdf_calendar(filepath, materia, interrogations)
            
            return send_file(filepath, as_attachment=True, download_name=filename)
        
        else:
            # Esporta JSON
            filename = f'calendario_{materia}_{timestamp}.json'
            filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
            
            export_data = {
                'materia': materia,
                'exported_at': datetime.now().isoformat(),
                'interrogations': [interr.to_dict() for interr in interrogations]
            }
            
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, ensure_ascii=False, indent=2)
            
            return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== API - AI ADVISOR ====================

@app.route('/api/ai-advice', methods=['POST'])
def get_ai_advice():
    """
    Ottiene consigli AI sul calendario
    
    Request Body:
        materia (str): Nome materia
        advice_type (str): Tipo di consiglio richiesto
        
    Returns:
        JSON: Consigli AI
    """
    try:
        data = request.get_json()
        materia = data.get('materia')
        advice_type = data.get('advice_type', 'general')
        
        if advice_type == 'general':
            advice = ai_advisor.get_general_advice()
        
        elif advice_type == 'distribution':
            interrogations = Interrogation.query.filter_by(materia=materia).all()
            calendario = {}
            for interr in interrogations:
                if interr.lezione_num not in calendario:
                    calendario[interr.lezione_num] = []
                calendario[interr.lezione_num].append(interr.to_dict())
            
            advice = ai_advisor.analyze_distribution(calendario)
        
        elif advice_type == 'quality':
            interrogations = Interrogation.query.filter_by(materia=materia).all()
            calendario = {}
            for interr in interrogations:
                if interr.lezione_num not in calendario:
                    calendario[interr.lezione_num] = []
                calendario[interr.lezione_num].append(interr.to_dict())
            
            total_students = Student.query.count()
            advice = ai_advisor.evaluate_schedule_quality(calendario, total_students)
        
        elif advice_type == 'study_time':
            interrogations = Interrogation.query.filter_by(materia=materia).all()
            calendario = {}
            for interr in interrogations:
                if interr.lezione_num not in calendario:
                    calendario[interr.lezione_num] = []
                calendario[interr.lezione_num].append(interr.to_dict())
            
            advice = ai_advisor.generate_study_time_advice(calendario)
        
        else:
            advice = ai_advisor.get_general_advice()
        
        return jsonify({
            'success': True,
            'advice': advice
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== VISUALIZZAZIONE INTERROGAZIONI ====================

@app.route('/api/interrogations', methods=['GET'])
def get_interrogations():
    """
    Endpoint per visualizzare tutte le interrogazioni salvate nel database
    
    Query Parameters:
        materia (str, optional): Filtra per materia specifica
        student_id (int, optional): Filtra per studente specifico
        limit (int, optional): Limita il numero di risultati
    
    Returns:
        JSON: {
            "success": bool,
            "count": int,
            "interrogations": [...]
        }
    """
    try:
        # Ottieni parametri di filtro
        materia = request.args.get('materia')
        student_id = request.args.get('student_id', type=int)
        limit = request.args.get('limit', type=int)
        
        # Query base
        query = Interrogation.query
        
        # Applica filtri se presenti
        if materia:
            query = query.filter_by(materia=materia)
        if student_id:
            query = query.filter_by(student_id=student_id)
        
        # Ordina per materia, lezione e ordine
        query = query.order_by(
            Interrogation.materia,
            Interrogation.lezione_num,
            Interrogation.ordine
        )
        
        # Applica limite se specificato
        if limit:
            query = query.limit(limit)
        
        # Esegui query
        interrogations = query.all()
        
        # Converti in dizionari
        result = [interr.to_dict() for interr in interrogations]
        
        return jsonify({
            'success': True,
            'count': len(result),
            'interrogations': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Errore durante recupero interrogazioni: {str(e)}'
        }), 500


@app.route('/api/interrogations/<int:interrogation_id>', methods=['GET'])
def get_interrogation_by_id(interrogation_id):
    """
    Endpoint per visualizzare una singola interrogazione per ID
    
    Args:
        interrogation_id (int): ID dell'interrogazione
    
    Returns:
        JSON: {
            "success": bool,
            "interrogation": {...}
        }
    """
    try:
        interrogation = Interrogation.query.get(interrogation_id)
        
        if not interrogation:
            return jsonify({
                'success': False,
                'error': 'Interrogazione non trovata'
            }), 404
        
        return jsonify({
            'success': True,
            'interrogation': interrogation.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Errore durante recupero interrogazione: {str(e)}'
        }), 500


@app.route('/interrogations')
def view_interrogations():
    """
    Pagina HTML per visualizzare le interrogazioni salvate
    """
    return render_template('interrogations.html')


# ==================== ERRORI ====================

@app.errorhandler(404)
def not_found(error):
    """Handler errore 404"""
    return jsonify({'success': False, 'error': 'Risorsa non trovata'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler errore 500"""
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Errore interno del server'}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        # Crea tabelle se non esistono (solo se MySQL è disponibile)
        try:
            db.create_all()
            print("✓ Database MySQL connesso e tabelle create")
        except Exception as e:
            print(f"⚠ MySQL non disponibile: {e}")
            print("✓ L'applicazione funzionerà solo con TinyDB")
    
    print("\n" + "="*50)
    print("  Applicazione Interrogazioni Programmate")
    print("="*50)
    print(f"\n✓ Server in esecuzione su http://localhost:{app.config['PORT']}")
    print(f"✓ Accesso LAN: http://<tuo-ip>:{app.config['PORT']}")
    print("\nPremi CTRL+C per fermare il server\n")
    
    # Avvia server
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
