"""Testes unitários para BackupManager

Cobertura alvo: inicialização, adição de exclusões, erro quando origem ausente, fluxo feliz com compressor mockado.
"""
from pathlib import Path
import os
import tempfile
import types
import pytest

from backup.core.backup_manager import BackupManager, BackupStats


class DummyConfig:
    def __init__(self, tmp_path):
        self.index_file = tmp_path / "index.json"
        self.all_exclusion_patterns = []
        self.default_backup_source = tmp_path / "source"
        self.default_format = "tar"
        self.default_compression_level = 6
        self.backup_destination = tmp_path / "backups"
        self.custom_exclusion_patterns = []

    def add_custom_pattern(self, pattern):
        self.custom_exclusion_patterns.append(pattern)

    def set(self, section, data):
        # simplificado para testes
        if section == 'compression':
            self.default_format = data.get('default_format', self.default_format)
            self.default_compression_level = data.get('default_level', self.default_compression_level)


def test_init_sets_index_and_exclusion(tmp_path, monkeypatch):
    # Prepara
    cfg = DummyConfig(tmp_path)

    # Substitui BackupIndex por um mock simples que não toca o FS
    class FakeIndex:
        def __init__(self, path):
            self.path = path
        def add_backup(self, info):
            self.last = info

    monkeypatch.setattr('backup.core.backup_manager.BackupIndex', FakeIndex)

    bm = BackupManager(cfg)
    assert isinstance(bm.index, FakeIndex)
    assert isinstance(bm.exclusion_filter, __import__('backup.core').core.exclusion.ExclusionFilter)
    assert isinstance(bm.stats, BackupStats)


def test_add_custom_exclusions_updates_config_and_filter(tmp_path, monkeypatch):
    cfg = DummyConfig(tmp_path)
    monkeypatch.setattr('backup.core.backup_manager.BackupIndex', lambda p: object())

    bm = BackupManager(cfg)
    bm.add_custom_exclusion('*.tmp')
    assert '*.tmp' in cfg.custom_exclusion_patterns


def test_create_backup_fails_when_source_missing(tmp_path, monkeypatch):
    cfg = DummyConfig(tmp_path)
    # source não existe
    if cfg.default_backup_source.exists():
        os.rmdir(cfg.default_backup_source)

    monkeypatch.setattr('backup.core.backup_manager.BackupIndex', lambda p: object())

    bm = BackupManager(cfg)
    result = bm.create_backup(silent=True)
    assert result is False


def test_create_backup_happy_path(tmp_path, monkeypatch):
    # Monta estrutura de diretório
    src = tmp_path / 'source'
    src.mkdir()
    (src / 'a.txt').write_text('hello')

    dest = tmp_path / 'backups'
    dest.mkdir()

    cfg = DummyConfig(tmp_path)
    cfg.default_backup_source = src
    cfg.backup_destination = dest
    cfg.default_format = 'tar'
    cfg.default_compression_level = 5

    # Fake Index para capturar add_backup
    class FakeIndex:
        def __init__(self, path):
            self.added = []
        def add_backup(self, info):
            self.added.append(info)
        def get_all(self):
            return self.added

    monkeypatch.setattr('backup.core.backup_manager.BackupIndex', FakeIndex)

    # Mock get_directory_info e calculate_directory_size
    monkeypatch.setattr('backup.core.backup_manager.get_directory_info', lambda p: {'nome': 'source', 'tipo': 'generico'})
    monkeypatch.setattr('backup.core.backup_manager.calculate_directory_size', lambda p, f: (1234, 1))

    # Mock compressor: cria o arquivo quando compress é chamado
    class FakeCompressor:
        extension = '.tar.gz'
        def compress(self, source, dest, exclusion_filter, progress_callback=None, compression_level=None):
            # cria arquivo de tamanho 512
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, 'wb') as fh:
                fh.write(b"0" * 512)
            return (1, 0, 0)

    monkeypatch.setattr('backup.core.backup_manager.get_compressor', lambda fmt: FakeCompressor())

    # Mock IntegrityChecker
    class FakeIntegrity:
        @staticmethod
        def calculate_md5(path):
            return 'deadbeef'

    monkeypatch.setattr('backup.core.backup_manager.IntegrityChecker', FakeIntegrity)

    bm = BackupManager(cfg)
    res = bm.create_backup(silent=True)
    assert res is True
    # verifica que index recebeu algo
    assert len(bm.index.added) == 1
    info = bm.index.added[0]
    assert info['arquivo'].endswith('.tar.gz')
    assert info['tamanho_backup'] == 512
