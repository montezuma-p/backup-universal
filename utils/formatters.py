"""
Módulo de Formatadores
Funções utilitárias para formatação de dados (tamanhos, datas, etc)
"""

from datetime import datetime
from typing import Union


def format_bytes(bytes_size: Union[int, float]) -> str:
    """
    Formata tamanho em bytes para formato legível
    
    Args:
        bytes_size: Tamanho em bytes
        
    Returns:
        String formatada (ex: "45.2 MB")
    """
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unidade}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def format_date(date: datetime, format_string: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Formata data para string
    
    Args:
        date: Objeto datetime
        format_string: Formato desejado
        
    Returns:
        String formatada
    """
    return date.strftime(format_string)


def format_compression_rate(original_size: int, compressed_size: int) -> float:
    """
    Calcula taxa de compressão em percentual
    
    Args:
        original_size: Tamanho original em bytes
        compressed_size: Tamanho comprimido em bytes
        
    Returns:
        Taxa de compressão (0-100)
    """
    if original_size == 0:
        return 0.0
    return ((original_size - compressed_size) / original_size) * 100


def format_progress(current: int, total: int) -> str:
    """
    Formata progresso como string de percentual
    
    Args:
        current: Valor atual
        total: Valor total
        
    Returns:
        String formatada (ex: "45.2%")
    """
    if total == 0:
        return "0.0%"
    percentage = (current / total) * 100
    return f"{percentage:.1f}%"


def format_number(number: int) -> str:
    """
    Formata número com separadores de milhar
    
    Args:
        number: Número inteiro
        
    Returns:
        String formatada (ex: "1,234,567")
    """
    return f"{number:,}"


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca string se exceder tamanho máximo
    
    Args:
        text: Texto a truncar
        max_length: Tamanho máximo
        suffix: Sufixo para indicar truncamento
        
    Returns:
        String truncada
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
