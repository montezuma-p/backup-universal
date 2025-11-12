#!/usr/bin/env python3
"""
CLI - Interface de Linha de Comando
Interface principal do sistema de backup
"""

import argparse
import sys
from pathlib import Path

from backup.config import Config
from backup.core.backup_manager import BackupManager
from backup.storage.cleanup import CleanupManager
from backup.restore.restore_manager import RestoreManager


def create_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos"""
    parser = argparse.ArgumentParser(
        description="Script de backup universal de diretórios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS DE USO:
  python3 -m backup                                    # Backup completo do diretório padrão
  python3 -m backup -d /home/user/documentos           # Backup de diretório específico
  python3 -m backup -d ./projetos --nome meus_projetos # Backup com nome personalizado
  python3 -m backup --compressao-maxima                # Backup com máxima compressão
  python3 -m backup --excluir "*.iso,Downloads,tmp"    # Excluir padrões específicos
  python3 -m backup --silencioso --formato tar         # Backup sem confirmações
  python3 -m backup --listar-backups                   # Lista backups existentes
  python3 -m backup --limpar-antigos                   # Remove backups antigos
  python3 -m backup --restaurar                        # Interface de restauração
        """
    )
    
    parser.add_argument(
        '-d', '--diretorio',
        help='Caminho do diretório para backup (padrão: configurado em config.json)'
    )
    
    parser.add_argument(
        '--nome',
        help='Nome personalizado para o backup'
    )
    
    parser.add_argument(
        '--compressao-maxima',
        action='store_true',
        help='Usa compressão máxima (mais lento, mas menor arquivo)'
    )
    
    parser.add_argument(
        '--excluir',
        help='Padrões adicionais para excluir (separados por vírgula)'
    )
    
    parser.add_argument(
        '--silencioso',
        action='store_true',
        help='Executa backup sem pedir confirmação (obrigatório informar --formato)'
    )
    
    parser.add_argument(
        '--formato',
        choices=['tar', 'zip'],
        help='Formato de compressão: "tar" para .tar.gz (Linux/macOS), "zip" para .zip (Windows)'
    )
    
    parser.add_argument(
        '--listar-backups',
        action='store_true',
        help='Lista todos os backups existentes'
    )
    
    parser.add_argument(
        '--limpar-antigos',
        action='store_true',
        help='Remove backups antigos (conforme política em config.json)'
    )
    
    parser.add_argument(
        '--restaurar',
        action='store_true',
        help='Interface interativa para restaurar backups'
    )
    
    parser.add_argument(
        '--config',
        help='Caminho para arquivo config.json alternativo'
    )
    
    return parser


def main():
    """Função principal do CLI"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Carrega configuração
    try:
        if args.config:
            config = Config(Path(args.config))
        else:
            config = Config()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        sys.exit(1)
    
    # Inicializa gerenciadores
    backup_manager = BackupManager(config)
    cleanup_manager = CleanupManager(backup_manager.index, config.backup_destination)
    restore_manager = RestoreManager(backup_manager.index, config.backup_destination)
    
    # Adiciona padrões de exclusão customizados
    if args.excluir:
        backup_manager.add_custom_exclusions(args.excluir)
        print(f"🚫 Padrões de exclusão adicionais: {args.excluir}")
    
    # Executa ação baseada nos argumentos
    if args.listar_backups:
        restore_manager.list_available_backups()
        
    elif args.limpar_antigos:
        cleanup_manager.cleanup_old_backups(
            days_to_keep=config.days_to_keep,
            max_per_directory=config.max_backups_per_directory
        )
        
    elif args.restaurar:
        restore_manager.interactive_restore()
        
    else:
        # Executa backup
        compression_level = 9 if args.compressao_maxima else None
        
        sucesso = backup_manager.create_backup(
            source_path=args.diretorio,
            backup_name=args.nome,
            format_type=args.formato,
            compression_level=compression_level,
            silent=args.silencioso
        )
        
        if sucesso:
            print("\n💡 DICAS:")
            print("   • Execute backups regularmente (semanal/quinzenal)")
            print("   • Use --limpar-antigos para manter espaço em disco")
            print("   • Teste restaurações periodicamente")
            print("   • Considere sincronizar a pasta 'backups' com nuvem")
            print("   • Use --excluir para personalizar padrões de exclusão")
        else:
            print("\n⚠️  Verifique se o diretório especificado existe e é acessível")
            sys.exit(1)


if __name__ == "__main__":
    main()
