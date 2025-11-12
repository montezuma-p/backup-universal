"""
Testes Unitários - Módulo de Índice
Testa o gerenciamento do índice JSON de backups
"""

import pytest
import json
import importlib.util
from pathlib import Path
from datetime import datetime

# Importa módulo diretamente do arquivo
spec = importlib.util.spec_from_file_location(
    "index",
    Path(__file__).parent.parent.parent / "storage" / "index.py"
)
index_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index_mod)

BackupIndex = index_mod.BackupIndex


class TestBackupIndexInit:
    """Testes de inicialização do BackupIndex"""
    
    def test_init_new_index(self, tmp_path):
        """Testa inicialização com arquivo inexistente"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        assert index.index_path == index_file
        assert index.get_all() == []
    
    def test_init_existing_index(self, tmp_path):
        """Testa inicialização com arquivo existente"""
        index_file = tmp_path / "index.json"
        
        # Cria arquivo de índice com dados
        test_data = [
            {"arquivo": "backup1.tar.gz", "nome_diretorio": "test"}
        ]
        index_file.write_text(json.dumps(test_data))
        
        index = BackupIndex(index_file)
        assert len(index.get_all()) == 1
        assert index.get_all()[0]["arquivo"] == "backup1.tar.gz"
    
    def test_init_corrupted_index(self, tmp_path):
        """Testa inicialização com arquivo JSON corrompido"""
        index_file = tmp_path / "index.json"
        index_file.write_text("{ invalid json }")
        
        # Deve inicializar vazio sem erro
        index = BackupIndex(index_file)
        assert index.get_all() == []


class TestAddBackup:
    """Testes para add_backup()"""
    
    def test_add_single_backup(self, tmp_path):
        """Testa adicionar um backup"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        backup_info = {
            "arquivo": "backup_test_20251112.tar.gz",
            "nome_diretorio": "test",
            "data_criacao": datetime.now().isoformat(),
            "tamanho_backup": 1024
        }
        
        index.add_backup(backup_info)
        
        assert len(index.get_all()) == 1
        assert index.get_all()[0]["arquivo"] == "backup_test_20251112.tar.gz"
    
    def test_add_multiple_backups(self, tmp_path):
        """Testa adicionar múltiplos backups"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        for i in range(3):
            backup_info = {
                "arquivo": f"backup_{i}.tar.gz",
                "nome_diretorio": "test",
                "tamanho_backup": 1024 * i
            }
            index.add_backup(backup_info)
        
        assert len(index.get_all()) == 3
    
    def test_add_backup_persists(self, tmp_path):
        """Testa que backup é salvo em disco"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        backup_info = {"arquivo": "test.tar.gz"}
        index.add_backup(backup_info)
        
        # Recarrega do arquivo
        index2 = BackupIndex(index_file)
        assert len(index2.get_all()) == 1


class TestRemoveBackup:
    """Testes para remove_backup()"""
    
    def test_remove_existing_backup(self, tmp_path):
        """Testa remover backup existente"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "backup1.tar.gz"})
        index.add_backup({"arquivo": "backup2.tar.gz"})
        
        result = index.remove_backup("backup1.tar.gz")
        
        assert result is True
        assert len(index.get_all()) == 1
        assert index.get_all()[0]["arquivo"] == "backup2.tar.gz"
    
    def test_remove_nonexistent_backup(self, tmp_path):
        """Testa remover backup inexistente"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "backup1.tar.gz"})
        
        result = index.remove_backup("nonexistent.tar.gz")
        
        assert result is False
        assert len(index.get_all()) == 1
    
    def test_remove_backup_persists(self, tmp_path):
        """Testa que remoção é salva em disco"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "backup1.tar.gz"})
        index.remove_backup("backup1.tar.gz")
        
        # Recarrega do arquivo
        index2 = BackupIndex(index_file)
        assert len(index2.get_all()) == 0


class TestGetByDirectory:
    """Testes para get_by_directory()"""
    
    def test_get_by_directory(self, tmp_path):
        """Testa buscar por diretório"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz", "nome_diretorio": "projeto1"})
        index.add_backup({"arquivo": "b2.tar.gz", "nome_diretorio": "projeto2"})
        index.add_backup({"arquivo": "b3.tar.gz", "nome_diretorio": "projeto1"})
        
        result = index.get_by_directory("projeto1")
        
        assert len(result) == 2
        assert all(b["nome_diretorio"] == "projeto1" for b in result)
    
    def test_get_by_directory_empty(self, tmp_path):
        """Testa buscar diretório sem backups"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        result = index.get_by_directory("nonexistent")
        assert result == []


class TestGetGroupedByDirectory:
    """Testes para get_grouped_by_directory()"""
    
    def test_grouped_by_directory(self, tmp_path):
        """Testa agrupamento por diretório"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz", "nome_diretorio": "proj1"})
        index.add_backup({"arquivo": "b2.tar.gz", "nome_diretorio": "proj2"})
        index.add_backup({"arquivo": "b3.tar.gz", "nome_diretorio": "proj1"})
        
        grouped = index.get_grouped_by_directory()
        
        assert len(grouped) == 2
        assert len(grouped["proj1"]) == 2
        assert len(grouped["proj2"]) == 1
    
    def test_grouped_empty_index(self, tmp_path):
        """Testa agrupamento com índice vazio"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        grouped = index.get_grouped_by_directory()
        assert grouped == {}
    
    def test_grouped_missing_directory_name(self, tmp_path):
        """Testa agrupamento com backups sem nome de diretório"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz"})  # Sem nome_diretorio
        
        grouped = index.get_grouped_by_directory()
        assert "desconhecido" in grouped


