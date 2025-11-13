<div align="center">

# 📦 backup universal

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-80%2B-success.svg)

**sistema inteligente de backup para linux**

*porque perder dados é coisa do passado* 🚀

</div>

---

<div align="center">

## 💡 o que é isso?

</div>

Sistema completo e modular de backup que faz tudo pra você: compacta, organiza, limpa backups antigos e ainda restaura quando precisar.

**Versão 1.2** agora com **suite completa de testes automatizados** e **80%+ de cobertura de código**.

<br>

<div align="center">

## ✨ recursos principais

</div>

<table>
<tr>
<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/compress.png" width="64"/><br>
<b>Compressão Inteligente</b><br>
</td>

<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/verified-badge.png" width="64"/><br>
<b>Verificação de Integridade</b><br>
</td>

<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/delete-shield.png" width="64"/><br>
<b>Exclusões Inteligentes</b><br>
</td>

<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/database-restore.png" width="64"/><br>
<b>Restauração Fácil</b><br>
</td>
</tr>
</table>

<br>

<div align="center">

## 🚀 instalação rápida

</div>

```bash
git clone https://github.com/montezuma-p/backup-universal
cd backup-universal
cp config.json.example config.json
```

<br>

<div align="center">

## 💻 como usar

</div>

```bash
# Criar backup
python3 -m backup --criar /caminho/origem

# Listar backups disponíveis
python3 -m backup --listar

# Restaurar backup
python3 -m backup --restaurar

# Limpar backups antigos
python3 -m backup --limpar-antigos
```

<br>

<div align="center">

## ⚙️ configuração

</div>

Edite o arquivo `config.json` com suas preferências:

```json
{
  "paths": {
    "backup_destination": "~/.backups"
  },
  "retention_policy": {
    "max_backups_per_directory": 5,
    "max_age_days": 30
  },
  "compression": {
    "algorithm": "gzip"
  }
}
```

<br>

<div align="center">

## 🧪 testes

</div>

O projeto inclui uma suite completa de testes automatizados:

```bash
# Instalar dependências de teste
pip install -r requirements-dev.txt

# Rodar todos os testes
pytest

# Ver cobertura de código
pytest --cov=backup --cov-report=html
```

**229 testes** cobrindo todos os módulos principais com **81% de cobertura total**.

<br>

<div align="center">

## 📁 estrutura do projeto

</div>

```
.
├── backup.sh
├── cli.py
├── config.json.example
├── config.py
├── core
│   ├── backup_manager.py
│   ├── compression.py
│   ├── exclusion.py
│   ├── __init__.py
│   └── integrity.py
├── docs
│   ├── CONTRIBUINDO.md
│   └── ROADMAP.md
├── examples
│   ├── examples.py
│   └── README.md
├── __init__.py
├── LICENSE
├── __main__.py
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── restore
│   ├── __init__.py
│   └── restore_manager.py
├── setup.py
├── storage
│   ├── cleanup.py
│   ├── index.py
│   └── __init__.py
├── tests
│   ├── conftest.py
│   ├── e2e
│   ├── __init__.py
│   ├── integration
│   ├── tmp_debug2
│   │   └── restored.txt
│   └── unit
│       ├── conftest.py
│       ├── __init__.py
│       ├── test_backup_manager.py
│       ├── test_cleanup.py
│       ├── test_compression.py
│       ├── test_config.py
│       ├── test_exclusion.py
│       ├── test_file_utils.py
│       ├── test_formatters.py
│       ├── test_index.py
│       ├── test_integrity.py
│       └── test_restore_manager.py
└── utils
    ├── file_utils.py
    ├── formatters.py
    ├── __init__.py
    └── user_input.py

12 directories, 44 files
```

<br>

<div align="center">

## 🎯 exclusões automáticas

</div>

O sistema ignora automaticamente arquivos desnecessários:

- **Dependências**: `node_modules`, `__pycache__`, `venv`
- **Cache**: `*.cache`, `.pytest_cache`, `.npm`
- **Temporários**: `*.tmp`, `*.log`
- **Controle de versão**: `.git`, `.svn`
- **IDEs**: `.vscode`, `.idea`, `*.swp`
- **Builds**: `build`, `dist`, `target`

<br>

<div align="center">

## 🛠️ stack tecnológico

</div>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white"/>
<img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"/>
</p>

<br>

<div align="center">

## 🔮 roadmap

</div>

Veja o [ROADMAP.md](docs/ROADMAP.md) completo para os próximos passos.

**v1.2** ✅ Suite de testes automatizados  
**v1.3** 🚧 Testes de integração  
**v1.4** 📋 Integração com cloud storage

<br>

<div align="center">

## 📄 licença

</div>

<p align="center">
Este projeto está sob a licença MIT.<br>
Veja o arquivo <a href="LICENSE">LICENSE</a> para mais detalhes.
</p>

<br>

<div align="center">

## 👨‍💻 autor

<img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="80"/>

**Montezuma**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/montezuma-p)

---

### 🎉 bora fazer backup! 🎉

</div>

---

