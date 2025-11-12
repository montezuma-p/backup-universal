"""
Testes Unitários - Módulo de Limpeza
Testa políticas de retenção e limpeza de backups antigos
"""

import pytest
import json
import sys
import importlib.util
from pathlib import Path
from datetime import datetime, timedelta


# Função para importar módulos diretamente, pulando __init__.py
def load_module_direct(module_name, filepath):
    """Carrega módulo diretamente do arquivo, pulando __init__.py"""
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        # Configurar __package__ para resolver imports relativos
        module.__package__ = module_name.rsplit('.', 1)[0] if '.' in module_name else ''
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Não foi possível carregar {module_name} de {filepath}")


# Obter diretório raiz do projeto  
project_root = Path(__file__).parent.parent.parent

# Adicionar raiz ao sys.path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Criar pacotes vazios para resolver imports relativos
if 'utils' not in sys.modules:
    utils_pkg = importlib.util.module_from_spec(
        importlib.util.spec_from_file_location('utils', project_root / 'utils' / '__init__.py')
    )
    utils_pkg.__path__ = [str(project_root / 'utils')]
    utils_pkg.__package__ = 'utils'
    sys.modules['utils'] = utils_pkg

if 'storage' not in sys.modules:
    storage_pkg = importlib.util.module_from_spec(
        importlib.util.spec_from_file_location('storage', project_root / 'storage' / '__init__.py')
    )
    storage_pkg.__path__ = [str(project_root / 'storage')]
    storage_pkg.__package__ = 'storage'
    sys.modules['storage'] = storage_pkg

# Importar formatters
formatters = load_module_direct('utils.formatters', project_root / 'utils' / 'formatters.py')
sys.modules['utils'].formatters = formatters

# Importar index
index_mod = load_module_direct('storage.index', project_root / 'storage' / 'index.py')
sys.modules['storage'].index = index_mod
BackupIndex = index_mod.BackupIndex

# Importar cleanup
cleanup_mod = load_module_direct('storage.cleanup', project_root / 'storage' / 'cleanup.py')
sys.modules['storage'].cleanup = cleanup_mod
CleanupManager = cleanup_mod.CleanupManager

import pytest
import json
import sys
import importlib.util
from pathlib import Path
from datetime import datetime, timedelta


