"""Testes unitários para RestoreManager
"""
from pathlib import Path
import os
import pytest

from backup.restore.restore_manager import RestoreManager


class FakeIndexEmpty:
    def get_all(self):
        return []

    def get_grouped_by_directory(self):
        return {}

    def get_sorted_by_date(self, reverse=True):
        return []


class FakeIndexGrouped:
    def __init__(self, backups):
        self._backups = backups

    def get_all(self):
        return list(self._backups)

    def get_grouped_by_directory(self):
        grouped = {}
        for b in self._backups:
            grouped.setdefault(b['nome_diretorio'], []).append(b)
        return grouped

    def get_sorted_by_date(self, reverse=True):
        return sorted(self._backups, key=lambda x: x['data_criacao'], reverse=reverse)


def test_list_available_backups_empty(capsys, tmp_path):
    idx = FakeIndexEmpty()
    rm = RestoreManager(idx, tmp_path)
    rm.list_available_backups()
    out = capsys.readouterr().out
    assert 'Nenhum backup encontrado' in out


def test_list_available_backups_grouped(capsys, tmp_path):
    b1 = {
        'arquivo': 'b1.tar.gz',
        'nome_diretorio': 'proj',
        'data_criacao': '2025-11-12T10:00:00',
        'tamanho_backup': 1000,
        'taxa_compressao': 50.0,
        'diretorio_origem': '/tmp/proj',
        'tipo_diretorio': 'generico'
    }
    b2 = {
        'arquivo': 'b2.tar.gz',
        'nome_diretorio': 'proj',
        'data_criacao': '2025-11-11T10:00:00',
        'tamanho_backup': 800,
        'taxa_compressao': 40.0,
        'diretorio_origem': '/tmp/proj',
        'tipo_diretorio': 'generico'
    }

    idx = FakeIndexGrouped([b1, b2])
    rm = RestoreManager(idx, tmp_path)
    rm.list_available_backups()
    out = capsys.readouterr().out
    assert 'proj' in out
    assert 'b1.tar.gz' in out and 'b2.tar.gz' in out
    assert 'Total' in out


def test_restore_by_name_not_in_index(tmp_path, capsys):
    idx = FakeIndexEmpty()
    rm = RestoreManager(idx, tmp_path)
    res = rm.restore_by_name('nope.tar.gz', tmp_path)
    out = capsys.readouterr().out
    assert res is False
    assert 'não encontrado no índice' in out


def test_restore_by_name_file_missing(tmp_path, capsys):
    b = {
        'arquivo': 'missing.tar.gz',
        'nome_diretorio': 'proj',
        'data_criacao': '2025-11-12T10:00:00',
        'tamanho_backup': 1000,
        'taxa_compressao': 50.0,
        'diretorio_origem': '/tmp/proj',
        'tipo_diretorio': 'generico'
    }
    class Idx:
        def get_all(self):
            return [b]

    idx = Idx()
    rm = RestoreManager(idx, tmp_path)
    res = rm.restore_by_name('missing.tar.gz', tmp_path)
    out = capsys.readouterr().out
    assert res is False
    assert 'Arquivo não encontrado' in out


def test_restore_by_name_success(tmp_path, monkeypatch, capsys):
    b = {
        'arquivo': 'ok.tar.gz',
        'nome_diretorio': 'proj',
        'data_criacao': '2025-11-12T10:00:00',
        'tamanho_backup': 1000,
        'taxa_compressao': 50.0,
        'diretorio_origem': '/tmp/proj',
        'tipo_diretorio': 'generico',
        'total_arquivos': 1
    }

    class Idx:
        def get_all(self):
            return [b]

    idx = Idx()
    # create backup file
    (tmp_path / 'ok.tar.gz').write_bytes(b'0' * 10)

    # fake compressor
    class FakeComp:
        def decompress(self, archive, dest):
            # simulate extraction by creating destination file
            (dest / 'restored.txt').write_text('ok')

    monkeypatch.setattr('backup.restore.restore_manager.get_compressor', lambda fmt: FakeComp())

    rm = RestoreManager(idx, tmp_path)
    dest = tmp_path / 'outdir'
    res = rm.restore_by_name('ok.tar.gz', dest)
    out = capsys.readouterr().out
    assert res is True
    assert 'Backup restaurado com sucesso' in out
    # compressor.decompress is called with destination.parent inside restore_backup
    assert (tmp_path / 'restored.txt').exists()


def test_verify_backup_integrity(tmp_path, monkeypatch, capsys):
    b = {
        'arquivo': 'check.tar.gz',
        'nome_diretorio': 'proj',
        'data_criacao': '2025-11-12T10:00:00',
        'tamanho_backup': 1000,
        'taxa_compressao': 50.0,
        'diretorio_origem': '/tmp/proj',
        'tipo_diretorio': 'generico',
        'hash_md5': 'abc123'
    }

    class Idx:
        def get_all(self):
            return [b]

    idx = Idx()
    (tmp_path / 'check.tar.gz').write_bytes(b'0' * 10)

    class FakeIntegrity:
        @staticmethod
        def calculate_md5(path):
            return 'abc123'

    # verify_backup_integrity imports IntegrityChecker from backup.core.integrity inside the method,
    # so patch the class on that module.
    monkeypatch.setattr('backup.core.integrity.IntegrityChecker', FakeIntegrity)

    rm = RestoreManager(idx, tmp_path)
    res = rm.verify_backup_integrity('check.tar.gz')
    out = capsys.readouterr().out
    assert res is True
    assert 'Backup íntegro' in out

    # now test corrupted
    class FakeIntegrity2:
        @staticmethod
        def calculate_md5(path):
            return 'dead'

    monkeypatch.setattr('backup.core.integrity.IntegrityChecker', FakeIntegrity2)
    res2 = rm.verify_backup_integrity('check.tar.gz')
    out2 = capsys.readouterr().out
    assert res2 is False
    assert 'Backup corrompido' in out2
