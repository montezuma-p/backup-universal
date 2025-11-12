# 💡 Exemplos de Uso Programático

Este diretório contém exemplos de como usar os módulos de backup programaticamente em seus próprios scripts Python.

## 🚀 Executando

```bash
cd examples
python3 examples.py
```

## 📚 O que há nos exemplos?

O arquivo `examples.py` demonstra:

1. **Backup Básico** - Criar backup de um diretório
2. **Backup Customizado** - Com exclusões personalizadas
3. **Listar Backups** - Consultar e agrupar backups
4. **Limpeza Automática** - Políticas de retenção
5. **Restauração** - Restaurar backups programaticamente
6. **Verificação de Integridade** - Validar hashes MD5
7. **Filtro de Exclusão** - Usar filtros independentemente

## 🔧 Uso nos seus scripts

```python
from backup.config import Config
from backup.core import BackupManager

# Cria gerenciador
config = Config()
manager = BackupManager(config)

# Faz backup
manager.create_backup(
    source_path="/caminho/origem",
    backup_name="meu_backup",
    format_type="tar",
    silent=True
)
```

Veja o arquivo `examples.py` para mais exemplos detalhados!
