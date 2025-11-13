"""
Módulo de Restauração
Sistema interativo para restauração de backups
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from backup.storage.index import BackupIndex
from backup.core.compression import get_compressor
from backup.utils.formatters import format_bytes, format_date
from backup.utils.user_input import safe_input


class RestoreManager:
    """Gerenciador de restauração de backups"""
    
    def __init__(self, index: BackupIndex, backup_dir: Path):
        """
        Inicializa o gerenciador de restauração
        
        Args:
            index: Instância do BackupIndex
            backup_dir: Diretório onde os backups estão armazenados
        """
        self.index = index
        self.backup_dir = Path(backup_dir)
    
    def list_available_backups(self) -> None:
        """Lista backups disponíveis de forma organizada"""
        print("\n📋 BACKUPS EXISTENTES")
        print("=" * 60)
        
        all_backups = self.index.get_all()
        
        if not all_backups:
            print("📂 Nenhum backup encontrado ainda.")
            print(f"💡 Execute um backup primeiro")
            return
        
        # Agrupa por diretório
        grouped = self.index.get_grouped_by_directory()
        
        # Lista backups agrupados
        for dir_name, dir_backups in grouped.items():
            print(f"\n📁 {dir_name} ({len(dir_backups)} backups)")
            
            # Ordena por data (mais recente primeiro)
            dir_backups.sort(key=lambda x: x['data_criacao'], reverse=True)
            
            for i, backup in enumerate(dir_backups):
                data_criacao = datetime.fromisoformat(backup['data_criacao'])
                data_str = format_date(data_criacao)
                
                tamanho = format_bytes(backup['tamanho_backup'])
                compressao = backup.get('taxa_compressao', 0)
                
                # Marca o mais recente
                marcador = "🟢 RECENTE" if i == 0 else "   "
                
                print(f"  {marcador} {backup['arquivo']}")
                print(f"      📅 {data_str}")
                print(f"      📊 {tamanho} (compressão: {compressao:.1f}%)")
                print(f"      🎯 Tipo: {backup.get('tipo_diretorio', 'generico')}")
                print(f"      📁 Origem: {backup.get('diretorio_origem', 'N/A')}")
        
        print(f"\n📊 Total: {len(all_backups)} backups")
    
    def interactive_restore(self) -> bool:
        """
        Interface interativa para restaurar backups
        
        Returns:
            True se restauração bem-sucedida, False caso contrário
        """
        print("\n🔄 RESTAURAÇÃO DE BACKUP")
        print("=" * 40)
        
        all_backups = self.index.get_all()
        
        if not all_backups:
            print("📂 Nenhum backup encontrado para restaurar.")
            return False
        
        # Lista backups disponíveis
        print("Backups disponíveis:")
        sorted_backups = self.index.get_sorted_by_date(reverse=True)
        
        for i, backup in enumerate(sorted_backups):
            data = datetime.fromisoformat(backup['data_criacao'])
            data_str = format_date(data, "%d/%m/%Y %H:%M")
            tamanho = format_bytes(backup['tamanho_backup'])
            
            print(f"  [{i+1}] {backup['nome_diretorio']} - {data_str} ({tamanho})")
        
        # Seleção do backup
        try:
            escolha = safe_input(f"\nEscolha um backup (1-{len(sorted_backups)}) ou 'c' para cancelar: ", "❌ Restauração cancelada pelo usuário.")
            
            if escolha is None:
                return False
            
            escolha = escolha.strip()
            
            if escolha.lower() == 'c':
                print("❌ Restauração cancelada.")
                return False
            
            indice = int(escolha) - 1
            if indice < 0 or indice >= len(sorted_backups):
                print("❌ Opção inválida.")
                return False
        
        except ValueError:
            print("❌ Opção inválida.")
            return False
        
        backup_escolhido = sorted_backups[indice]
        arquivo_backup = self.backup_dir / backup_escolhido['arquivo']
        
        if not arquivo_backup.exists():
            print(f"❌ Arquivo de backup não encontrado: {backup_escolhido['arquivo']}")
            return False
        
        # Escolha do destino
        print(f"\n📁 Restaurando: {backup_escolhido['nome_diretorio']}")
        print(f"📂 Origem: {backup_escolhido.get('diretorio_origem', 'N/A')}")
        
        destino_default = Path.home() / "restauracao" / backup_escolhido['nome_diretorio']
        destino_str = safe_input(f"Diretório de destino (Enter para {destino_default}): ", "❌ Restauração cancelada pelo usuário.")
        
        if destino_str is None:
            return False
        
        destino_str = destino_str.strip()
        
        if destino_str:
            destino = Path(destino_str).expanduser()
        else:
            destino = destino_default
        
        # Cria diretório de destino
        destino.mkdir(parents=True, exist_ok=True)
        
        # Confirma restauração
        print(f"\n🤔 Confirma restauração?")
        print(f"   📦 Backup: {backup_escolhido['arquivo']}")
        print(f"   📁 Destino: {destino}")
        confirmacao = safe_input("   Digite 's' para confirmar: ", "❌ Restauração cancelada pelo usuário.")
        
        if confirmacao is None:
            return False
        
        if confirmacao.lower() != 's':
            print("❌ Restauração cancelada.")
            return False
        
        # Executa restauração
        return self.restore_backup(arquivo_backup, destino, backup_escolhido)
    
    def restore_backup(
        self,
        archive_path: Path,
        destination: Path,
        backup_info: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Restaura um backup específico
        
        Args:
            archive_path: Caminho do arquivo de backup
            destination: Diretório de destino
            backup_info: Informações do backup (opcional)
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            print(f"\n⏳ Extraindo backup...")
            
            # Detecta formato pelo nome do arquivo
            if archive_path.suffix == '.gz' and archive_path.stem.endswith('.tar'):
                formato = 'tar'
            elif archive_path.suffix == '.zip':
                formato = 'zip'
            else:
                print(f"❌ Formato de arquivo não reconhecido: {archive_path}")
                return False
            
            # Obtém compressor apropriado
            compressor = get_compressor(formato)
            
            # Extrai backup
            compressor.decompress(archive_path, destination.parent)
            
            print(f"✅ Backup restaurado com sucesso!")
            print(f"📁 Localização: {destination}")
            
            if backup_info:
                print(f"\n📊 Informações do backup:")
                print(f"   • Origem: {backup_info.get('diretorio_origem', 'N/A')}")
                print(f"   • Data: {format_date(datetime.fromisoformat(backup_info['data_criacao']))}")
                print(f"   • Arquivos: {backup_info.get('total_arquivos', 'N/A'):,}")
                print(f"   • Tipo: {backup_info.get('tipo_diretorio', 'generico')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante restauração: {e}")
            return False
    
    def restore_by_name(self, backup_name: str, destination: Path) -> bool:
        """
        Restaura um backup pelo nome do arquivo
        
        Args:
            backup_name: Nome do arquivo de backup
            destination: Diretório de destino
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        # Busca backup no índice
        backup_info = None
        for backup in self.index.get_all():
            if backup['arquivo'] == backup_name:
                backup_info = backup
                break
        
        if not backup_info:
            print(f"❌ Backup não encontrado no índice: {backup_name}")
            return False
        
        archive_path = self.backup_dir / backup_name
        
        if not archive_path.exists():
            print(f"❌ Arquivo não encontrado: {archive_path}")
            return False
        
        return self.restore_backup(archive_path, destination, backup_info)
    
    def verify_backup_integrity(self, backup_name: str) -> bool:
        """
        Verifica integridade de um backup comparando hash
        
        Args:
            backup_name: Nome do arquivo de backup
            
        Returns:
            True se íntegro, False caso contrário
        """
        from backup.core.integrity import IntegrityChecker
        
        # Busca backup no índice
        backup_info = None
        for backup in self.index.get_all():
            if backup['arquivo'] == backup_name:
                backup_info = backup
                break
        
        if not backup_info:
            print(f"❌ Backup não encontrado no índice: {backup_name}")
            return False
        
        expected_hash = backup_info.get('hash_md5')
        if not expected_hash:
            print(f"⚠️  Backup não possui hash MD5 registrado")
            return False
        
        archive_path = self.backup_dir / backup_name
        
        if not archive_path.exists():
            print(f"❌ Arquivo não encontrado: {archive_path}")
            return False
        
        print(f"🔍 Verificando integridade de {backup_name}...")
        actual_hash = IntegrityChecker.calculate_md5(archive_path)
        
        if actual_hash == expected_hash:
            print(f"✅ Backup íntegro! Hash: {actual_hash[:16]}...")
            return True
        else:
            print(f"❌ Backup corrompido!")
            print(f"   Esperado: {expected_hash[:16]}...")
            print(f"   Atual: {actual_hash[:16] if actual_hash else 'N/A'}...")
            return False
