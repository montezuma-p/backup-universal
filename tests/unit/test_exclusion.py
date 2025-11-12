"""
Testes Unitários - Módulo de Exclusão
Testa o sistema de filtros de exclusão
"""

import pytest
import importlib.util
from pathlib import Path

# Importa módulo diretamente do arquivo sem passar por __init__.py
spec = importlib.util.spec_from_file_location(
    "exclusion",
    Path(__file__).parent.parent.parent / "core" / "exclusion.py"
)
exclusion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exclusion)

ExclusionFilter = exclusion.ExclusionFilter


class TestExclusionFilterInit:
    """Testes de inicialização do ExclusionFilter"""
    
    def test_init_empty(self):
        """Testa inicialização sem padrões"""
        filter = ExclusionFilter()
        assert len(filter) == 0
        assert filter.get_patterns() == []
    
    def test_init_with_patterns(self):
        """Testa inicialização com padrões"""
        patterns = ["*.pyc", "__pycache__", "node_modules"]
        filter = ExclusionFilter(patterns)
        assert len(filter) == 3
        assert filter.get_patterns() == patterns
    
    def test_init_with_none(self):
        """Testa inicialização com None"""
        filter = ExclusionFilter(None)
        assert len(filter) == 0


class TestAddPattern:
    """Testes para add_pattern()"""
    
    def test_add_single_pattern(self, exclusion_filter):
        """Testa adicionar um padrão"""
        exclusion_filter.add_pattern("*.log")
        assert "*.log" in exclusion_filter.get_patterns()
    
    def test_add_duplicate_pattern(self, exclusion_filter):
        """Testa adicionar padrão duplicado (não deve adicionar)"""
        exclusion_filter.add_pattern("*.pyc")
        initial_count = len(exclusion_filter)
        exclusion_filter.add_pattern("*.pyc")
        assert len(exclusion_filter) == initial_count
    
    def test_add_empty_pattern(self, exclusion_filter):
        """Testa adicionar padrão vazio (não deve adicionar)"""
        initial_count = len(exclusion_filter)
        exclusion_filter.add_pattern("")
        assert len(exclusion_filter) == initial_count
    
    def test_cache_cleared_on_add(self, exclusion_filter):
        """Testa se cache é limpo ao adicionar padrão"""
        # Popula cache
        exclusion_filter.should_exclude("test.pyc")
        assert len(exclusion_filter._cache) > 0
        
        # Adiciona padrão
        exclusion_filter.add_pattern("*.log")
        assert len(exclusion_filter._cache) == 0


class TestAddPatterns:
    """Testes para add_patterns()"""
    
    def test_add_multiple_patterns(self, exclusion_filter):
        """Testa adicionar múltiplos padrões"""
        new_patterns = ["*.log", "*.tmp", "*.bak"]
        initial_count = len(exclusion_filter)
        exclusion_filter.add_patterns(new_patterns)
        # *.tmp já existe no fixture, então só adiciona 2 novos
        assert len(exclusion_filter) == initial_count + 2
    
    def test_add_empty_list(self, exclusion_filter):
        """Testa adicionar lista vazia"""
        initial_count = len(exclusion_filter)
        exclusion_filter.add_patterns([])
        assert len(exclusion_filter) == initial_count


class TestRemovePattern:
    """Testes para remove_pattern()"""
    
    def test_remove_existing_pattern(self, exclusion_filter):
        """Testa remover padrão existente"""
        exclusion_filter.add_pattern("*.log")
        assert "*.log" in exclusion_filter.get_patterns()
        
        exclusion_filter.remove_pattern("*.log")
        assert "*.log" not in exclusion_filter.get_patterns()
    
    def test_remove_nonexistent_pattern(self, exclusion_filter):
        """Testa remover padrão inexistente (não deve dar erro)"""
        initial_count = len(exclusion_filter)
        exclusion_filter.remove_pattern("*.xyz")
        assert len(exclusion_filter) == initial_count
    
    def test_cache_cleared_on_remove(self, exclusion_filter):
        """Testa se cache é limpo ao remover padrão"""
        # Popula cache
        exclusion_filter.should_exclude("test.pyc")
        assert len(exclusion_filter._cache) > 0
        
        # Remove padrão
        exclusion_filter.remove_pattern("*.pyc")
        assert len(exclusion_filter._cache) == 0


