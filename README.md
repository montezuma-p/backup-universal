<div align="center">

# 📦 backup universal 📦

<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWEwYzIzbjg4cHoyN2hoNWswajBreDRieTRudmh4ZmZnNzg2Nmt5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Yra5D7TBosllmwnGhG/giphy.gif" width="400"/>

### 🚀 script inteligente de backup

**Porque perder dados é coisa do passado.**  
</div>

---

## 🎯 o que é isso?

Sistema completo de backup universal para Linux que:
- 📦 **Compacta** diretórios inteiros com exclusões inteligentes
- 🗜️ **Suporta** múltiplos formatos (.tar.gz e .zip)
- 🎯 **Detecta** tipos de projeto (Node.js, Python, Java, Git)
- 🧹 **Limpa** backups antigos automaticamente
- 🔄 **Restaura** backups interativamente
- 📈 **Estatísticas** detalhadas de compressão
- 🔒 **Hash MD5** para verificação de integridade

<div align="center">

<img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGd3eGh3d2tkODYzNTZteHExN25ndmJsZDFncmtyZmZlOGx2cGg0dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/CuuSHzuc0O166MRfjt/giphy.gif" width="250"/>

</div>

---

## ⚡ features principais

<table>
<tr>
<td width="50%">

### 🎨 **Exclusões Inteligentes**
Ignora automaticamente:
- `node_modules`, `__pycache__`, `.git`
- Arquivos temporários e cache
- Builds e IDEs
- ISOs e arquivos grandes

_smart pattern matching_

</td>
<td width="50%">

### 🗂️ **Gerenciamento Avançado**
Sistema completo com:
- Índice JSON de todos os backups
- Agrupamento por diretório
- Políticas de retenção configuráveis
- Estatísticas de compressão

_complete lifecycle management_

</td>
</tr>
<tr>
<td>

### 🔄 **Restauração Simples**
Interface interativa para:
- Listar backups disponíveis
- Escolher versões específicas
- Restaurar para qualquer local
- Validar integridade

_restore with confidence_

</td>
<td>

### 📊 **Relatórios Detalhados**
Informações completas:
- Taxa de compressão
- Número de arquivos
- Tamanho antes/depois
- Tipo de projeto detectado

_know everything about your backups_

</td>
</tr>
</table>

---

## 🚀 instalação

```bash
# Clone o repositório
git clone https://github.com/montezuma-p/backup-universal
cd backup-universal

# Configure suas preferências
cp config.json.example config.json
```

## 🤝 contribuindo

Quer ajudar no projeto? Veja o [guia de contribuição](docs/CONTRIBUINDO.md)!

**Três formas de executar:**

```bash
# 1. Shell script (recomendado)
./backup.sh --listar-backups

# 2. Como módulo Python
cd .. && python3 -m backup --help

# 3. Criando um alias global
echo "alias backup='/caminho/completo/backup.sh'" >> ~/.bashrc
source ~/.bashrc
backup --help
```

---

## 📖 uso

### 📦 Criar Backup

```bash
# Backup do diretório padrão (configurado em config.json)
python3 -m backup

# Backup de diretório específico
python3 -m backup -d /home/user/projetos

# Backup com nome personalizado
python3 -m backup -d ./meu-projeto --nome projeto-importante

# Backup com compressão máxima
python3 -m backup --compressao-maxima

# Backup silencioso (sem confirmação) - requer formato
python3 -m backup -d ~/documentos --silencioso --formato tar

# Backup em formato ZIP (compatível com Windows)
python3 -m backup --formato zip

# Excluir padrões adicionais
python3 -m backup --excluir "*.mp4,*.mkv,videos"
```

### 📋 Listar Backups

```bash
# Lista todos os backups com estatísticas
python3 -m backup --listar-backups
```

