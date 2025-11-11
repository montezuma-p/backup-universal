"""
Módulo de Limpeza
Gerenciamento de políticas de retenção e limpeza de backups antigos
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from .index import BackupIndex
from ..utils.formatters import format_bytes, format_date


class CleanupManager:
    """Gerenciador de limpeza de backups antigos"""
    
    def __init__(self, index: BackupIndex, backup_dir: Path):
        """
        Inicializa o gerenciador de limpeza
        
        Args:
            index: Instância do BackupIndex
            backup_dir: Diretório onde os backups estão armazenados
        """
        self.index = index
        self.backup_dir = Path(backup_dir)
    
    def cleanup_old_backups(
        self,
        days_to_keep: int = 30,
        max_per_directory: int = 5
    ) -> Dict[str, Any]:
        """
        Remove backups antigos baseado em critérios
        
        Args:
            days_to_keep: Dias para manter backups
            max_per_directory: Máximo de backups por diretório
            
        Returns:
            Dicionário com estatísticas da limpeza
        """
        print(f"\n🧹 LIMPANDO BACKUPS ANTIGOS")
        print(f"📋 Critérios:")
        print(f"   • Manter no máximo {max_per_directory} backups por diretório")
        print(f"   • Manter backups dos últimos {days_to_keep} dias")
        print("=" * 50)
        
        all_backups = self.index.get_all()
        
        if not all_backups:
            print("📂 Nenhum backup para limpar.")
            return {
                'removed_count': 0,
                'freed_space': 0,
                'kept_count': 0
            }
        
        # Data limite
        date_limit = datetime.now() - timedelta(days=days_to_keep)
        
        # Agrupa por diretório
        grouped = self.index.get_grouped_by_directory()
        
        backups_to_remove = []
        freed_space = 0
        
        # Aplica critérios de limpeza
        for dir_name, dir_backups in grouped.items():
            # Ordena por data (mais recente primeiro)
            dir_backups.sort(key=lambda x: x['data_criacao'], reverse=True)
            
            print(f"\n📁 Processando: {dir_name}")
            
            for i, backup in enumerate(dir_backups):
                data_backup = datetime.fromisoformat(backup['data_criacao'])
                arquivo_backup = self.backup_dir / backup['arquivo']
                
                should_remove = False
                reason = ""
                
                # Critério 1: Excede limite de backups
                if i >= max_per_directory:
                    should_remove = True
                    reason = f"excede limite ({max_per_directory} por diretório)"
                
                # Critério 2: Mais antigo que days_to_keep
                elif data_backup < date_limit:
                    should_remove = True
                    reason = f"mais antigo que {days_to_keep} dias"
                
                if should_remove:
                    if arquivo_backup.exists():
                        try:
                            file_size = arquivo_backup.stat().st_size
                            arquivo_backup.unlink()
                            freed_space += file_size
                            
                            date_str = format_date(data_backup, "%d/%m/%Y")
                            size_str = format_bytes(file_size)
                            print(f"   🗑️  Removido: {backup['arquivo']} ({date_str}, {size_str}) - {reason}")
                            
                        except Exception as e:
                            print(f"   ⚠️  Erro ao remover {backup['arquivo']}: {e}")
                            continue
                    else:
                        print(f"   ⚠️  Arquivo {backup['arquivo']} não encontrado (removido do índice)")
                    
                    backups_to_remove.append(backup['arquivo'])
        
        # Remove do índice
        for arquivo in backups_to_remove:
            self.index.remove_backup(arquivo)
        
        kept_count = len(all_backups) - len(backups_to_remove)
        
        # Relatório final
        print(f"\n✅ LIMPEZA CONCLUÍDA")
        print("=" * 30)
        print(f"🗑️  Backups removidos: {len(backups_to_remove)}")
        print(f"💾 Espaço liberado: {format_bytes(freed_space)}")
        print(f"📁 Backups mantidos: {kept_count}")
        
        return {
            'removed_count': len(backups_to_remove),
            'freed_space': freed_space,
            'kept_count': kept_count
        }
    
    def cleanup_by_size(self, max_total_size_gb: int) -> Dict[str, Any]:
        """
        Remove backups mais antigos até ficar abaixo do limite de tamanho
        
        Args:
            max_total_size_gb: Tamanho máximo total em GB
            
        Returns:
            Dicionário com estatísticas
        """
        max_size_bytes = max_total_size_gb * 1024 * 1024 * 1024
        current_size = self.index.get_total_size()
        
        if current_size <= max_size_bytes:
            print(f"✅ Tamanho total ({format_bytes(current_size)}) está dentro do limite.")
            return {
                'removed_count': 0,
                'freed_space': 0,
                'kept_count': len(self.index)
            }
        
        print(f"\n🧹 LIMPANDO POR TAMANHO")
        print(f"📊 Tamanho atual: {format_bytes(current_size)}")
        print(f"📏 Limite: {format_bytes(max_size_bytes)}")
        print(f"📉 Necessário liberar: {format_bytes(current_size - max_size_bytes)}")
        print("=" * 50)
        
        # Ordena backups por data (mais antigo primeiro)
        sorted_backups = self.index.get_sorted_by_date(reverse=False)
        
        backups_to_remove = []
        freed_space = 0
        
        # Remove mais antigos até ficar abaixo do limite
        for backup in sorted_backups:
            if current_size - freed_space <= max_size_bytes:
                break
            
            arquivo_backup = self.backup_dir / backup['arquivo']
            
            if arquivo_backup.exists():
                try:
                    file_size = arquivo_backup.stat().st_size
                    arquivo_backup.unlink()
                    freed_space += file_size
                    
                    data_backup = datetime.fromisoformat(backup['data_criacao'])
                    print(f"   🗑️  Removido: {backup['arquivo']} ({format_date(data_backup, '%d/%m/%Y')})")
                    
                except Exception as e:
                    print(f"   ⚠️  Erro ao remover {backup['arquivo']}: {e}")
                    continue
            
            backups_to_remove.append(backup['arquivo'])
        
        # Remove do índice
        for arquivo in backups_to_remove:
            self.index.remove_backup(arquivo)
        
        print(f"\n✅ Espaço liberado: {format_bytes(freed_space)}")
        
        return {
            'removed_count': len(backups_to_remove),
            'freed_space': freed_space,
            'kept_count': len(self.index)
        }
    
    def remove_orphaned_files(self) -> int:
        """
        Remove arquivos de backup que não estão no índice
        
        Returns:
            Número de arquivos órfãos removidos
        """
        print(f"\n🧹 PROCURANDO ARQUIVOS ÓRFÃOS")
        print("=" * 40)
        
        if not self.backup_dir.exists():
            print("📂 Diretório de backups não encontrado.")
            return 0
        
        # Lista todos os arquivos de backup no diretório
        backup_files = set()
        for ext in ['*.tar.gz', '*.zip']:
            backup_files.update(self.backup_dir.glob(ext))
        
        # Arquivos no índice
        indexed_files = set(
            self.backup_dir / b['arquivo']
            for b in self.index.get_all()
        )
        
        # Arquivos órfãos
        orphaned = backup_files - indexed_files
        
        if not orphaned:
            print("✅ Nenhum arquivo órfão encontrado.")
            return 0
        
        print(f"⚠️  Encontrados {len(orphaned)} arquivos órfãos:")
        
        removed = 0
        for file_path in orphaned:
            try:
                file_path.unlink()
                print(f"   🗑️  Removido: {file_path.name}")
                removed += 1
            except Exception as e:
                print(f"   ⚠️  Erro ao remover {file_path.name}: {e}")
        
        print(f"\n✅ {removed} arquivos órfãos removidos.")
        return removed
