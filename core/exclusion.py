"""
Módulo de Exclusão
Gerencia padrões de exclusão de arquivos e diretórios
"""

import fnmatch
from pathlib import Path
from typing import List, Set


class ExclusionFilter:
    """Filtro de exclusão baseado em padrões glob"""
    
    def __init__(self, patterns: List[str] = None):
        """
        Inicializa o filtro de exclusão
        
        Args:
            patterns: Lista de padrões glob para exclusão
        """
        self.patterns: List[str] = patterns or []
        self._cache: Set[str] = set()  # Cache de itens já verificados
        
    def add_pattern(self, pattern: str) -> None:
        """Adiciona um padrão de exclusão"""
        if pattern and pattern not in self.patterns:
            self.patterns.append(pattern)
            self._cache.clear()  # Limpa cache ao modificar padrões
            
    def add_patterns(self, patterns: List[str]) -> None:
        """Adiciona múltiplos padrões de exclusão"""
        for pattern in patterns:
            self.add_pattern(pattern)
            
    def remove_pattern(self, pattern: str) -> None:
        """Remove um padrão de exclusão"""
        if pattern in self.patterns:
            self.patterns.remove(pattern)
            self._cache.clear()
            
    def should_exclude(self, path: str) -> bool:
        """
        Verifica se um caminho deve ser excluído
        
        Args:
            path: Caminho do arquivo ou diretório (pode ser apenas o nome)
            
        Returns:
            True se deve ser excluído, False caso contrário
        """
        # Usa cache para melhor performance
        cache_key = str(path)
        if cache_key in self._cache:
            return True
            
        # Obtém apenas o nome do arquivo/diretório
        nome = Path(path).name
        
        # Verifica cada padrão
        for pattern in self.patterns:
            if fnmatch.fnmatch(nome, pattern):
                self._cache.add(cache_key)
                return True
                
        return False
    
    def filter_paths(self, paths: List[Path]) -> List[Path]:
        """
        Filtra uma lista de caminhos removendo os que devem ser excluídos
        
        Args:
            paths: Lista de caminhos
            
        Returns:
            Lista filtrada
        """
        return [p for p in paths if not self.should_exclude(str(p))]
    
    def get_patterns(self) -> List[str]:
        """Retorna lista de padrões ativos"""
        return self.patterns.copy()
    
    def clear_cache(self) -> None:
        """Limpa o cache de verificações"""
        self._cache.clear()
    
    def __repr__(self) -> str:
        return f"<ExclusionFilter: {len(self.patterns)} patterns>"
    
    def __len__(self) -> int:
        return len(self.patterns)
