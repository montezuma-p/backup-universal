"""
Backup Universal - Sistema modular de backup
Versão 1.1 - Modularizada com config.json

Sistema completo de backup com:
- Compressão em múltiplos formatos (tar.gz, zip)
- Exclusões inteligentes
- Gerenciamento de índice
- Restauração interativa
- Limpeza automática
"""

__version__ = "1.1.0"
__author__ = "Pedro Montezuma"
__license__ = "MIT"

from .config import Config
from .core import BackupManager, ExclusionFilter, IntegrityChecker
from .storage import BackupIndex, CleanupManager
from .restore import RestoreManager

__all__ = [
    'Config',
    'BackupManager',
    'ExclusionFilter',
    'IntegrityChecker',
    'BackupIndex',
    'CleanupManager',
    'RestoreManager'
]
