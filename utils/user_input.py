#!/usr/bin/env python3
"""
User Input Utilities
Funções auxiliares para entrada de dados do usuário
"""

from typing import Optional


def safe_input(prompt: str, cancel_msg: str = "❌ Operação cancelada pelo usuário.") -> Optional[str]:
    """
    Input seguro que trata Ctrl+C (KeyboardInterrupt) elegantemente.
    
    Args:
        prompt: Mensagem a ser exibida ao usuário
        cancel_msg: Mensagem exibida quando usuário pressiona Ctrl+C
    
    Returns:
        String digitada pelo usuário ou None se cancelado (Ctrl+C)
    
    Examples:
        >>> resposta = safe_input("Digite algo: ")
        >>> if resposta is None:
        ...     print("Cancelado!")
        ... else:
        ...     print(f"Você digitou: {resposta}")
    """
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print(f"\n{cancel_msg}")
        return None