Saída:
```
📋 BACKUPS EXISTENTES
============================================================

📁 meu-projeto (3 backups)
  🟢 RECENTE backup_meu-projeto_20241105_143022.tar.gz
      📅 05/11/2024 14:30:22
      📊 45.2 MB (compressão: 78.5%)
      🎯 Tipo: nodejs
      📁 Origem: /home/user/projetos/meu-projeto
```

### 🧹 Limpar Backups Antigos

```bash
# Remove backups conforme política configurada em config.json
python3 -m backup --limpar-antigos
```

### 🔄 Restaurar Backup

```bash
# Interface interativa para restauração
python3 -m backup --restaurar
```

---

## ⚙️ configuração

### 📁 Estrutura Modular (v1.1)

```
backup-universal/
├── backup.sh                # 🚀 Script launcher
├── config.json.example      # 📝 Template de configuração
├── LICENSE
├── README.md
├── docs/                    # 📚 Documentação
│   └── ROADMAP.md
├── examples/                # 💡 Exemplos de uso
│   └── examples.py
└── backup/                  # 📦 Package Python
    ├── __init__.py          # Package principal
    ├── __main__.py          # Entry point
    ├── cli.py               # Interface CLI
    ├── config.py            # Gerenciador de configuração
    ├── config.json          # Configuração pessoal (não versionado)
    ├── core/                # Módulos principais
    │   ├── backup_manager.py    # Orquestrador
    │   ├── compression.py       # Compressão
    │   ├── exclusion.py         # Filtros
    │   └── integrity.py         # Hashes
    ├── storage/             # Armazenamento
    │   ├── index.py         # Índice JSON
    │   └── cleanup.py       # Limpeza
    ├── restore/             # Restauração
    │   └── restore_manager.py
    └── utils/               # Utilitários
        ├── formatters.py
        └── file_utils.py
```
│   └── restore_manager.py
└── utils/                  # Utilitários
    ├── formatters.py
    └── file_utils.py
```

### 🔧 config.json

Todas as configurações agora estão centralizadas em `config.json`:

```json
{
  "paths": {
    "default_backup_source": "/home/montezuma",
    "backup_destination": "~/.bin/data/backups/archives"
  },
  "retention_policy": {
    "max_backups_per_directory": 5,
    "days_to_keep": 30
  },
  "compression": {
    "default_format": "tar",
    "default_level": 6
  },
  "exclusion_patterns": {
    "default": [...],
    "custom": []
  }
}
```

Os backups são armazenados em:
```
~/.bin/data/backups/archives/
├── backup_projeto1_20241105_143022.tar.gz
├── backup_projeto2_20241105_150433.zip
└── indice_backups.json
```

### 📝 Padrões de Exclusão Padrão

- **Temporários:** `*.tmp`, `*.temp`, `*.log`, `*.cache`
- **Node.js:** `node_modules`, `npm-debug.log`, `.npm`
- **Python:** `__pycache__`, `*.pyc`, `.pytest_cache`, `venv`, `.venv`
- **Git:** `.git`
- **IDEs:** `.vscode`, `.idea`, `*.swp`, `*.swo`
- **Builds:** `build`, `dist`, `target`
- **OS:** `.DS_Store`, `Thumbs.db`, `.Trash`
- **Grandes:** `*.iso`, `*.dmg`, `*.img`

---

## 🎯 exemplos práticos

### Backup de Projeto Web

```bash
# Backup de projeto Node.js com exclusões
python3 backup.py -d ~/projetos/meu-site \
  --nome site-producao \
  --excluir "uploads,*.log,public/temp" \
  --formato tar
```

### Backup Automatizado (Cron)

```bash
# Adicione ao crontab (crontab -e)
# Backup diário às 3h da manhã
0 3 * * * python3 ~/.scripts/tools/backup/backup.py -d ~/projetos --silencioso --formato tar

