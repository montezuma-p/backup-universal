"""
Módulo Backup Manager
Orquestrador principal do processo de backup
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

from .compression import get_compressor
from .exclusion import ExclusionFilter
from .integrity import IntegrityChecker
from ..storage.index import BackupIndex
from ..utils.formatters import format_bytes, format_compression_rate, format_number
from ..utils.file_utils import calculate_directory_size, get_directory_info
from ..config import Config


class BackupStats:
    """Estatísticas do processo de backup"""
    
    def __init__(self):
        self.total_files = 0
        self.excluded_files = 0
        self.excluded_dirs = 0
        self.original_size = 0
        self.backup_size = 0
        self.compression_rate = 0.0
        self.hash_md5 = ""
        
    def reset(self):
        """Reseta as estatísticas"""
        self.__init__()


class BackupManager:
    """Gerenciador principal de backups"""
    
    def __init__(self, config: Config):
        """
        Inicializa o gerenciador de backup
        
        Args:
            config: Instância de Config com configurações
        """
        self.config = config
        self.index = BackupIndex(config.index_file)
        self.exclusion_filter = ExclusionFilter(config.all_exclusion_patterns)
        self.stats = BackupStats()
        
    def create_backup(
        self,
        source_path: Optional[Path] = None,
        backup_name: Optional[str] = None,
        format_type: Optional[str] = None,
        compression_level: Optional[int] = None,
        silent: bool = False
    ) -> bool:
        """
        Cria um backup de um diretório
        
        Args:
            source_path: Caminho de origem (usa padrão se None)
            backup_name: Nome personalizado do backup (opcional)
            format_type: Formato ('tar' ou 'zip', usa padrão se None)
            compression_level: Nível de compressão 0-9 (usa padrão se None)
            silent: Se True, não pede confirmação
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        # Define valores padrão
        if source_path is None:
            source_path = self.config.default_backup_source
        else:
            source_path = Path(source_path).expanduser().resolve()
            
        if format_type is None:
            format_type = self.config.default_format
            
        if compression_level is None:
            compression_level = self.config.default_compression_level
        
        # Validações
        if not source_path.exists():
            print(f"❌ Erro: Diretório '{source_path}' não encontrado!")
            return False
            
        if not source_path.is_dir():
            print(f"❌ Erro: '{source_path}' não é um diretório!")
            return False
        
        # Obtém informações do diretório
        dir_info = get_directory_info(source_path)
        dir_name = dir_info["nome"]
        
        print(f"\n📦 INICIANDO BACKUP")
        print("=" * 50)
        print(f"📁 Diretório: {source_path}")
        print(f"🏷️  Tipo: {dir_info['tipo']}")
        
        # Calcula tamanho
        print("📊 Calculando tamanho do backup...")
        self.stats.original_size, estimated_files = calculate_directory_size(
            source_path,
            self.exclusion_filter
        )
        
        print(f"📈 Arquivos a processar: {format_number(estimated_files)}")
        print(f"📏 Tamanho estimado: {format_bytes(self.stats.original_size)}")
        
        # Confirmação interativa
        if not silent:
            if not self._confirm_backup(dir_name, format_type):
                print("❌ Backup cancelado pelo usuário.")
                return False
        else:
            if not format_type:
                print("❌ O formato de backup deve ser especificado em modo silencioso.")
                return False
        
        # Define nome do arquivo de backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        compressor = get_compressor(format_type)
        
        if backup_name:
            filename = f"{backup_name}_{timestamp}{compressor.extension}"
        else:
            filename = f"backup_{dir_name}_{timestamp}{compressor.extension}"
        
        backup_path = self.config.backup_destination / filename
        
        # Cria backup
        print(f"\n⏳ Criando backup: {filename}")
        if compression_level >= 9:
            print("🗜️  Usando compressão máxima...")
        
        # Reset estatísticas
        self.stats.reset()
        
        try:
            # Progresso
            progress_tracker = ProgressTracker(estimated_files)
            
            # Comprime
            total_files, excluded_files, excluded_dirs = compressor.compress(
                source_path,
                backup_path,
                self.exclusion_filter,
                progress_callback=progress_tracker.update,
                compression_level=compression_level
            )
            
            self.stats.total_files = total_files
            self.stats.excluded_files = excluded_files
            self.stats.excluded_dirs = excluded_dirs
            
            # Calcula informações finais
            self.stats.backup_size = backup_path.stat().st_size
            self.stats.compression_rate = format_compression_rate(
                self.stats.original_size,
                self.stats.backup_size
            )
            self.stats.hash_md5 = IntegrityChecker.calculate_md5(backup_path) or ""
            
            # Registra no índice
            backup_info = {
                "arquivo": filename,
                "diretorio_origem": str(source_path),
                "nome_diretorio": dir_name,
                "data_criacao": datetime.now().isoformat(),
                "tamanho_original": self.stats.original_size,
                "tamanho_backup": self.stats.backup_size,
                "taxa_compressao": self.stats.compression_rate,
                "total_arquivos": self.stats.total_files,
                "arquivos_excluidos": self.stats.excluded_files,
                "diretorios_excluidos": self.stats.excluded_dirs,
                "tipo_diretorio": dir_info["tipo"],
                "hash_md5": self.stats.hash_md5,
                "compressao_maxima": (compression_level >= 9),
                "formato": format_type
            }
            
            self.index.add_backup(backup_info)
            
            # Relatório final
            self._print_success_report(filename, backup_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            # Remove arquivo parcial
            if backup_path.exists():
                try:
                    backup_path.unlink()
                except:
                    pass
            return False
    
    def _confirm_backup(self, dir_name: str, format_type: str) -> bool:
        """
        Solicita confirmação do usuário
        
        Args:
            dir_name: Nome do diretório
            format_type: Formato atual
            
        Returns:
            True se confirmado, False caso contrário
        """
        print(f"\n🤔 Deseja prosseguir com o backup de '{dir_name}'?")
        
        custom_patterns = self.config.custom_exclusion_patterns
        if custom_patterns:
            print(f"🚫 Padrões de exclusão adicionais: {', '.join(custom_patterns)}")
        
        print("   Escolha o formato de compressão:")
        print("   [1] .tar.gz (Linux/macOS)")
        print("   [2] .zip (Windows)")
        print("      OBS: Para poder descompactar em um Windows")
        
        formato_opcao = input("   Digite 1 para .tar.gz ou 2 para .zip: ").strip()
        
        if formato_opcao == '1':
            format_type = 'tar'
        elif formato_opcao == '2':
            format_type = 'zip'
        else:
            print("❌ Opção inválida.")
            return False
        
        # Atualiza formato escolhido
        self.config.set('compression', {
            'default_format': format_type,
            'default_level': self.config.default_compression_level
        })
        
        confirmacao = input("   Digite 's' para continuar ou qualquer tecla para cancelar: ").lower()
        return confirmacao == 's'
    
    def _print_success_report(self, filename: str, backup_path: Path) -> None:
        """Imprime relatório de sucesso"""
        print(f"\n✅ BACKUP CONCLUÍDO COM SUCESSO!")
        print("=" * 50)
        print(f"📁 Arquivo: {filename}")
        print(f"📊 Arquivos incluídos: {format_number(self.stats.total_files)}")
        print(f"🚫 Itens excluídos: {format_number(self.stats.excluded_files + self.stats.excluded_dirs)}")
        print(f"📏 Tamanho original: {format_bytes(self.stats.original_size)}")
        print(f"🗜️  Tamanho backup: {format_bytes(self.stats.backup_size)}")
        print(f"📉 Compressão: {self.stats.compression_rate:.1f}%")
        print(f"🔒 Hash MD5: {self.stats.hash_md5[:16]}...")
        print(f"💾 Localização: {backup_path}")
    
    def add_custom_exclusion(self, pattern: str) -> None:
        """Adiciona padrão de exclusão customizado"""
        self.config.add_custom_pattern(pattern)
        self.exclusion_filter.add_pattern(pattern)
    
    def add_custom_exclusions(self, patterns_string: str) -> None:
        """
        Adiciona múltiplos padrões de exclusão
        
        Args:
            patterns_string: String com padrões separados por vírgula
        """
        if patterns_string:
            patterns = [p.strip() for p in patterns_string.split(',') if p.strip()]
            for pattern in patterns:
                self.add_custom_exclusion(pattern)


class ProgressTracker:
    """Rastreador de progresso do backup"""
    
    def __init__(self, total_estimated: int):
        self.total_estimated = total_estimated
        self.current = 0
        self.last_reported = 0
        self.report_interval = max(100, total_estimated // 50)  # Relata a cada 2%
    
    def update(self, current: int) -> None:
        """Atualiza progresso"""
        self.current = current
        
        if self.current - self.last_reported >= self.report_interval:
            if self.total_estimated > 0:
                progress = (self.current / self.total_estimated) * 100
                print(f"   📦 Progresso: {format_number(self.current)}/{format_number(self.total_estimated)} arquivos ({progress:.1f}%)")
            else:
                print(f"   📦 Processados: {format_number(self.current)} arquivos")
            
            self.last_reported = self.current