class TestShouldExclude:
    """Testes para should_exclude()"""
    
    def test_exclude_pyc_files(self, exclusion_filter):
        """Testa exclusão de arquivos .pyc"""
        assert exclusion_filter.should_exclude("test.pyc") is True
        assert exclusion_filter.should_exclude("module.pyc") is True
    
    def test_exclude_pycache_dir(self, exclusion_filter):
        """Testa exclusão de __pycache__"""
        assert exclusion_filter.should_exclude("__pycache__") is True
        assert exclusion_filter.should_exclude("src/__pycache__") is True
    
    def test_exclude_node_modules(self, exclusion_filter):
        """Testa exclusão de node_modules"""
        assert exclusion_filter.should_exclude("node_modules") is True
        assert exclusion_filter.should_exclude("project/node_modules") is True
    
    def test_not_exclude_python_files(self, exclusion_filter):
        """Testa que arquivos .py não são excluídos"""
        assert exclusion_filter.should_exclude("test.py") is False
        assert exclusion_filter.should_exclude("module.py") is False
    
    def test_not_exclude_normal_files(self, exclusion_filter):
        """Testa que arquivos normais não são excluídos"""
        assert exclusion_filter.should_exclude("README.md") is False
        assert exclusion_filter.should_exclude("config.json") is False
    
    def test_wildcard_pattern(self):
        """Testa padrão com wildcard"""
        filter = ExclusionFilter(["test_*"])
        assert filter.should_exclude("test_file.txt") is True
        assert filter.should_exclude("test_module.py") is True
        assert filter.should_exclude("my_test.py") is False
    
    def test_cache_usage(self, exclusion_filter):
        """Testa uso do cache"""
        # Primeira verificação
        result1 = exclusion_filter.should_exclude("test.pyc")
        assert "test.pyc" in exclusion_filter._cache
        
        # Segunda verificação (usa cache)
        result2 = exclusion_filter.should_exclude("test.pyc")
        assert result1 == result2


class TestFilterPaths:
    """Testes para filter_paths()"""
    
    def test_filter_mixed_paths(self, exclusion_filter):
        """Testa filtrar lista mista de caminhos"""
        paths = [
            Path("src/main.py"),
            Path("src/test.pyc"),
            Path("src/__pycache__"),
            Path("README.md"),
            Path("node_modules"),
        ]
        
        filtered = exclusion_filter.filter_paths(paths)
        
        # Deve manter apenas .py e README.md
        assert len(filtered) == 2
        assert Path("src/main.py") in filtered
        assert Path("README.md") in filtered
    
    def test_filter_empty_list(self, exclusion_filter):
        """Testa filtrar lista vazia"""
        assert exclusion_filter.filter_paths([]) == []
    
    def test_filter_all_excluded(self, exclusion_filter):
        """Testa quando todos são excluídos"""
        paths = [
            Path("test.pyc"),
            Path("__pycache__"),
            Path("node_modules"),
        ]
        
        filtered = exclusion_filter.filter_paths(paths)
        assert len(filtered) == 0
    
    def test_filter_none_excluded(self, exclusion_filter):
        """Testa quando nenhum é excluído"""
        paths = [
            Path("main.py"),
            Path("config.json"),
            Path("README.md"),
        ]
        
        filtered = exclusion_filter.filter_paths(paths)
        assert len(filtered) == 3


class TestGetPatterns:
    """Testes para get_patterns()"""
    
    def test_get_patterns_returns_copy(self, exclusion_filter):
        """Testa que get_patterns() retorna uma cópia"""
        patterns = exclusion_filter.get_patterns()
        patterns.append("*.new")
        
        # Não deve afetar o original
        assert "*.new" not in exclusion_filter.get_patterns()


class TestClearCache:
    """Testes para clear_cache()"""
    
    def test_clear_cache(self, exclusion_filter):
        """Testa limpar cache"""
        # Popula cache
        exclusion_filter.should_exclude("test.pyc")
        exclusion_filter.should_exclude("module.pyc")
        assert len(exclusion_filter._cache) > 0
        
        # Limpa cache
        exclusion_filter.clear_cache()
        assert len(exclusion_filter._cache) == 0


class TestMagicMethods:
    """Testes para métodos mágicos"""
    
    def test_len(self, exclusion_filter):
        """Testa __len__()"""
        assert len(exclusion_filter) == 4  # Fixture tem 4 padrões
        exclusion_filter.add_pattern("*.log")
        assert len(exclusion_filter) == 5
    
    def test_repr(self, exclusion_filter):
        """Testa __repr__()"""
        repr_str = repr(exclusion_filter)
        assert "ExclusionFilter" in repr_str
        assert "4 patterns" in repr_str  # Fixture tem 4 padrões