class TestGetSortedByDate:
    """Testes para get_sorted_by_date()"""
    
    def test_sort_descending(self, tmp_path):
        """Testa ordenação decrescente (mais recente primeiro)"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1", "data_criacao": "2025-11-10T10:00:00"})
        index.add_backup({"arquivo": "b2", "data_criacao": "2025-11-12T10:00:00"})
        index.add_backup({"arquivo": "b3", "data_criacao": "2025-11-11T10:00:00"})
        
        sorted_backups = index.get_sorted_by_date(reverse=True)
        
        assert sorted_backups[0]["arquivo"] == "b2"  # Mais recente
        assert sorted_backups[1]["arquivo"] == "b3"
        assert sorted_backups[2]["arquivo"] == "b1"  # Mais antigo
    
    def test_sort_ascending(self, tmp_path):
        """Testa ordenação crescente (mais antigo primeiro)"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1", "data_criacao": "2025-11-12T10:00:00"})
        index.add_backup({"arquivo": "b2", "data_criacao": "2025-11-10T10:00:00"})
        
        sorted_backups = index.get_sorted_by_date(reverse=False)
        
        assert sorted_backups[0]["arquivo"] == "b2"  # Mais antigo
        assert sorted_backups[1]["arquivo"] == "b1"  # Mais recente


class TestFindByHash:
    """Testes para find_by_hash()"""
    
    def test_find_existing_hash(self, tmp_path):
        """Testa encontrar backup por hash existente"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz", "hash_md5": "abc123"})
        index.add_backup({"arquivo": "b2.tar.gz", "hash_md5": "def456"})
        
        result = index.find_by_hash("abc123")
        
        assert result is not None
        assert result["arquivo"] == "b1.tar.gz"
    
    def test_find_nonexistent_hash(self, tmp_path):
        """Testa buscar hash inexistente"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz", "hash_md5": "abc123"})
        
        result = index.find_by_hash("nonexistent")
        assert result is None


class TestGetTotalSize:
    """Testes para get_total_size()"""
    
    def test_total_size(self, tmp_path):
        """Testa cálculo de tamanho total"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1", "tamanho_backup": 1024})
        index.add_backup({"arquivo": "b2", "tamanho_backup": 2048})
        index.add_backup({"arquivo": "b3", "tamanho_backup": 512})
        
        total = index.get_total_size()
        assert total == 3584  # 1024 + 2048 + 512
    
    def test_total_size_empty(self, tmp_path):
        """Testa tamanho total com índice vazio"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        assert index.get_total_size() == 0
    
    def test_total_size_missing_field(self, tmp_path):
        """Testa com backups sem campo tamanho_backup"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1"})  # Sem tamanho_backup
        index.add_backup({"arquivo": "b2", "tamanho_backup": 1024})
        
        total = index.get_total_size()
        assert total == 1024


class TestGetAll:
    """Testes para get_all()"""
    
    def test_get_all_returns_copy(self, tmp_path):
        """Testa que get_all() retorna uma cópia"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz"})
        
        backups = index.get_all()
        backups.append({"arquivo": "b2.tar.gz"})
        
        # Não deve afetar o índice original
        assert len(index.get_all()) == 1


class TestLoadAndSave:
    """Testes para load() e save()"""
    
    def test_save_creates_directory(self, tmp_path):
        """Testa que save() cria diretório se não existir"""
        index_file = tmp_path / "nested" / "dir" / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "test.tar.gz"})
        
        assert index_file.exists()
        assert index_file.parent.exists()
    
    def test_reload_preserves_data(self, tmp_path):
        """Testa que reload() preserva dados"""
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        index.add_backup({"arquivo": "b1.tar.gz", "tamanho_backup": 1024})
        
        # Recarrega
        index.load()
        
        backups = index.get_all()
        assert len(backups) == 1
        assert backups[0]["arquivo"] == "b1.tar.gz"
