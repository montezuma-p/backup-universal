"""
Módulo de Índice
Gerenciamento do índice JSON de backups
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class BackupIndex:
    """Gerenciador do índice de backups"""
    
    def __init__(self, index_path: Path):
        """
        Inicializa o gerenciador de índice
        
        Args:
            index_path: Caminho para o arquivo de índice JSON
        """
        self.index_path = Path(index_path)
        self._backups: List[Dict[str, Any]] = []
        self.load()
    
    def load(self) -> None:
        """Carrega índice do arquivo JSON"""
        if not self.index_path.exists():
            self._backups = []
            return
        
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self._backups = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._backups = []
    
    def save(self) -> None:
        """Salva índice no arquivo JSON"""
        try:
            # Garante que o diretório existe
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self._backups, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Aviso: Erro ao salvar índice: {e}")
    
    def add_backup(self, backup_info: Dict[str, Any]) -> None:
        """
        Adiciona um backup ao índice
        
        Args:
            backup_info: Dicionário com informações do backup
        """
        self._backups.append(backup_info)
        self.save()
    
    def remove_backup(self, arquivo: str) -> bool:
        """
        Remove um backup do índice pelo nome do arquivo
        
        Args:
            arquivo: Nome do arquivo de backup
            
        Returns:
            True se removido, False se não encontrado
        """
        original_len = len(self._backups)
        self._backups = [b for b in self._backups if b.get('arquivo') != arquivo]
        
        if len(self._backups) < original_len:
            self.save()
            return True
        return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Retorna todos os backups"""
        return self._backups.copy()
    
    def get_by_directory(self, directory_name: str) -> List[Dict[str, Any]]:
        """
        Retorna backups de um diretório específico
        
        Args:
            directory_name: Nome do diretório
            
        Returns:
            Lista de backups
        """
        return [
            b for b in self._backups
            if b.get('nome_diretorio') == directory_name
        ]
    
    def get_grouped_by_directory(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retorna backups agrupados por diretório
        
        Returns:
            Dicionário {nome_diretorio: [backups]}
        """
        grouped = {}
        for backup in self._backups:
            dir_name = backup.get('nome_diretorio', 'desconhecido')
            if dir_name not in grouped:
                grouped[dir_name] = []
            grouped[dir_name].append(backup)
        return grouped
    
    def get_sorted_by_date(self, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Retorna backups ordenados por data
        
        Args:
            reverse: Se True, mais recentes primeiro
            
        Returns:
            Lista ordenada de backups
        """
        return sorted(
            self._backups,
            key=lambda x: x.get('data_criacao', ''),
            reverse=reverse
        )
    
    def find_by_hash(self, hash_md5: str) -> Optional[Dict[str, Any]]:
        """
        Encontra backup por hash MD5
        
        Args:
            hash_md5: Hash MD5 do backup
            
        Returns:
            Informações do backup ou None
        """
        for backup in self._backups:
            if backup.get('hash_md5') == hash_md5:
                return backup
        return None
    
    def get_total_size(self) -> int:
        """
        Calcula tamanho total de todos os backups
        
        Returns:
            Tamanho total em bytes
        """
        return sum(b.get('tamanho_backup', 0) for b in self._backups)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais dos backups
        
        Returns:
            Dicionário com estatísticas
        """
        if not self._backups:
            return {
                'total_backups': 0,
                'total_size': 0,
                'unique_directories': 0,
                'oldest_backup': None,
                'newest_backup': None
            }
        
        sorted_backups = self.get_sorted_by_date(reverse=False)
        
        return {
            'total_backups': len(self._backups),
            'total_size': self.get_total_size(),
            'unique_directories': len(self.get_grouped_by_directory()),
            'oldest_backup': sorted_backups[0].get('data_criacao') if sorted_backups else None,
            'newest_backup': sorted_backups[-1].get('data_criacao') if sorted_backups else None
        }
    
    def clear(self) -> None:
        """Remove todos os backups do índice"""
        self._backups = []
        self.save()
    
    def __len__(self) -> int:
        return len(self._backups)
    
    def __repr__(self) -> str:
        return f"<BackupIndex: {len(self._backups)} backups>"
