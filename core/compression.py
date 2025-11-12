"""
Módulo de Compressão
Classes para compressão de backups em diferentes formatos
"""

import os
import tarfile
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Callable, Tuple


class Compressor(ABC):
    """Classe base abstrata para compressores"""
    
    @abstractmethod
    def compress(
        self,
        source_path: Path,
        output_path: Path,
        exclusion_filter,
        progress_callback: Optional[Callable] = None,
        compression_level: int = 6
    ) -> Tuple[int, int, int]:
        """
        Comprime um diretório
        
        Args:
            source_path: Caminho do diretório de origem
            output_path: Caminho do arquivo de saída
            exclusion_filter: Filtro de exclusão
            progress_callback: Função de callback para progresso
            compression_level: Nível de compressão (0-9)
            
        Returns:
            Tupla (total_arquivos, arquivos_excluidos, diretorios_excluidos)
        """
        pass
    
    @abstractmethod
    def decompress(self, archive_path: Path, destination_path: Path) -> None:
        """
        Descomprime um arquivo
        
        Args:
            archive_path: Caminho do arquivo comprimido
            destination_path: Caminho de destino
        """
        pass
    
    @property
    @abstractmethod
    def extension(self) -> str:
        """Extensão do arquivo gerado"""
        pass


class TarCompressor(Compressor):
    """Compressor para formato .tar.gz"""
    
    @property
    def extension(self) -> str:
        return ".tar.gz"
    
    def compress(
        self,
        source_path: Path,
        output_path: Path,
        exclusion_filter,
        progress_callback: Optional[Callable] = None,
        compression_level: int = 6
    ) -> Tuple[int, int, int]:
        """Comprime usando tar.gz"""
        total_files = 0
        excluded_files = 0
        excluded_dirs = 0
        
        with tarfile.open(
            output_path,
            'w:gz',
            compresslevel=compression_level
        ) as tar:
            for root, dirs, files in os.walk(source_path):
                # Remove diretórios excluídos
                dirs_before = len(dirs)
                dirs[:] = [d for d in dirs if not exclusion_filter.should_exclude(d)]
                excluded_dirs += (dirs_before - len(dirs))
                
                # Adiciona arquivos
                for file in files:
                    if exclusion_filter.should_exclude(file):
                        excluded_files += 1
                        continue
                    
                    try:
                        file_path = Path(root) / file
                        # Mantém estrutura relativa
                        arcname = file_path.relative_to(source_path.parent)
                        tar.add(str(file_path), arcname=str(arcname))
                        total_files += 1
                        
                        # Callback de progresso
                        if progress_callback:
                            progress_callback(total_files)
                            
                    except Exception as e:
                        print(f"   ⚠️  Erro ao adicionar {file}: {e}")
                        excluded_files += 1
                        continue
        
        return total_files, excluded_files, excluded_dirs
    
    def decompress(self, archive_path: Path, destination_path: Path) -> None:
        """Descomprime arquivo tar.gz"""
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=destination_path)


class ZipCompressor(Compressor):
    """Compressor para formato .zip"""
    
    @property
    def extension(self) -> str:
        return ".zip"
    
    def compress(
        self,
        source_path: Path,
        output_path: Path,
        exclusion_filter,
        progress_callback: Optional[Callable] = None,
        compression_level: int = 6
    ) -> Tuple[int, int, int]:
        """Comprime usando zip"""
        total_files = 0
        excluded_files = 0
        excluded_dirs = 0
        
        with zipfile.ZipFile(
            output_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=compression_level
        ) as zipf:
            for root, dirs, files in os.walk(source_path):
                # Remove diretórios excluídos
                dirs_before = len(dirs)
                dirs[:] = [d for d in dirs if not exclusion_filter.should_exclude(d)]
                excluded_dirs += (dirs_before - len(dirs))
                
                # Adiciona arquivos
                for file in files:
                    if exclusion_filter.should_exclude(file):
                        excluded_files += 1
                        continue
                    
                    try:
                        file_path = Path(root) / file
                        # Mantém estrutura relativa
                        arcname = file_path.relative_to(source_path.parent)
                        zipf.write(str(file_path), arcname=str(arcname))
                        total_files += 1
                        
                        # Callback de progresso
                        if progress_callback:
                            progress_callback(total_files)
                            
                    except Exception as e:
                        print(f"   ⚠️  Erro ao adicionar {file}: {e}")
                        excluded_files += 1
                        continue
        
        return total_files, excluded_files, excluded_dirs
    
    def decompress(self, archive_path: Path, destination_path: Path) -> None:
        """Descomprime arquivo zip"""
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extractall(path=destination_path)


def get_compressor(format_type: str) -> Compressor:
    """
    Factory function para obter compressor adequado
    
    Args:
        format_type: Tipo de formato ('tar' ou 'zip')
        
    Returns:
        Instância de Compressor apropriada
        
    Raises:
        ValueError: Se formato não for suportado
    """
    if format_type.lower() == 'tar':
        return TarCompressor()
    elif format_type.lower() == 'zip':
        return ZipCompressor()
    else:
        raise ValueError(f"Formato não suportado: {format_type}")
