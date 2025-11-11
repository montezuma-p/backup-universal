"""
Core - Módulos principais do sistema de backup
"""

from .exclusion import ExclusionFilter
from .integrity import IntegrityChecker
from .compression import Compressor, TarCompressor, ZipCompressor, get_compressor
from .backup_manager import BackupManager, BackupStats

__all__ = [
    'ExclusionFilter',
    'IntegrityChecker',
    'Compressor',
    'TarCompressor',
    'ZipCompressor',
    'get_compressor',
    'BackupManager',
    'BackupStats'
]