def import_module_from_file(module_name: str, file_path: Path):
    """Importa um módulo Python de um arquivo específico."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Obter diretório raiz do projeto
project_root = Path(__file__).parent.parent.parent

# Importar dependências primeiro
formatters_module = import_module_from_file('formatters', project_root / 'utils' / 'formatters.py')
index_module = import_module_from_file('index', project_root / 'storage' / 'index.py')

# Injetar as dependências no sys.modules para resolver imports relativos
sys.modules['utils'] = type(sys)('utils')
sys.modules['utils'].formatters = formatters_module
sys.modules['storage'] = type(sys)('storage')
sys.modules['storage'].index = index_module

# Agora importar cleanup
cleanup_module = import_module_from_file('cleanup', project_root / 'storage' / 'cleanup.py')

CleanupManager = cleanup_module.CleanupManager
BackupIndex = index_module.BackupIndex


@pytest.fixture
def backup_dir(tmp_path):
    """Cria diretório temporário para backups"""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    return backup_dir


@pytest.fixture
def index_with_backups(backup_dir):
    """Cria índice com backups de teste"""
    index_file = backup_dir / "index.json"
    index = BackupIndex(index_file)
    
    # Adiciona backups de diferentes datas
    now = datetime.now()
    
    # Projeto 1 - 5 backups (últimos 50 dias)
    for i in range(5):
        days_ago = i * 10
        date = now - timedelta(days=days_ago)
        
        filename = f"backup_proj1_{i}.tar.gz"
        
        # Cria arquivo físico
        file_path = backup_dir / filename
        file_path.write_text("x" * (1024 * (i + 1)))  # Tamanhos diferentes
        
        index.add_backup({
            "arquivo": filename,
            "nome_diretorio": "projeto1",
            "data_criacao": date.isoformat(),
            "tamanho_backup": file_path.stat().st_size
        })
    
    # Projeto 2 - 3 backups (últimos 20 dias)
    for i in range(3):
        days_ago = i * 10
        date = now - timedelta(days=days_ago)
        
        filename = f"backup_proj2_{i}.tar.gz"
        file_path = backup_dir / filename
        file_path.write_text("y" * (2048 * (i + 1)))
        
        index.add_backup({
            "arquivo": filename,
            "nome_diretorio": "projeto2",
            "data_criacao": date.isoformat(),
            "tamanho_backup": file_path.stat().st_size
        })
    
    return index


class TestCleanupManagerInit:
    """Testes de inicialização do CleanupManager"""
    
    def test_init(self, backup_dir):
        """Testa inicialização básica"""
        index_file = backup_dir / "index.json"
        index = BackupIndex(index_file)
        
        manager = CleanupManager(index, backup_dir)
        
        assert manager.index == index
        assert manager.backup_dir == backup_dir


class TestCleanupOldBackups:
    """Testes para cleanup_old_backups()"""
    
    def test_cleanup_by_max_per_directory(self, backup_dir, index_with_backups, capsys):
        """Testa limpeza por limite de backups por diretório"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Mantém apenas 3 backups por diretório
        result = manager.cleanup_old_backups(days_to_keep=365, max_per_directory=3)
        
        # Projeto 1 tinha 5, deve remover 2
        # Projeto 2 tinha 3, não remove nenhum
        assert result['removed_count'] == 2
        assert result['kept_count'] == 6
        
        # Verifica que os mais antigos foram removidos
        proj1_backups = index_with_backups.get_by_directory("projeto1")
        assert len(proj1_backups) == 3
    
    def test_cleanup_by_days(self, backup_dir, index_with_backups):
        """Testa limpeza por idade dos backups"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Mantém apenas últimos 15 dias
        result = manager.cleanup_old_backups(days_to_keep=15, max_per_directory=10)
        
        # Deve remover backups mais antigos que 15 dias
        assert result['removed_count'] > 0
        assert result['kept_count'] < 8
    
    def test_cleanup_empty_index(self, backup_dir, capsys):
        """Testa limpeza com índice vazio"""
        index_file = backup_dir / "index.json"
        index = BackupIndex(index_file)
        manager = CleanupManager(index, backup_dir)
        
        result = manager.cleanup_old_backups()
        
        assert result['removed_count'] == 0
        assert result['freed_space'] == 0
        assert result['kept_count'] == 0
        
        captured = capsys.readouterr()
        assert "Nenhum backup para limpar" in captured.out
    
    def test_cleanup_removes_files(self, backup_dir, index_with_backups):
        """Testa que arquivos físicos são removidos"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Conta arquivos antes
        files_before = list(backup_dir.glob("*.tar.gz"))
        
        manager.cleanup_old_backups(days_to_keep=5, max_per_directory=2)
        
        # Conta arquivos depois
        files_after = list(backup_dir.glob("*.tar.gz"))
        
        assert len(files_after) < len(files_before)
    
    def test_cleanup_updates_index(self, backup_dir, index_with_backups):
        """Testa que índice é atualizado após limpeza"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        initial_count = len(index_with_backups.get_all())
        
        result = manager.cleanup_old_backups(days_to_keep=15, max_per_directory=2)
        
        final_count = len(index_with_backups.get_all())
        
        assert final_count == initial_count - result['removed_count']
    
    def test_cleanup_calculates_freed_space(self, backup_dir, index_with_backups):
        """Testa cálculo de espaço liberado"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        result = manager.cleanup_old_backups(days_to_keep=5, max_per_directory=1)
        
        # Deve ter liberado algum espaço
        assert result['freed_space'] > 0
    
    def test_cleanup_missing_file_warning(self, backup_dir, index_with_backups, capsys):
        """Testa warning quando arquivo físico não existe"""
        # Remove um arquivo físico mas mantém no índice
        file_to_remove = backup_dir / "backup_proj1_4.tar.gz"
        if file_to_remove.exists():
            file_to_remove.unlink()
        
        manager = CleanupManager(index_with_backups, backup_dir)
        manager.cleanup_old_backups(days_to_keep=5, max_per_directory=1)
        
        captured = capsys.readouterr()
        assert "não encontrado" in captured.out


class TestCleanupBySize:
    """Testes para cleanup_by_size()"""
    
    def test_cleanup_within_limit(self, backup_dir, index_with_backups, capsys):
        """Testa quando tamanho está dentro do limite"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Limite muito alto
        result = manager.cleanup_by_size(max_total_size_gb=100)
        
        assert result['removed_count'] == 0
        assert result['freed_space'] == 0
        
        captured = capsys.readouterr()
        assert "está dentro do limite" in captured.out
    
    def test_cleanup_exceeds_limit(self, backup_dir, index_with_backups):
        """Testa quando tamanho excede o limite"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Limite muito baixo (força limpeza)
        # 0.00001 GB = ~10 KB
        result = manager.cleanup_by_size(max_total_size_gb=0.00001)
        
        # Deve remover alguns backups
        assert result['removed_count'] > 0
        assert result['freed_space'] > 0
    
    def test_cleanup_removes_oldest_first(self, backup_dir, index_with_backups):
        """Testa que remove os mais antigos primeiro"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Limite baixo para forçar remoções
        manager.cleanup_by_size(max_total_size_gb=0.00001)
        
        # Os backups restantes devem ser os mais recentes
        remaining = index_with_backups.get_sorted_by_date(reverse=True)
        
        if len(remaining) > 1:
            # Primeiro deve ser mais recente que o último
            first_date = datetime.fromisoformat(remaining[0]['data_criacao'])
            last_date = datetime.fromisoformat(remaining[-1]['data_criacao'])
            assert first_date > last_date
    
    def test_cleanup_stops_when_limit_reached(self, backup_dir, index_with_backups):
        """Testa que para de remover quando atinge o limite"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        initial_size = index_with_backups.get_total_size()
        limit_gb = (initial_size / 2) / (1024 * 1024 * 1024)  # Metade do tamanho atual
        
        manager.cleanup_by_size(max_total_size_gb=limit_gb)
        
        final_size = index_with_backups.get_total_size()
        limit_bytes = limit_gb * 1024 * 1024 * 1024
        
        # Deve estar no limite ou abaixo
        assert final_size <= limit_bytes * 1.1  # 10% de tolerância


