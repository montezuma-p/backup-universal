#!/usr/bin/env python3
"""
Exemplo de Uso Programático dos Módulos de Backup
Este arquivo demonstra como usar os módulos de backup em seu próprio código Python
"""

import sys
from pathlib import Path

# Adiciona o diretório ao path se necessário
sys.path.insert(0, str(Path(__file__).parent.parent))

from backup.config import Config
from backup.core import BackupManager, ExclusionFilter, IntegrityChecker
from backup.storage import BackupIndex, CleanupManager
from backup.restore import RestoreManager


def exemplo_backup_basico():
    """Exemplo: Criar um backup básico"""
    print("=== Exemplo 1: Backup Básico ===\n")
    
    # Carrega configuração
    config = Config()
    
    # Cria gerenciador de backup
    manager = BackupManager(config)
    
    # Cria backup do diretório padrão
    sucesso = manager.create_backup(
        source_path="/home/montezuma/Documents",
        backup_name="documentos",
        format_type="tar",
        silent=True  # Sem confirmação
    )
    
    if sucesso:
        print("✅ Backup criado com sucesso!")
    else:
        print("❌ Erro ao criar backup")


def exemplo_backup_customizado():
    """Exemplo: Backup com exclusões customizadas"""
    print("\n=== Exemplo 2: Backup Customizado ===\n")
    
    config = Config()
    manager = BackupManager(config)
    
    # Adiciona padrões de exclusão personalizados
    manager.add_custom_exclusion("*.pdf")
    manager.add_custom_exclusion("backup_*")
    
    # Cria backup
    manager.create_backup(
        source_path="/home/montezuma/Projects",
        backup_name="projetos_sem_pdfs",
        format_type="zip",
        compression_level=9,  # Máxima compressão
        silent=True
    )


def exemplo_listar_backups():
    """Exemplo: Listar e consultar backups"""
    print("\n=== Exemplo 3: Consultar Backups ===\n")
    
    config = Config()
    index = BackupIndex(config.index_file)
    
    # Lista todos os backups
    todos = index.get_all()
    print(f"Total de backups: {len(todos)}")
    
    # Backups agrupados por diretório
    por_dir = index.get_grouped_by_directory()
    print(f"\nDiretórios com backup: {len(por_dir)}")
    
    for dir_name, backups in por_dir.items():
        print(f"  📁 {dir_name}: {len(backups)} backups")
    
    # Estatísticas
    stats = index.get_statistics()
    print(f"\nEstatísticas:")
    print(f"  - Total de backups: {stats['total_backups']}")
    print(f"  - Tamanho total: {stats['total_size'] / (1024**3):.2f} GB")
    print(f"  - Diretórios únicos: {stats['unique_directories']}")


def exemplo_limpeza():
    """Exemplo: Limpeza automática de backups antigos"""
    print("\n=== Exemplo 4: Limpeza Automática ===\n")
    
    config = Config()
    index = BackupIndex(config.index_file)
    cleanup = CleanupManager(index, config.backup_destination)
    
    # Limpa backups antigos
    resultado = cleanup.cleanup_old_backups(
        days_to_keep=30,
        max_per_directory=3
    )
    
    print(f"\nResultado:")
    print(f"  - Removidos: {resultado['removed_count']}")
    print(f"  - Espaço liberado: {resultado['freed_space'] / (1024**2):.2f} MB")
    print(f"  - Mantidos: {resultado['kept_count']}")


def exemplo_restauracao():
    """Exemplo: Restaurar backup programaticamente"""
    print("\n=== Exemplo 5: Restauração ===\n")
    
    config = Config()
    index = BackupIndex(config.index_file)
    restore = RestoreManager(index, config.backup_destination)
    
    # Lista backups disponíveis
    backups = index.get_sorted_by_date(reverse=True)
    
    if backups:
        backup_mais_recente = backups[0]
        print(f"Backup mais recente: {backup_mais_recente['arquivo']}")
        
        # Restaura para um diretório específico
        destino = Path("/tmp/restauracao_teste")
        sucesso = restore.restore_by_name(
            backup_mais_recente['arquivo'],
            destino
        )
        
        if sucesso:
            print(f"✅ Backup restaurado em: {destino}")
    else:
        print("❌ Nenhum backup disponível")


def exemplo_verificacao_integridade():
    """Exemplo: Verificar integridade de backups"""
    print("\n=== Exemplo 6: Verificação de Integridade ===\n")
    
    config = Config()
    index = BackupIndex(config.index_file)
    restore = RestoreManager(index, config.backup_destination)
    
    backups = index.get_all()
    
    print("Verificando integridade de todos os backups...")
    
    integros = 0
    corrompidos = 0
    
    for backup in backups[:5]:  # Verifica apenas os 5 primeiros para exemplo
        arquivo = backup['arquivo']
        if restore.verify_backup_integrity(arquivo):
            integros += 1
        else:
            corrompidos += 1
    
    print(f"\nResultado:")
    print(f"  ✅ Íntegros: {integros}")
    print(f"  ❌ Corrompidos: {corrompidos}")


def exemplo_exclusion_filter():
    """Exemplo: Usar filtro de exclusão independentemente"""
    print("\n=== Exemplo 7: Filtro de Exclusão ===\n")
    
    # Cria filtro customizado
    filtro = ExclusionFilter()
    filtro.add_patterns([
        "*.log",
        "*.tmp",
        "node_modules",
        "__pycache__"
    ])
    
    # Testa arquivos
    arquivos_teste = [
        "arquivo.txt",      # ✅ Não excluído
        "debug.log",        # ❌ Excluído
        "temp.tmp",         # ❌ Excluído
        "node_modules",     # ❌ Excluído
        "main.py",          # ✅ Não excluído
        "__pycache__"       # ❌ Excluído
    ]
    
    print("Testando filtro de exclusão:")
    for arquivo in arquivos_teste:
        excluir = filtro.should_exclude(arquivo)
        status = "❌ EXCLUIR" if excluir else "✅ INCLUIR"
        print(f"  {status}: {arquivo}")


if __name__ == "__main__":
    print("🎓 EXEMPLOS DE USO DOS MÓDULOS DE BACKUP\n")
    print("=" * 60)
    
    
    
    exemplo_backup_basico()
    exemplo_backup_customizado()
    exemplo_listar_backups()
    exemplo_limpeza()
    exemplo_restauracao()
    exemplo_verificacao_integridade()
    exemplo_exclusion_filter()
    
    print("\n" + "=" * 60)
    print("✨ Fim dos exemplos!")
    print("\n💡 Dica: Edite este arquivo e descomente os exemplos que quiser testar!")