# Limpeza semanal aos domingos às 4h
0 4 * * 0 python3 ~/.scripts/tools/backup/backup.py --limpar-antigos
```

### Backup de Múltiplos Diretórios

```bash
# Script shell para backup de múltiplos diretórios
#!/bin/bash
for dir in ~/projetos/*/; do
    python3 backup.py -d "$dir" --silencioso --formato tar
done
```

---

## 📊 estrutura do índice

O arquivo `indice_backups.json` mantém registro completo:

```json
[
  {
    "arquivo": "backup_meu-projeto_20241105_143022.tar.gz",
    "diretorio_origem": "/home/user/projetos/meu-projeto",
    "nome_diretorio": "meu-projeto",
    "data_criacao": "2024-11-05T14:30:22.123456",
    "tamanho_original": 210534400,
    "tamanho_backup": 45234560,
    "taxa_compressao": 78.5,
    "total_arquivos": 1523,
    "arquivos_excluidos": 45632,
    "diretorios_excluidos": 234,
    "tipo_diretorio": "nodejs",
    "hash_md5": "a1b2c3d4e5f6...",
    "compressao_maxima": false,
    "formato": "tar"
  }
]
```

---

## 🛠️ stack tecnológico

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

**Bibliotecas Python:**
- `tarfile` - Compressão .tar.gz
- `zipfile` - Compressão .zip
- `hashlib` - Verificação de integridade
- `argparse` - CLI interface
- `pathlib` - Manipulação de paths
- `json` - Gerenciamento de índice

---

## 🎯 casos de uso

✅ **Backup de projetos antes de grandes mudanças**  
✅ **Versionamento de configurações do sistema**  
✅ **Arquivamento de projetos antigos**  
✅ **Backup antes de limpezas de disco**  
✅ **Proteção de dados importantes**  
✅ **Sincronização com nuvem (pasta de backups)**

<div align="center">

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjl6a2VyYzZvdGRmYndlanE3aXl6eG1iN2k4bHp0bWczY282Z3JoYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YQitE4YNQNahy/giphy.gif" width="300"/>

</div>

---

## 🔮 roadmap

Veja [ROADMAP.md](ROADMAP.md) para planos futuros e desenvolvimento.

---

## 🤝 contribuindo

Contribuições são sempre bem-vindas!

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 autor

Feito com ❤️ por **[Montezuma](https://github.com/montezuma-p)**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/montezuma-p)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/montezuma-p/)

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHZ2ZDR6YnBxOGFsemJ5Z3FjcW1vdWV6dXlhZ3RrODRlbWN5eXZ1ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hvRJCLFzcasrR4ia7z/giphy.gif" width="100"/>

### 🚀 **bora fazer backup das paradas importantes!** 🚀

</div>

---

## 🎉 Novidades da Versão 1.1

### ✨ Modularização Completa

A versão 1.1 traz uma **refatoração completa** do código:

- **📦 Arquitetura Modular**: Código organizado em módulos especializados
- **⚙️ config.json**: Todas as configurações em um único arquivo JSON
- **🧪 Testabilidade**: Cada módulo pode ser testado isoladamente
- **🔌 Reutilização**: Módulos podem ser importados em outros projetos
- **📚 Manutenibilidade**: Fácil localização e correção de bugs

### 🏗️ Estrutura de Módulos

| Módulo | Responsabilidade |
|--------|------------------|
| `config.py` | Gerenciamento de configurações |
| `core/backup_manager.py` | Orquestração do processo de backup |
| `core/compression.py` | Compressão (tar.gz, zip) |
| `core/exclusion.py` | Filtros de exclusão |
| `core/integrity.py` | Verificação de integridade (hashes) |
| `storage/index.py` | Gerenciamento do índice JSON |
| `storage/cleanup.py` | Políticas de limpeza |
| `restore/restore_manager.py` | Sistema de restauração |
| `utils/formatters.py` | Formatação de dados |
| `utils/file_utils.py` | Operações com arquivos |

### 🔄 Migração da v1.0

Se você usava a versão anterior (`backup.py`), **nada muda na linha de comando**! A interface permanece 100% compatível. Apenas execute com `python3 -m backup` ao invés de `python3 backup.py`.

---

