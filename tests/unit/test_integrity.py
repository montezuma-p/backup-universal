"""
Testes Unitários - Módulo de Integridade
Testa cálculo de hashes e verificação de integridade
"""

import pytest
import importlib.util
from pathlib import Path

# Importa módulo diretamente do arquivo sem passar por __init__.py
spec = importlib.util.spec_from_file_location(
    "integrity",
    Path(__file__).parent.parent.parent / "core" / "integrity.py"
)
integrity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integrity)

IntegrityChecker = integrity.IntegrityChecker


class TestCalculateMD5:
    """Testes para calculate_md5()"""
    
    def test_md5_text_file(self, sample_text_file):
        """Testa MD5 de arquivo de texto"""
        hash_result = IntegrityChecker.calculate_md5(sample_text_file)
        assert hash_result is not None
        assert len(hash_result) == 32  # MD5 tem 32 caracteres hex
        assert hash_result.isalnum()
    
    def test_md5_binary_file(self, sample_binary_file):
        """Testa MD5 de arquivo binário"""
        hash_result = IntegrityChecker.calculate_md5(sample_binary_file)
        assert hash_result is not None
        assert len(hash_result) == 32
    
    def test_md5_same_content_same_hash(self, tmp_path):
        """Testa que mesmo conteúdo gera mesmo hash"""
        # Cria dois arquivos com mesmo conteúdo
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        content = "Hello World!\n"
        file1.write_text(content)
        file2.write_text(content)
        
        hash1 = IntegrityChecker.calculate_md5(file1)
        hash2 = IntegrityChecker.calculate_md5(file2)
        
        assert hash1 == hash2
    
    def test_md5_different_content(self, tmp_path):
        """Testa que conteúdos diferentes geram hashes diferentes"""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        file1.write_text("Hello World!")
        file2.write_text("Hello Python!")
        
        hash1 = IntegrityChecker.calculate_md5(file1)
        hash2 = IntegrityChecker.calculate_md5(file2)
        
        assert hash1 != hash2
    
    def test_md5_nonexistent_file(self, tmp_path):
        """Testa MD5 de arquivo inexistente (deve retornar None)"""
        nonexistent = tmp_path / "nonexistent.txt"
        hash_result = IntegrityChecker.calculate_md5(nonexistent)
        assert hash_result is None
    
    def test_md5_empty_file(self, tmp_path):
        """Testa MD5 de arquivo vazio"""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        hash_result = IntegrityChecker.calculate_md5(empty_file)
        assert hash_result is not None
        # Hash MD5 de arquivo vazio: d41d8cd98f00b204e9800998ecf8427e
        assert hash_result == "d41d8cd98f00b204e9800998ecf8427e"
    
    def test_md5_known_hash(self, tmp_path):
        """Testa MD5 com hash conhecido"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        hash_result = IntegrityChecker.calculate_md5(file)
        # Hash MD5 de "Hello World!\n"
        expected = "8ddd8be4b179a529afa5f2ffae4b9858"
        assert hash_result == expected


class TestCalculateSHA256:
    """Testes para calculate_sha256()"""
    
    def test_sha256_text_file(self, sample_text_file):
        """Testa SHA256 de arquivo de texto"""
        hash_result = IntegrityChecker.calculate_sha256(sample_text_file)
        assert hash_result is not None
        assert len(hash_result) == 64  # SHA256 tem 64 caracteres hex
        assert hash_result.isalnum()
    
    def test_sha256_binary_file(self, sample_binary_file):
        """Testa SHA256 de arquivo binário"""
        hash_result = IntegrityChecker.calculate_sha256(sample_binary_file)
        assert hash_result is not None
        assert len(hash_result) == 64
    
    def test_sha256_same_content_same_hash(self, tmp_path):
        """Testa que mesmo conteúdo gera mesmo hash"""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        content = "Hello World!\n"
        file1.write_text(content)
        file2.write_text(content)
        
        hash1 = IntegrityChecker.calculate_sha256(file1)
        hash2 = IntegrityChecker.calculate_sha256(file2)
        
        assert hash1 == hash2
    
    def test_sha256_different_content(self, tmp_path):
        """Testa que conteúdos diferentes geram hashes diferentes"""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        file1.write_text("Hello World!")
        file2.write_text("Hello Python!")
        
        hash1 = IntegrityChecker.calculate_sha256(file1)
        hash2 = IntegrityChecker.calculate_sha256(file2)
        
        assert hash1 != hash2
    
    def test_sha256_nonexistent_file(self, tmp_path):
        """Testa SHA256 de arquivo inexistente (deve retornar None)"""
        nonexistent = tmp_path / "nonexistent.txt"
        hash_result = IntegrityChecker.calculate_sha256(nonexistent)
        assert hash_result is None
    
    def test_sha256_empty_file(self, tmp_path):
        """Testa SHA256 de arquivo vazio"""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        hash_result = IntegrityChecker.calculate_sha256(empty_file)
        assert hash_result is not None
        # Hash SHA256 de arquivo vazio
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert hash_result == expected


class TestVerifyFile:
    """Testes para verify_file()"""
    
    def test_verify_md5_correct(self, tmp_path):
        """Testa verificação MD5 com hash correto"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        # Hash MD5 correto de "Hello World!\n"
        expected_hash = "8ddd8be4b179a529afa5f2ffae4b9858"
        
        assert IntegrityChecker.verify_file(file, expected_hash, 'md5') is True
    
    def test_verify_md5_incorrect(self, tmp_path):
        """Testa verificação MD5 com hash incorreto"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        wrong_hash = "0000000000000000000000000000000"
        
        assert IntegrityChecker.verify_file(file, wrong_hash, 'md5') is False
    
    def test_verify_sha256_correct(self, tmp_path):
        """Testa verificação SHA256 com hash correto"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        # Calcula hash real
        expected_hash = IntegrityChecker.calculate_sha256(file)
        
        assert IntegrityChecker.verify_file(file, expected_hash, 'sha256') is True
    
    def test_verify_sha256_incorrect(self, tmp_path):
        """Testa verificação SHA256 com hash incorreto"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        wrong_hash = "0" * 64
        
        assert IntegrityChecker.verify_file(file, wrong_hash, 'sha256') is False
    
    def test_verify_case_insensitive(self, tmp_path):
        """Testa que verificação é case-insensitive"""
        file = tmp_path / "test.txt"
        file.write_text("Hello World!\n")
        
        hash_lower = "8ddd8be4b179a529afa5f2ffae4b9858"
        hash_upper = "8DDD8BE4B179A529AFA5F2FFAE4B9858"
        hash_mixed = "8dDd8bE4B179a529afA5f2ffae4B9858"
        
        assert IntegrityChecker.verify_file(file, hash_lower, 'md5') is True
        assert IntegrityChecker.verify_file(file, hash_upper, 'md5') is True
        assert IntegrityChecker.verify_file(file, hash_mixed, 'md5') is True
    
    def test_verify_nonexistent_file(self, tmp_path):
        """Testa verificação de arquivo inexistente"""
        nonexistent = tmp_path / "nonexistent.txt"
        fake_hash = "8ddd8be4b179a529afa5f2ffae4b9858"
        
        assert IntegrityChecker.verify_file(nonexistent, fake_hash, 'md5') is False
    
    def test_verify_unsupported_algorithm(self, tmp_path):
        """Testa algoritmo não suportado"""
        file = tmp_path / "test.txt"
        file.write_text("Hello")
        
        with pytest.raises(ValueError, match="Algoritmo não suportado"):
            IntegrityChecker.verify_file(file, "somehash", 'sha512')


class TestCalculateHash:
    """Testes para calculate_hash() - método genérico"""
    
    def test_calculate_hash_md5(self, sample_text_file):
        """Testa cálculo genérico com MD5"""
        hash_result = IntegrityChecker.calculate_hash(sample_text_file, 'md5')
        assert hash_result is not None
        assert len(hash_result) == 32
    
    def test_calculate_hash_sha256(self, sample_text_file):
        """Testa cálculo genérico com SHA256"""
        hash_result = IntegrityChecker.calculate_hash(sample_text_file, 'sha256')
        assert hash_result is not None
        assert len(hash_result) == 64
    
    def test_calculate_hash_default_md5(self, sample_text_file):
        """Testa que MD5 é o padrão"""
        hash_md5 = IntegrityChecker.calculate_hash(sample_text_file, 'md5')
        hash_default = IntegrityChecker.calculate_hash(sample_text_file)
        
        assert hash_md5 == hash_default
    
    def test_calculate_hash_unsupported_algorithm(self, sample_text_file):
        """Testa algoritmo não suportado"""
        with pytest.raises(ValueError, match="Algoritmo não suportado"):
            IntegrityChecker.calculate_hash(sample_text_file, 'sha512')
    
    def test_calculate_hash_case_insensitive_algorithm(self, sample_text_file):
        """Testa que nome do algoritmo é case-insensitive"""
        hash_lower = IntegrityChecker.calculate_hash(sample_text_file, 'md5')
        hash_upper = IntegrityChecker.calculate_hash(sample_text_file, 'MD5')
        hash_mixed = IntegrityChecker.calculate_hash(sample_text_file, 'Md5')
        
        assert hash_lower == hash_upper == hash_mixed


class TestChunkSize:
    """Testes relacionados ao tamanho de chunk"""
    
    def test_chunk_size_constant(self):
        """Testa que CHUNK_SIZE está definido"""
        assert IntegrityChecker.CHUNK_SIZE == 4096
    
    def test_large_file_hash(self, tmp_path):
        """Testa hash de arquivo grande (maior que CHUNK_SIZE)"""
        large_file = tmp_path / "large.txt"
        
        # Cria arquivo de ~10KB (maior que 4KB chunk)
        content = "A" * 10240
        large_file.write_text(content)
        
        hash_result = IntegrityChecker.calculate_md5(large_file)
        assert hash_result is not None
        assert len(hash_result) == 32