class TestRemoveOrphanedFiles:
    """Testes para remove_orphaned_files()"""
    
    def test_no_orphaned_files(self, backup_dir, index_with_backups, capsys):
        """Testa quando não há arquivos órfãos"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        count = manager.remove_orphaned_files()
        
        assert count == 0
        
        captured = capsys.readouterr()
        assert "Nenhum arquivo órfão encontrado" in captured.out
    
    def test_remove_orphaned_files(self, backup_dir, index_with_backups, capsys):
        """Testa remoção de arquivos órfãos"""
        # Cria arquivo órfão (não está no índice)
        orphan = backup_dir / "orphaned_backup.tar.gz"
        orphan.write_text("orphaned content")
        
        manager = CleanupManager(index_with_backups, backup_dir)
        count = manager.remove_orphaned_files()
        
        assert count == 1
        assert not orphan.exists()
        
        captured = capsys.readouterr()
        assert "orphaned_backup.tar.gz" in captured.out
    
    def test_remove_multiple_orphaned_files(self, backup_dir, index_with_backups):
        """Testa remoção de múltiplos arquivos órfãos"""
        # Cria vários órfãos
        orphans = []
        for i in range(3):
            orphan = backup_dir / f"orphan_{i}.tar.gz"
            orphan.write_text(f"orphan {i}")
            orphans.append(orphan)
        
        manager = CleanupManager(index_with_backups, backup_dir)
        count = manager.remove_orphaned_files()
        
        assert count == 3
        for orphan in orphans:
            assert not orphan.exists()
    
    def test_keeps_indexed_files(self, backup_dir, index_with_backups):
        """Testa que mantém arquivos que estão no índice"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Pega arquivos indexados antes
        indexed_files = [backup_dir / b['arquivo'] for b in index_with_backups.get_all()]
        
        manager.remove_orphaned_files()
        
        # Todos os arquivos indexados devem ainda existir
        for file_path in indexed_files:
            assert file_path.exists()
    
    def test_nonexistent_backup_dir(self, tmp_path, capsys):
        """Testa com diretório de backups inexistente"""
        nonexistent_dir = tmp_path / "nonexistent"
        index_file = tmp_path / "index.json"
        index = BackupIndex(index_file)
        
        manager = CleanupManager(index, nonexistent_dir)
        count = manager.remove_orphaned_files()
        
        assert count == 0
        
        captured = capsys.readouterr()
        assert "não encontrado" in captured.out
    
    def test_handles_zip_files(self, backup_dir, index_with_backups):
        """Testa que remove arquivos .zip órfãos também"""
        orphan_zip = backup_dir / "orphan.zip"
        orphan_zip.write_text("orphaned zip")
        
        manager = CleanupManager(index_with_backups, backup_dir)
        count = manager.remove_orphaned_files()
        
        assert count == 1
        assert not orphan_zip.exists()


class TestIntegration:
    """Testes de integração entre diferentes métodos de limpeza"""
    
    def test_sequential_cleanups(self, backup_dir, index_with_backups):
        """Testa múltiplas limpezas sequenciais"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Primeira limpeza por dias
        result1 = manager.cleanup_old_backups(days_to_keep=25, max_per_directory=10)
        count_after_first = len(index_with_backups.get_all())
        
        # Segunda limpeza por quantidade
        result2 = manager.cleanup_old_backups(days_to_keep=365, max_per_directory=2)
        count_after_second = len(index_with_backups.get_all())
        
        assert count_after_second <= count_after_first
    
    def test_cleanup_then_remove_orphans(self, backup_dir, index_with_backups):
        """Testa limpar backups e depois remover órfãos"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        # Limpeza normal
        manager.cleanup_old_backups(days_to_keep=5, max_per_directory=1)
        
        # Adiciona órfão
        orphan = backup_dir / "orphan.tar.gz"
        orphan.write_text("orphan")
        
        # Remove órfãos
        count = manager.remove_orphaned_files()
        
        assert count == 1
    
    def test_combined_cleanup_strategy(self, backup_dir, index_with_backups):
        """Testa estratégia combinada de limpeza"""
        manager = CleanupManager(index_with_backups, backup_dir)
        
        initial_count = len(index_with_backups.get_all())
        
        # 1. Limpa por dias
        manager.cleanup_old_backups(days_to_keep=30, max_per_directory=10)
        
        # 2. Limpa por tamanho
        manager.cleanup_by_size(max_total_size_gb=0.00001)
        
        # 3. Remove órfãos
        manager.remove_orphaned_files()
        
        final_count = len(index_with_backups.get_all())
        
        # Deve ter removido alguns backups
        assert final_count < initial_count
