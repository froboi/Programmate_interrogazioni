"""
Modulo AI Advisor per fornire consigli intelligenti sulla gestione delle interrogazioni
Fornisce suggerimenti per ottimizzazione calendario, strategie di interrogazione, etc.
"""
import random
from datetime import datetime, timedelta
from collections import Counter


class AIAdvisor:
    """
    Classe per fornire consigli intelligenti sulle interrogazioni
    """
    
    def __init__(self):
        """
        Inizializza l'AI Advisor
        """
        self.suggestions = []
    
    def analyze_distribution(self, calendario):
        """
        Analizza la distribuzione degli studenti nelle lezioni
        
        Args:
            calendario (dict): Dizionario con struttura {lezione_num: [studenti]}
            
        Returns:
            dict: Analisi e suggerimenti
        """
        suggestions = []
        warnings = []
        
        # Conta studenti per lezione
        student_counts = {lezione: len(studenti) for lezione, studenti in calendario.items()}
        
        # Controlla bilanciamento
        if student_counts:
            max_count = max(student_counts.values())
            min_count = min(student_counts.values())
            avg_count = sum(student_counts.values()) / len(student_counts)
            
            # Suggerimenti basati su bilanciamento
            if max_count - min_count > 2:
                warnings.append({
                    'type': 'unbalanced',
                    'message': f'Distribuzione sbilanciata: alcune lezioni hanno fino a {max_count} interrogazioni mentre altre solo {min_count}',
                    'suggestion': 'Considera di riequilibrare il numero di interrogazioni per lezione'
                })
            else:
                suggestions.append({
                    'type': 'balanced',
                    'message': f'Buona distribuzione! Le interrogazioni sono ben bilanciate (media: {avg_count:.1f} per lezione)'
                })
            
            # Suggerimenti per carico eccessivo
            if max_count > 5:
                warnings.append({
                    'type': 'overload',
                    'message': f'Alcune lezioni hanno {max_count} interrogazioni, potrebbe essere eccessivo',
                    'suggestion': 'Considera di distribuire le interrogazioni su più lezioni per ridurre il carico'
                })
        
        return {
            'statistics': {
                'total_interrogations': sum(student_counts.values()),
                'lessons': len(calendario),
                'avg_per_lesson': avg_count if student_counts else 0,
                'max_per_lesson': max_count if student_counts else 0,
                'min_per_lesson': min_count if student_counts else 0
            },
            'suggestions': suggestions,
            'warnings': warnings
        }
    
    def suggest_optimal_distribution(self, num_students, num_lessons):
        """
        Suggerisce una distribuzione ottimale degli studenti
        
        Args:
            num_students (int): Numero totale di studenti
            num_lessons (int): Numero di lezioni
            
        Returns:
            dict: Suggerimento di distribuzione
        """
        # Calcola distribuzione ideale
        base_count = num_students // num_lessons
        remainder = num_students % num_lessons
        
        distribution = []
        for i in range(num_lessons):
            if i < remainder:
                distribution.append(base_count + 1)
            else:
                distribution.append(base_count)
        
        return {
            'suggested_distribution': distribution,
            'explanation': f'Distribuzione ottimale: {base_count} o {base_count + 1} studenti per lezione',
            'reasoning': 'Questa distribuzione minimizza il carico per lezione e mantiene l\'equilibrio'
        }
    
    def check_student_repetitions(self, calendario_attuale, calendario_precedente=None):
        """
        Controlla se ci sono ripetizioni di studenti
        
        Args:
            calendario_attuale (dict): Calendario corrente
            calendario_precedente (dict, optional): Calendario precedente per confronto
            
        Returns:
            dict: Analisi ripetizioni
        """
        all_students = []
        for studenti in calendario_attuale.values():
            all_students.extend([s['registro_num'] for s in studenti])
        
        # Conta occorrenze
        student_counter = Counter(all_students)
        duplicates = {k: v for k, v in student_counter.items() if v > 1}
        
        warnings = []
        if duplicates:
            for registro_num, count in duplicates.items():
                warnings.append({
                    'type': 'duplicate',
                    'message': f'Lo studente con registro {registro_num} appare {count} volte',
                    'suggestion': 'Rimuovi le duplicazioni per garantire equità'
                })
        
        return {
            'has_duplicates': len(duplicates) > 0,
            'duplicates': duplicates,
            'warnings': warnings,
            'unique_students': len(set(all_students)),
            'total_slots': len(all_students)
        }
    
    def suggest_best_days(self, num_lessons):
        """
        Suggerisce i giorni migliori per le interrogazioni
        
        Args:
            num_lessons (int): Numero di lezioni
            
        Returns:
            dict: Suggerimenti sui giorni
        """
        # Giorni della settimana con punteggi di "produttività"
        days_scores = {
            'Lunedì': 3,
            'Martedì': 5,
            'Mercoledì': 5,
            'Giovedì': 4,
            'Venerdì': 2,
            'Sabato': 1
        }
        
        suggestions = []
        
        if num_lessons <= 3:
            suggestions.append({
                'type': 'optimal_days',
                'message': 'Con poche lezioni settimanali, scegli giorni centrali (martedì-giovedì)',
                'reasoning': 'Gli studenti sono più concentrati a metà settimana'
            })
        else:
            suggestions.append({
                'type': 'spread_days',
                'message': 'Distribuisci le lezioni uniformemente nella settimana',
                'reasoning': 'Evita sovraccarichi in giorni consecutivi'
            })
        
        # Evita il lunedì e venerdì se possibile
        suggestions.append({
            'type': 'avoid_edges',
            'message': 'Se possibile, evita di programmare troppe interrogazioni il lunedì o venerdì',
            'reasoning': 'Inizio e fine settimana possono essere meno produttivi'
        })
        
        return {
            'suggestions': suggestions,
            'recommended_days': sorted(days_scores.items(), key=lambda x: x[1], reverse=True)[:num_lessons]
        }
    
    def generate_study_time_advice(self, calendario):
        """
        Genera consigli sui tempi di studio per gli studenti
        
        Args:
            calendario (dict): Calendario interrogazioni
            
        Returns:
            dict: Consigli sui tempi di studio
        """
        suggestions = []
        
        # Calcola giorni tra interrogazioni
        lesson_numbers = sorted(calendario.keys())
        
        if len(lesson_numbers) > 1:
            avg_gap = (lesson_numbers[-1] - lesson_numbers[0]) / (len(lesson_numbers) - 1)
            
            if avg_gap <= 1:
                suggestions.append({
                    'type': 'frequent_tests',
                    'message': 'Interrogazioni molto frequenti (ogni giorno o quasi)',
                    'advice': 'Gli studenti dovrebbero studiare costantemente per mantenere il ritmo'
                })
            elif avg_gap <= 3:
                suggestions.append({
                    'type': 'regular_tests',
                    'message': 'Cadenza regolare di interrogazioni',
                    'advice': 'Buon equilibrio: consiglia agli studenti di dedicare 2-3 giorni di studio'
                })
            else:
                suggestions.append({
                    'type': 'spaced_tests',
                    'message': 'Interrogazioni ben distanziate',
                    'advice': 'Gli studenti hanno tempo per preparazione approfondita (4+ giorni)'
                })
        
        return {
            'suggestions': suggestions,
            'general_advice': 'Consiglia agli studenti di rivedere il materiale ogni giorno anziché studiare tutto la sera prima'
        }
    
    def optimize_calendar(self, studenti, num_lezioni, preferenze=None):
        """
        Ottimizza la creazione del calendario con algoritmi intelligenti
        
        Args:
            studenti (list): Lista di studenti
            num_lezioni (int): Numero di lezioni
            preferenze (dict, optional): Preferenze utente
            
        Returns:
            dict: Calendario ottimizzato con spiegazione
        """
        if not studenti or num_lezioni <= 0:
            return {'error': 'Parametri non validi'}
        
        # Shuffle per casualità
        random.shuffle(studenti)
        
        # Calcola distribuzione ottimale
        optimal = self.suggest_optimal_distribution(len(studenti), num_lezioni)
        distribution = optimal['suggested_distribution']
        
        # Assegna studenti
        calendario = {}
        student_index = 0
        
        for lezione_num in range(1, num_lezioni + 1):
            num_students_this_lesson = distribution[lezione_num - 1]
            calendario[lezione_num] = studenti[student_index:student_index + num_students_this_lesson]
            student_index += num_students_this_lesson
        
        return {
            'calendario': calendario,
            'optimization_info': {
                'method': 'balanced_random',
                'reasoning': 'Distribuzione bilanciata con estrazione casuale',
                'benefits': [
                    'Carico equilibrato tra le lezioni',
                    'Nessuna ripetizione di studenti',
                    'Ordine casuale per equità'
                ]
            },
            'statistics': optimal
        }
    
    def get_general_advice(self):
        """
        Fornisce consigli generali sulla gestione delle interrogazioni
        
        Returns:
            dict: Consigli generali
        """
        advice = [
            {
                'category': 'Equità',
                'tip': 'Assicurati che ogni studente sia interrogato con la stessa frequenza nel semestre',
                'importance': 'alta'
            },
            {
                'category': 'Preparazione',
                'tip': 'Annuncia le interrogazioni programmate con almeno una settimana di anticipo',
                'importance': 'media'
            },
            {
                'category': 'Varietà',
                'tip': 'Varia gli argomenti delle interrogazioni per mantenere alto l\'interesse',
                'importance': 'media'
            },
            {
                'category': 'Feedback',
                'tip': 'Fornisci feedback immediato dopo ogni interrogazione per massimizzare l\'apprendimento',
                'importance': 'alta'
            },
            {
                'category': 'Flessibilità',
                'tip': 'Mantieni una piccola riserva di "slot" per interrogazioni di recupero',
                'importance': 'bassa'
            },
            {
                'category': 'Comunicazione',
                'tip': 'Comunica chiaramente i criteri di valutazione prima delle interrogazioni',
                'importance': 'alta'
            },
            {
                'category': 'Bilanciamento',
                'tip': 'Non programmare più di 4-5 interrogazioni per lezione per evitare sovraccarico',
                'importance': 'media'
            },
            {
                'category': 'Motivazione',
                'tip': 'Considera di includere interrogazioni "bonus" per argomenti particolarmente interessanti',
                'importance': 'bassa'
            }
        ]
        
        return {
            'advice': advice,
            'priority_tips': [tip for tip in advice if tip['importance'] == 'alta']
        }
    
    def evaluate_schedule_quality(self, calendario, studenti_totali):
        """
        Valuta la qualità complessiva del calendario
        
        Args:
            calendario (dict): Calendario interrogazioni
            studenti_totali (int): Numero totale studenti
            
        Returns:
            dict: Valutazione con punteggio
        """
        score = 100
        issues = []
        good_points = []
        
        # Analizza distribuzione
        distribution_analysis = self.analyze_distribution(calendario)
        
        # Controlla ripetizioni
        repetition_check = self.check_student_repetitions(calendario)
        
        if repetition_check['has_duplicates']:
            score -= 30
            issues.append('Presenti studenti duplicati')
        else:
            good_points.append('Nessuna duplicazione di studenti')
        
        # Controlla bilanciamento
        stats = distribution_analysis['statistics']
        if stats['max_per_lesson'] - stats['min_per_lesson'] > 2:
            score -= 20
            issues.append('Distribuzione sbilanciata tra le lezioni')
        else:
            good_points.append('Buon bilanciamento del carico')
        
        # Controlla copertura
        coverage = (stats['total_interrogations'] / studenti_totali * 100) if studenti_totali > 0 else 0
        if coverage < 80:
            score -= 15
            issues.append(f'Copertura bassa: solo {coverage:.0f}% degli studenti')
        elif coverage == 100:
            good_points.append('Copertura completa: tutti gli studenti inclusi')
        
        # Controlla sovraccarico
        if stats['max_per_lesson'] > 5:
            score -= 10
            issues.append('Alcune lezioni hanno troppe interrogazioni')
        
        # Determina giudizio
        if score >= 90:
            quality = 'Eccellente'
        elif score >= 75:
            quality = 'Buona'
        elif score >= 60:
            quality = 'Sufficiente'
        else:
            quality = 'Da migliorare'
        
        return {
            'score': max(0, score),
            'quality': quality,
            'issues': issues,
            'good_points': good_points,
            'recommendations': self._generate_recommendations(score, issues)
        }
    
    def _generate_recommendations(self, score, issues):
        """
        Genera raccomandazioni basate sul punteggio
        
        Args:
            score (int): Punteggio qualità
            issues (list): Lista problemi
            
        Returns:
            list: Lista raccomandazioni
        """
        recommendations = []
        
        if score < 70:
            recommendations.append('Considera di rigenerare il calendario per una migliore distribuzione')
        
        if 'duplicati' in ' '.join(issues).lower():
            recommendations.append('Rimuovi gli studenti duplicati usando la funzione di modifica')
        
        if 'sbilanciata' in ' '.join(issues).lower():
            recommendations.append('Usa la funzione "rimescola" per riequilibrare le interrogazioni')
        
        if 'copertura bassa' in ' '.join(issues).lower():
            recommendations.append('Aggiungi più slot di interrogazione o riduci il numero di lezioni')
        
        if not recommendations:
            recommendations.append('Il calendario è ottimale! Puoi procedere con il salvataggio')
        
        return recommendations
