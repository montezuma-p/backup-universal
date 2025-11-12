#!/bin/bash
#
# Backup Universal - Script Launcher
# Wrapper simples para executar o sistema de backup modular
#

# Diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navega para o diretório pai e executa como módulo Python
cd "$(dirname "$SCRIPT_DIR")" || exit 1
python3 -m backup "$@"
