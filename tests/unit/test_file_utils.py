"""
Testes Unitários - Módulo de Utilitários de Arquivos
Testa funções utilitárias para operações com arquivos
"""

import pytest
import importlib.util
from pathlib import Path
from datetime import datetime

# Importa módulo diretamente do arquivo
spec = importlib.util.spec_from_file_location(
    "file_utils",
    Path(__file__).parent.parent.parent / "utils" / "file_utils.py"
)
file_utils_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_utils_mod)

calculate_directory_size = file_utils_mod.calculate_directory_size
detect_directory_type = file_utils_mod.detect_directory_type
get_directory_info = file_utils_mod.get_directory_info
ensure_directory = file_utils_mod.ensure_directory
safe_file_remove = file_utils_mod.safe_file_remove
get_file_size = file_utils_mod.get_file_size

# Importa ExclusionFilter para testes
spec_excl = importlib.util.spec_from_file_location(
    "exclusion",
    Path(__file__).parent.parent.parent / "core" / "exclusion.py"
)
exclusion_mod = importlib.util.module_from_spec(spec_excl)
spec_excl.loader.exec_module(exclusion_mod)
ExclusionFilter = exclusion_mod.ExclusionFilter


class TestCalculateDirectorySize:
    """Testes para calculate_directory_size()"""
    
    def test_basic_calculation(self, tmp_path):
        """Testa cálculo básico de tamanho"""
        # Cria arquivos
        (tmp_path / "file1.txt").write_text("a" * 100)
        (tmp_path / "file2.txt").write_text("b" * 200)
        
        total_size, total_files = calculate_directory_size(tmp_path)
        
        assert total_size == 300
        assert total_files == 2
    
    def test_with_subdirectories(self, tmp_path):
        """Testa cálculo com subdiretórios"""
        (tmp_path / "file1.txt").write_text("a" * 100)
        
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("b" * 200)
        
        total_size, total_files = calculate_directory_size(tmp_path)
        
        assert total_size == 300
        assert total_files == 2
    
    def test_empty_directory(self, tmp_path):
        """Testa diretório vazio"""
        total_size, total_files = calculate_directory_size(tmp_path)
        
        assert total_size == 0
        assert total_files == 0
    
    def test_with_exclusion_filter(self, tmp_path):
        """Testa com filtro de exclusão"""
        (tmp_path / "file1.txt").write_text("a" * 100)
        (tmp_path / "file2.pyc").write_text("b" * 200)
        (tmp_path / "file3.tmp").write_text("c" * 150)
        
        filter = ExclusionFilter(['*.pyc', '*.tmp'])
        total_size, total_files = calculate_directory_size(tmp_path, filter)
        
        # Deve contar apenas file1.txt
        assert total_size == 100
        assert total_files == 1
    
    def test_with_excluded_directories(self, tmp_path):
        """Testa com diretórios excluídos"""
        (tmp_path / "file1.txt").write_text("a" * 100)
        
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "cache.pyc").write_text("b" * 200)
        
        filter = ExclusionFilter(['__pycache__'])
        total_size, total_files = calculate_directory_size(tmp_path, filter)
        
        # Não deve contar arquivos em __pycache__
        assert total_size == 100
        assert total_files == 1


class TestDetectDirectoryType:
    """Testes para detect_directory_type()"""
    
    def test_detect_nodejs(self, tmp_path):
        """Testa detecção de projeto Node.js"""
        (tmp_path / "package.json").write_text('{"name": "test"}')
        
        assert detect_directory_type(tmp_path) == "nodejs"
    
    def test_detect_python_requirements(self, tmp_path):
        """Testa detecção de projeto Python (requirements.txt)"""
        (tmp_path / "requirements.txt").write_text("pytest>=7.0")
        
        assert detect_directory_type(tmp_path) == "python"
    
    def test_detect_python_setup(self, tmp_path):
        """Testa detecção de projeto Python (setup.py)"""
        (tmp_path / "setup.py").write_text("from setuptools import setup")
        
        assert detect_directory_type(tmp_path) == "python"
    
    def test_detect_java(self, tmp_path):
        """Testa detecção de projeto Java"""
        (tmp_path / "pom.xml").write_text("<project></project>")
        
        assert detect_directory_type(tmp_path) == "java"
    
    def test_detect_git(self, tmp_path):
        """Testa detecção de repositório Git"""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        assert detect_directory_type(tmp_path) == "git"
    
    def test_detect_generic(self, tmp_path):
        """Testa detecção genérica"""
        (tmp_path / "random.txt").write_text("content")
        
        assert detect_directory_type(tmp_path) == "generico"
    
    def test_nonexistent_directory(self, tmp_path):
        """Testa diretório inexistente"""
        nonexistent = tmp_path / "nonexistent"
        
        assert detect_directory_type(nonexistent) == "generico"
    
    def test_file_instead_of_directory(self, tmp_path):
        """Testa quando caminho é arquivo, não diretório"""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        
        assert detect_directory_type(file_path) == "generico"
    
    def test_priority_nodejs_over_git(self, tmp_path):
        """Testa que Node.js tem prioridade sobre Git"""
        (tmp_path / "package.json").write_text('{}')
        (tmp_path / ".git").mkdir()
        
        # package.json é verificado primeiro
        assert detect_directory_type(tmp_path) == "nodejs"


