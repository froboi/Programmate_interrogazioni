"""
Utility functions per l'applicazione
Funzioni helper generiche utilizzabili in tutta l'applicazione
"""

import random
import string
from datetime import datetime, date
import json
import csv
from typing import List, Dict, Any, Optional


def generate_random_string(length: int = 32) -> str:
    """
    Genera una stringa casuale
    
    Args:
        length (int): Lunghezza della stringa
        
    Returns:
        str: Stringa casuale
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def validate_email(email: str) -> bool:
    """
    Valida un indirizzo email (base)
    
    Args:
        email (str): Email da validare
        
    Returns:
        bool: True se valida
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def format_datetime(dt: datetime, format_str: str = '%d/%m/%Y %H:%M') -> str:
    """
    Formatta un datetime in stringa
    
    Args:
        dt (datetime): Oggetto datetime
        format_str (str): Formato output
        
    Returns:
        str: Data formattata
    """
    if not dt:
        return ''
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = '%Y-%m-%d') -> Optional[date]:
    """
    Parsifica una stringa in date
    
    Args:
        date_str (str): Stringa data
        format_str (str): Formato input
        
    Returns:
        date: Oggetto date o None
    """
    try:
        return datetime.strptime(date_str, format_str).date()
    except:
        return None


def sanitize_filename(filename: str) -> str:
    """
    Sanitizza un nome file rimuovendo caratteri pericolosi
    
    Args:
        filename (str): Nome file originale
        
    Returns:
        str: Nome file sicuro
    """
    # Rimuovi caratteri non permessi
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized = ''.join(c for c in filename if c in valid_chars)
    
    # Limita lunghezza
    return sanitized[:255]


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divide una lista in chunk di dimensione specificata
    
    Args:
        lst (List): Lista da dividere
        chunk_size (int): Dimensione di ogni chunk
        
    Returns:
        List[List]: Lista di chunk
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Appiattisce una lista nested
    
    Args:
        nested_list (List[List]): Lista nested
        
    Returns:
        List: Lista appiattita
    """
    return [item for sublist in nested_list for item in sublist]


def dict_to_csv_string(data: List[Dict], fieldnames: Optional[List[str]] = None) -> str:
    """
    Converte una lista di dizionari in stringa CSV
    
    Args:
        data (List[Dict]): Dati da convertire
        fieldnames (List[str], optional): Nomi campi
        
    Returns:
        str: Stringa CSV
    """
    if not data:
        return ''
    
    if not fieldnames:
        fieldnames = list(data[0].keys())
    
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue()


def calculate_percentage(part: float, total: float) -> float:
    """
    Calcola una percentuale
    
    Args:
        part (float): Parte
        total (float): Totale
        
    Returns:
        float: Percentuale (0-100)
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def shuffle_preserving_length(items: List[Any]) -> List[Any]:
    """
    Mescola una lista preservando la lunghezza
    
    Args:
        items (List): Lista da mescolare
        
    Returns:
        List: Lista mescolata
    """
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled


def remove_duplicates_preserve_order(items: List[Any]) -> List[Any]:
    """
    Rimuove duplicati preservando l'ordine
    
    Args:
        items (List): Lista con possibili duplicati
        
    Returns:
        List: Lista senza duplicati
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Unisce più dizionari
    
    Args:
        *dicts: Dizionari da unire
        
    Returns:
        Dict: Dizionario unito
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def safe_int(value: Any, default: int = 0) -> int:
    """
    Converte un valore in int in modo sicuro
    
    Args:
        value (Any): Valore da convertire
        default (int): Valore di default
        
    Returns:
        int: Valore convertito
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Converte un valore in float in modo sicuro
    
    Args:
        value (Any): Valore da convertire
        default (float): Valore di default
        
    Returns:
        float: Valore convertito
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def is_valid_json(json_str: str) -> bool:
    """
    Verifica se una stringa è JSON valido
    
    Args:
        json_str (str): Stringa da verificare
        
    Returns:
        bool: True se valido
    """
    try:
        json.loads(json_str)
        return True
    except:
        return False


def truncate_string(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """
    Tronca una stringa a lunghezza massima
    
    Args:
        text (str): Testo da troncare
        max_length (int): Lunghezza massima
        suffix (str): Suffisso da aggiungere
        
    Returns:
        str: Testo troncato
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_file_extension(filename: str) -> str:
    """
    Estrae l'estensione da un filename
    
    Args:
        filename (str): Nome file
        
    Returns:
        str: Estensione (senza punto)
    """
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def bytes_to_human_readable(bytes_size: int) -> str:
    """
    Converte bytes in formato leggibile
    
    Args:
        bytes_size (int): Dimensione in bytes
        
    Returns:
        str: Dimensione formattata
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def get_current_timestamp() -> str:
    """
    Ottiene timestamp corrente formattato
    
    Returns:
        str: Timestamp ISO format
    """
    return datetime.now().isoformat()


def get_date_range(start_date: date, end_date: date) -> List[date]:
    """
    Genera una lista di date tra start e end
    
    Args:
        start_date (date): Data inizio
        end_date (date): Data fine
        
    Returns:
        List[date]: Lista di date
    """
    from datetime import timedelta
    
    date_list = []
    current_date = start_date
    
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    
    return date_list


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge profondo di due dizionari
    
    Args:
        dict1 (Dict): Primo dizionario
        dict2 (Dict): Secondo dizionario
        
    Returns:
        Dict: Dizionario merged
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


# Export funzioni principali
__all__ = [
    'generate_random_string',
    'validate_email',
    'format_datetime',
    'parse_date',
    'sanitize_filename',
    'chunk_list',
    'flatten_list',
    'dict_to_csv_string',
    'calculate_percentage',
    'shuffle_preserving_length',
    'remove_duplicates_preserve_order',
    'merge_dicts',
    'safe_int',
    'safe_float',
    'is_valid_json',
    'truncate_string',
    'get_file_extension',
    'bytes_to_human_readable',
    'get_current_timestamp',
    'get_date_range',
    'deep_merge_dicts'
]
