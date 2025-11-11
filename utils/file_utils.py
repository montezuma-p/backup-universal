"""
Módulo de Utilitários de Arquivos
Funções utilitárias para operações com arquivos e diretórios
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Dict


def calculate_directory_size(path: Path, exclusion_filter=None) -> Tuple[int, int]:
    """
    Calcula o tamanho total de um diretório
    
    Args:
        path: Caminho do diretório
        exclusion_filter: Filtro de exclusão (opcional)
        
    Returns:
        Tupla (tamanho_total_bytes, total_arquivos)
    """
    total_size = 0
    total_files = 0
    
    for root, dirs, files in os.walk(path):
        # Remove diretórios excluídos se houver filtro
        if exclusion_filter:
            dirs[:] = [d for d in dirs if not exclusion_filter.should_exclude(d)]
        
        for arquivo in files:
            # Verifica exclusão de arquivo se houver filtro
            if exclusion_filter and exclusion_filter.should_exclude(arquivo):
                continue
                
            try:
                caminho_arquivo = Path(root) / arquivo
                total_size += caminho_arquivo.stat().st_size
                total_files += 1
            except (OSError, IOError):
                continue
                
    return total_size, total_files


def detect_directory_type(path: Path) -> str:
    """
    Detecta o tipo de diretório baseado em arquivos característicos
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Tipo do diretório (nodejs, python, java, git, generico)
    """
    if not path.exists() or not path.is_dir():
        return "generico"
    
    # Detecta tipo baseado em arquivos característicos
    if (path / "package.json").exists():
        return "nodejs"
    elif (path / "requirements.txt").exists() or (path / "setup.py").exists():
        return "python"
    elif (path / "pom.xml").exists():
        return "java"
    elif (path / ".git").exists():
        return "git"
    
    return "generico"


def get_directory_info(path: Path) -> Optional[Dict]:
    """
    Obtém informações sobre um diretório
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Dicionário com informações ou None se não existir
    """
    if not path.exists():
        return None
    
    try:
        stat_info = path.stat()
        return {
            "nome": path.name,
            "caminho": str(path.absolute()),
            "tipo": detect_directory_type(path),
            "ultima_modificacao": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "tamanho": stat_info.st_size if path.is_file() else None
        }
    except Exception:
        return None


def ensure_directory(path: Path) -> Path:
    """
    Garante que um diretório existe, criando se necessário
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Path do diretório
    """
    path = Path(path).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_file_remove(path: Path) -> bool:
    """
    Remove arquivo de forma segura, ignorando erros
    
    Args:
        path: Caminho do arquivo
        
    Returns:
        True se removido com sucesso, False caso contrário
    """
    try:
        if path.exists():
            path.unlink()
            return True
    except Exception:
        pass
    return False


def get_file_size(path: Path) -> int:
    """
    Obtém tamanho de arquivo em bytes
    
    Args:
        path: Caminho do arquivo
        
    Returns:
        Tamanho em bytes, ou 0 se arquivo não existir
    """
    try:
        return path.stat().st_size
    except (OSError, IOError):
        return 0