class TestGetDirectoryInfo:
    """Testes para get_directory_info()"""
    
    def test_basic_info(self, tmp_path):
        """Testa informações básicas"""
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        
        info = get_directory_info(test_dir)
        
        assert info is not None
        assert info["nome"] == "test"
        assert info["tipo"] == "generico"
        assert "caminho" in info
        assert "ultima_modificacao" in info
    
    def test_with_project_type(self, tmp_path):
        """Testa com tipo de projeto detectado"""
        (tmp_path / "package.json").write_text('{}')
        
        info = get_directory_info(tmp_path)
        
        assert info["tipo"] == "nodejs"
    
    def test_nonexistent_directory(self, tmp_path):
        """Testa diretório inexistente"""
        nonexistent = tmp_path / "nonexistent"
        
        info = get_directory_info(nonexistent)
        assert info is None
    
    def test_file_path(self, tmp_path):
        """Testa informações de arquivo"""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        
        info = get_directory_info(file_path)
        
        assert info is not None
        assert info["nome"] == "file.txt"
        assert info["tamanho"] == 7  # len("content")
    
    def test_directory_has_no_size(self, tmp_path):
        """Testa que diretório não tem campo tamanho"""
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        
        info = get_directory_info(test_dir)
        
        assert info["tamanho"] is None


class TestEnsureDirectory:
    """Testes para ensure_directory()"""
    
    def test_create_simple_directory(self, tmp_path):
        """Testa criar diretório simples"""
        new_dir = tmp_path / "new"
        
        result = ensure_directory(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir
    
    def test_create_nested_directories(self, tmp_path):
        """Testa criar diretórios aninhados"""
        nested = tmp_path / "a" / "b" / "c"
        
        result = ensure_directory(nested)
        
        assert nested.exists()
        assert nested.is_dir()
    
    def test_existing_directory(self, tmp_path):
        """Testa com diretório existente (não deve dar erro)"""
        test_dir = tmp_path / "existing"
        test_dir.mkdir()
        
        result = ensure_directory(test_dir)
        
        assert test_dir.exists()
        assert result == test_dir
    
    def test_with_tilde_expansion(self, tmp_path, monkeypatch):
        """Testa expansão de ~ (home)"""
        # Simula home directory
        monkeypatch.setenv("HOME", str(tmp_path))
        
        result = ensure_directory(Path("~/test"))
        
        assert result.exists()
        assert "test" in str(result)


class TestSafeFileRemove:
    """Testes para safe_file_remove()"""
    
    def test_remove_existing_file(self, tmp_path):
        """Testa remover arquivo existente"""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        
        result = safe_file_remove(file_path)
        
        assert result is True
        assert not file_path.exists()
    
    def test_remove_nonexistent_file(self, tmp_path):
        """Testa remover arquivo inexistente"""
        file_path = tmp_path / "nonexistent.txt"
        
        result = safe_file_remove(file_path)
        
        assert result is False
    
    def test_remove_directory_fails_safely(self, tmp_path):
        """Testa que remover diretório falha de forma segura"""
        dir_path = tmp_path / "dir"
        dir_path.mkdir()
        
        result = safe_file_remove(dir_path)
        
        # Deve retornar False sem lançar exceção
        assert result is False
        assert dir_path.exists()


class TestGetFileSize:
    """Testes para get_file_size()"""
    
    def test_small_file(self, tmp_path):
        """Testa arquivo pequeno"""
        file_path = tmp_path / "small.txt"
        file_path.write_text("hello")
        
        size = get_file_size(file_path)
        assert size == 5
    
    def test_large_file(self, tmp_path):
        """Testa arquivo grande"""
        file_path = tmp_path / "large.txt"
        file_path.write_text("a" * 10000)
        
        size = get_file_size(file_path)
        assert size == 10000
    
    def test_empty_file(self, tmp_path):
        """Testa arquivo vazio"""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")
        
        size = get_file_size(file_path)
        assert size == 0
    
    def test_nonexistent_file(self, tmp_path):
        """Testa arquivo inexistente"""
        file_path = tmp_path / "nonexistent.txt"
        
        size = get_file_size(file_path)
        assert size == 0
    
    def test_directory(self, tmp_path):
        """Testa com diretório (deve retornar tamanho do diretório)"""
        dir_path = tmp_path / "dir"
        dir_path.mkdir()
        
        size = get_file_size(dir_path)
        # Diretório tem tamanho > 0 no sistema de arquivos
        assert size >= 0


class TestIntegration:
    """Testes de integração entre funções"""
    
    def test_calculate_then_detect(self, tmp_path):
        """Testa calcular tamanho e detectar tipo"""
        (tmp_path / "package.json").write_text('{}')
        (tmp_path / "file.txt").write_text("a" * 100)
        
        size, files = calculate_directory_size(tmp_path)
        dir_type = detect_directory_type(tmp_path)
        
        assert size > 100  # Inclui package.json
        assert files == 2
        assert dir_type == "nodejs"
    
    def test_ensure_then_calculate(self, tmp_path):
        """Testa criar diretório e calcular tamanho"""
        new_dir = tmp_path / "new"
        ensure_directory(new_dir)
        
        size, files = calculate_directory_size(new_dir)
        
        assert size == 0
        assert files == 0
    
    def test_get_info_comprehensive(self, tmp_path):
        """Testa informações completas de diretório Python"""
        (tmp_path / "requirements.txt").write_text("pytest")
        (tmp_path / "main.py").write_text("print('hello')")
        
        info = get_directory_info(tmp_path)
        
        assert info["tipo"] == "python"
        assert info["nome"] == tmp_path.name
        assert "ultima_modificacao" in info
