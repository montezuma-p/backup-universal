"""
Core - Módulos principais do sistema de backup
"""

from backup.core.exclusion import ExclusionFilter
from backup.core.integrity import IntegrityChecker
from backup.core.compression import Compressor, TarCompressor, ZipCompressor, get_compressor
from backup.core.backup_manager import BackupManager, BackupStats

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
