"""
Módulo de Integridade
Cálculo de hashes e verificação de integridade de arquivos
"""

import hashlib
from pathlib import Path
from typing import Optional


class IntegrityChecker:
    """Verificador de integridade de arquivos usando hashes"""
    
    CHUNK_SIZE = 4096  # 4KB chunks para leitura eficiente
    
    @staticmethod
    def calculate_md5(file_path: Path) -> Optional[str]:
        """
        Calcula hash MD5 de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            String hexadecimal do hash MD5, ou None em caso de erro
        """
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(IntegrityChecker.CHUNK_SIZE), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def calculate_sha256(file_path: Path) -> Optional[str]:
        """
        Calcula hash SHA256 de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            String hexadecimal do hash SHA256, ou None em caso de erro
        """
        hash_sha256 = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(IntegrityChecker.CHUNK_SIZE), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def verify_file(file_path: Path, expected_hash: str, algorithm: str = 'md5') -> bool:
        """
        Verifica se o hash de um arquivo corresponde ao esperado
        
        Args:
            file_path: Caminho do arquivo
            expected_hash: Hash esperado
            algorithm: Algoritmo ('md5' ou 'sha256')
            
        Returns:
            True se o hash corresponde, False caso contrário
        """
        if algorithm.lower() == 'md5':
            actual_hash = IntegrityChecker.calculate_md5(file_path)
        elif algorithm.lower() == 'sha256':
            actual_hash = IntegrityChecker.calculate_sha256(file_path)
        else:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")
        
        if actual_hash is None:
            return False
            
        return actual_hash.lower() == expected_hash.lower()
    
    @staticmethod
    def calculate_hash(file_path: Path, algorithm: str = 'md5') -> Optional[str]:
        """
        Calcula hash de um arquivo usando o algoritmo especificado
        
        Args:
            file_path: Caminho do arquivo
            algorithm: Algoritmo ('md5' ou 'sha256')
            
        Returns:
            String hexadecimal do hash, ou None em caso de erro
        """
        if algorithm.lower() == 'md5':
            return IntegrityChecker.calculate_md5(file_path)
        elif algorithm.lower() == 'sha256':
            return IntegrityChecker.calculate_sha256(file_path)
        else:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")
