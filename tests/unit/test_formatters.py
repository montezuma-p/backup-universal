"""
Testes Unitários - Módulo de Formatadores
Testa funções puras de formatação
"""

import pytest
import importlib.util
from datetime import datetime
from pathlib import Path

# Importa módulo diretamente do arquivo sem passar por __init__.py
spec = importlib.util.spec_from_file_location(
    "formatters",
    Path(__file__).parent.parent.parent / "utils" / "formatters.py"
)
formatters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(formatters)

format_bytes = formatters.format_bytes
format_date = formatters.format_date
format_compression_rate = formatters.format_compression_rate
format_progress = formatters.format_progress
format_number = formatters.format_number
truncate_string = formatters.truncate_string


class TestFormatBytes:
    """Testes para format_bytes()"""
    
    def test_bytes(self):
        """Testa formatação de bytes"""
        assert format_bytes(100) == "100.0 B"
        assert format_bytes(0) == "0.0 B"
        assert format_bytes(1) == "1.0 B"
    
    def test_kilobytes(self):
        """Testa formatação de kilobytes"""
        assert format_bytes(1024) == "1.0 KB"
        assert format_bytes(1536) == "1.5 KB"
        assert format_bytes(2048) == "2.0 KB"
    
    def test_megabytes(self):
        """Testa formatação de megabytes"""
        assert format_bytes(1048576) == "1.0 MB"
        assert format_bytes(5242880) == "5.0 MB"
        assert format_bytes(10485760) == "10.0 MB"
    
    def test_gigabytes(self):
        """Testa formatação de gigabytes"""
        assert format_bytes(1073741824) == "1.0 GB"
        assert format_bytes(2147483648) == "2.0 GB"
    
    def test_terabytes(self):
        """Testa formatação de terabytes"""
        assert format_bytes(1099511627776) == "1.0 TB"
    
    def test_float_input(self):
        """Testa entrada com float"""
        assert format_bytes(1024.5) == "1.0 KB"
        assert format_bytes(1536.7) == "1.5 KB"


class TestFormatDate:
    """Testes para format_date()"""
    
    def test_default_format(self):
        """Testa formato padrão"""
        date = datetime(2025, 11, 12, 15, 30, 45)
        assert format_date(date) == "12/11/2025 15:30:45"
    
    def test_custom_format_date_only(self):
        """Testa formato customizado - apenas data"""
        date = datetime(2025, 11, 12, 15, 30, 45)
        assert format_date(date, "%Y-%m-%d") == "2025-11-12"
    
    def test_custom_format_time_only(self):
        """Testa formato customizado - apenas hora"""
        date = datetime(2025, 11, 12, 15, 30, 45)
        assert format_date(date, "%H:%M:%S") == "15:30:45"
    
    def test_custom_format_iso(self):
        """Testa formato ISO"""
        date = datetime(2025, 11, 12, 15, 30, 45)
        assert format_date(date, "%Y-%m-%dT%H:%M:%S") == "2025-11-12T15:30:45"


class TestFormatCompressionRate:
    """Testes para format_compression_rate()"""
    
    def test_no_compression(self):
        """Testa sem compressão (mesmos tamanhos)"""
        assert format_compression_rate(1000, 1000) == 0.0
    
    def test_50_percent_compression(self):
        """Testa 50% de compressão"""
        assert format_compression_rate(1000, 500) == 50.0
    
    def test_90_percent_compression(self):
        """Testa 90% de compressão"""
        assert format_compression_rate(1000, 100) == 90.0
    
    def test_25_percent_compression(self):
        """Testa 25% de compressão"""
        assert format_compression_rate(1000, 750) == 25.0
    
    def test_zero_original_size(self):
        """Testa com tamanho original zero"""
        assert format_compression_rate(0, 0) == 0.0
        assert format_compression_rate(0, 100) == 0.0
    
    def test_large_numbers(self):
        """Testa com números grandes"""
        original = 1073741824  # 1 GB
        compressed = 536870912  # 512 MB
        assert format_compression_rate(original, compressed) == 50.0


class TestFormatProgress:
    """Testes para format_progress()"""
    
    def test_zero_progress(self):
        """Testa 0% de progresso"""
        assert format_progress(0, 100) == "0.0%"
    
    def test_half_progress(self):
        """Testa 50% de progresso"""
        assert format_progress(50, 100) == "50.0%"
    
    def test_full_progress(self):
        """Testa 100% de progresso"""
        assert format_progress(100, 100) == "100.0%"
    
    def test_decimal_progress(self):
        """Testa progresso com decimais"""
        assert format_progress(33, 100) == "33.0%"
        assert format_progress(66, 100) == "66.0%"
    
    def test_zero_total(self):
        """Testa com total zero"""
        assert format_progress(0, 0) == "0.0%"
        assert format_progress(50, 0) == "0.0%"
    
    def test_small_numbers(self):
        """Testa com números pequenos"""
        assert format_progress(1, 3) == "33.3%"
        assert format_progress(2, 3) == "66.7%"


class TestFormatNumber:
    """Testes para format_number()"""
    
    def test_small_numbers(self):
        """Testa números pequenos (sem separador)"""
        assert format_number(0) == "0"
        assert format_number(100) == "100"
        assert format_number(999) == "999"
    
    def test_thousands(self):
        """Testa milhares"""
        assert format_number(1000) == "1,000"
        assert format_number(5000) == "5,000"
        assert format_number(9999) == "9,999"
    
    def test_millions(self):
        """Testa milhões"""
        assert format_number(1000000) == "1,000,000"
        assert format_number(5500000) == "5,500,000"
    
    def test_billions(self):
        """Testa bilhões"""
        assert format_number(1000000000) == "1,000,000,000"


class TestTruncateString:
    """Testes para truncate_string()"""
    
    def test_no_truncation_needed(self):
        """Testa quando não precisa truncar"""
        text = "Hello World"
        assert truncate_string(text, 50) == "Hello World"
        assert truncate_string(text, 11) == "Hello World"
    
    def test_exact_length(self):
        """Testa quando texto tem exatamente o tamanho máximo"""
        text = "Hello"
        assert truncate_string(text, 5) == "Hello"
    
    def test_truncation_default_suffix(self):
        """Testa truncamento com sufixo padrão"""
        text = "This is a very long text that needs to be truncated"
        result = truncate_string(text, 20)
        assert len(result) <= 20 + 3  # 20 + len("...")
        assert result.endswith("...")
    
    def test_truncation_custom_suffix(self):
        """Testa truncamento com sufixo customizado"""
        text = "This is a very long text"
        result = truncate_string(text, 10, suffix=">>>")
        assert result.endswith(">>>")
    
    def test_empty_string(self):
        """Testa string vazia"""
        assert truncate_string("", 10) == ""
    
    def test_very_short_max_length(self):
        """Testa com tamanho máximo muito curto"""
        text = "Hello World"
        result = truncate_string(text, 3)
        assert len(result) <= 6  # 3 + len("...")
