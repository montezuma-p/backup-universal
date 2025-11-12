"""
Pytest Configuration & Shared Fixtures
Configuração global e fixtures reutilizáveis para todos os testes
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Importa módulos do projeto
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from backup.config import Config
from backup.core import ExclusionFilter, IntegrityChecker
from backup.storage import BackupIndex


# ==================== FIXTURES DE DIRETÓRIOS ====================

@pytest.fixture
def tmp_backup_dir(tmp_path):
    """
    Cria diretório temporário para armazenar backups de teste
    
    Returns:
        Path: Caminho do diretório temporário
    """
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    return backup_dir


@pytest.fixture
def tmp_source_dir(tmp_path):
    """
    Cria diretório temporário com arquivos de teste para backup
    
    Returns:
        Path: Caminho com estrutura de arquivos de teste
    """
    source = tmp_path / "source"
    source.mkdir()
    
    # Cria alguns arquivos de teste
    (source / "file1.txt").write_text("conteúdo do arquivo 1")
    (source / "file2.py").write_text("print('hello world')")
    (source / "data.json").write_text('{"key": "value"}')
    
    # Cria subdiretório
    subdir = source / "subdir"
    subdir.mkdir()
    (subdir / "nested.txt").write_text("arquivo aninhado")
    
    return source


@pytest.fixture
def tmp_config_file(tmp_path):
    """
    Cria arquivo config.json temporário para testes
    
    Returns:
        Path: Caminho do config.json temporário
    """
    config_data = {
        "paths": {
            "default_backup_source": str(tmp_path / "source"),
            "backup_destination": str(tmp_path / "backups"),
            "temp_dir": str(tmp_path / "temp")
        },
        "retention_policy": {
            "max_backups_per_directory": 5,
            "days_to_keep": 30,
            "max_total_size_gb": 50
        },
        "compression": {
            "default_format": "tar",
            "default_level": 6
        },
        "exclusion_patterns": {
            "default": ["*.tmp", "*.log", "__pycache__"],
            "custom": []
        },
        "notifications": {
            "enabled": False,
            "email": "",
            "webhook_url": ""
        }
    }
    
    config_file = tmp_path / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    return config_file


# ==================== FIXTURES DE OBJETOS ====================

@pytest.fixture
def exclusion_filter():
    """
    Cria ExclusionFilter básico para testes
    
    Returns:
        ExclusionFilter: Filtro com padrões padrão
    """
    return ExclusionFilter(['*.log', '*.tmp', '__pycache__', 'node_modules'])


@pytest.fixture
def backup_index(tmp_backup_dir):
    """
    Cria BackupIndex vazio para testes
    
    Returns:
        BackupIndex: Índice de backups em diretório temporário
    """
    index_file = tmp_backup_dir / "indice_backups.json"
    return BackupIndex(index_file)


@pytest.fixture
def sample_backup_info():
    """
    Retorna dicionário com informações de backup de exemplo
    
    Returns:
        Dict: Dados de exemplo de um backup
    """
    return {
        "arquivo": "backup_test_20251112_120000.tar.gz",
        "diretorio_origem": "/tmp/test/source",
        "nome_diretorio": "test",
        "data_criacao": datetime.now().isoformat(),
        "tamanho_original": 1024000,
        "tamanho_backup": 512000,
        "taxa_compressao": 50.0,
        "total_arquivos": 42,
        "arquivos_excluidos": 8,
        "diretorios_excluidos": 2,
        "tipo_diretorio": "python",
        "hash_md5": "a1b2c3d4e5f6g7h8i9j0",
        "compressao_maxima": False,
        "formato": "tar"
    }


# ==================== FIXTURES DE ARQUIVOS DE TESTE ====================

@pytest.fixture
def sample_text_file(tmp_path):
    """
    Cria arquivo de texto de exemplo para testes de hash
    
    Returns:
        Path: Caminho do arquivo criado
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello, World!\nTeste de conteúdo.\n")
    return file_path


@pytest.fixture
def sample_binary_file(tmp_path):
    """
    Cria arquivo binário de exemplo
    
    Returns:
        Path: Caminho do arquivo binário
    """
    file_path = tmp_path / "sample.bin"
    file_path.write_bytes(b'\x00\x01\x02\x03\x04\x05')
    return file_path


# ==================== FIXTURES DE ESTRUTURA COMPLEXA ====================

@pytest.fixture
def complex_source_structure(tmp_path):
    """
    Cria estrutura de diretórios complexa simulando projeto real
    
    Returns:
        Path: Raiz da estrutura criada
    """
    root = tmp_path / "project"
    root.mkdir()
    
    # Simula projeto Python
    (root / "main.py").write_text("# Main file")
    (root / "README.md").write_text("# Project README")
    (root / "requirements.txt").write_text("requests==2.28.0")
    
    # Diretório src
    src = root / "src"
    src.mkdir()
    (src / "__init__.py").write_text("")
    (src / "module.py").write_text("def function(): pass")
    
    # Diretório a ser excluído
    pycache = src / "__pycache__"
    pycache.mkdir()
    (pycache / "module.cpython-39.pyc").write_bytes(b"compiled")
    
    # Venv a ser excluído
    venv = root / "venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin")
    
    # Tests
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_module.py").write_text("def test_function(): assert True")
    
    return root


# ==================== HOOKS & CONFIGURAÇÕES ====================

def pytest_configure(config):
    """Hook executado antes dos testes começarem"""
    config.addinivalue_line(
        "markers", "requires_filesystem: marca testes que precisam de acesso real ao filesystem"
    )


@pytest.fixture(autouse=True)
def reset_environment():
    """
    Fixture executada automaticamente antes de cada teste
    Garante ambiente limpo
    """
    # Setup antes do teste
    yield
    # Teardown depois do teste
    # Adicione aqui qualquer limpeza necessária
    pass


# ==================== UTILITIES PARA TESTES ====================

@pytest.fixture
def create_test_archive(tmp_path):
    """
    Factory fixture para criar arquivos .tar.gz de teste
    
    Returns:
        Callable: Função que cria arquivo de teste
    """
    import tarfile
    
    def _create(name: str, files: Dict[str, str]) -> Path:
        """
        Cria arquivo tar.gz com conteúdo especificado
        
        Args:
            name: Nome do arquivo (sem extensão)
            files: Dict {nome_arquivo: conteúdo}
            
        Returns:
            Path: Caminho do arquivo criado
        """
        archive_path = tmp_path / f"{name}.tar.gz"
        
        with tarfile.open(archive_path, 'w:gz') as tar:
            for filename, content in files.items():
                file_path = tmp_path / filename
                file_path.write_text(content)
                tar.add(str(file_path), arcname=filename)
                file_path.unlink()  # Remove arquivo temporário
        
        return archive_path
    
    return _create


# ==================== MARKERS PERSONALIZADOS ====================

def pytest_collection_modifyitems(config, items):
    """
    Adiciona markers automaticamente baseado no nome do arquivo
    """
    for item in items:
        # Adiciona marker 'unit' para testes em tests/unit/
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Adiciona marker 'integration' para testes em tests/integration/
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Adiciona marker 'e2e' para testes em tests/e2e/
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
