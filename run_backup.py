#!/usr/bin/env python3
"""
Script auxiliar para executar o backup de qualquer lugar
Wrapper para o módulo backup
"""

import sys
import os

# Adiciona o diretório pai ao path para permitir import do módulo backup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backup.cli import main

if __name__ == "__main__":
    main()
