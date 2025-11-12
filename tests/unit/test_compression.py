"""
Testes Unitários - Módulo de Compressão
Testa compressores tar.gz e zip
"""

import pytest
import tarfile
import zipfile
import importlib.util
from pathlib import Path

# Importa módulo diretamente do arquivo
spec = importlib.util.spec_from_file_location(
    "compression",
    Path(__file__).parent.parent.parent / "core" / "compression.py"
)
compression_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compression_mod)

TarCompressor = compression_mod.TarCompressor
ZipCompressor = compression_mod.ZipCompressor
get_compressor = compression_mod.get_compressor

# Importa ExclusionFilter para testes
spec_excl = importlib.util.spec_from_file_location(
    "exclusion",
    Path(__file__).parent.parent.parent / "core" / "exclusion.py"
)
exclusion_mod = importlib.util.module_from_spec(spec_excl)
spec_excl.loader.exec_module(exclusion_mod)
ExclusionFilter = exclusion_mod.ExclusionFilter


@pytest.fixture
def source_dir(tmp_path):
    """Cria diretório de origem com arquivos para testar compressão"""
    source = tmp_path / "source"
    source.mkdir()
    
    # Arquivos normais
    (source / "file1.txt").write_text("conteúdo 1")
    (source / "file2.py").write_text("print('hello')")
    (source / "README.md").write_text("# Project")
    
    # Subdiretório
    subdir = source / "subdir"
    subdir.mkdir()
    (subdir / "nested.txt").write_text("arquivo aninhado")
    
    # Arquivos que devem ser excluídos
    (source / "file.pyc").write_text("bytecode")
    (source / "temp.tmp").write_text("temp")
    
    # Diretório que deve ser excluído
    pycache = source / "__pycache__"
    pycache.mkdir()
    (pycache / "cache.pyc").write_text("cache")
    
    return source


@pytest.fixture
def simple_exclusion_filter():
    """Filtro de exclusão simples para testes"""
    return ExclusionFilter(['*.pyc', '*.tmp', '__pycache__'])


class TestTarCompressor:
    """Testes para TarCompressor"""
    
    def test_extension(self):
        """Testa propriedade extension"""
        compressor = TarCompressor()
        assert compressor.extension == ".tar.gz"
    
    def test_compress_basic(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa compressão básica"""
        compressor = TarCompressor()
        output = tmp_path / "backup.tar.gz"
        
        total_files, excluded_files, excluded_dirs = compressor.compress(
            source_dir,
            output,
            simple_exclusion_filter
        )
        
        # Verifica que arquivo foi criado
        assert output.exists()
        assert output.stat().st_size > 0
        
        # Verifica contadores
        assert total_files >= 3  # file1.txt, file2.py, README.md, nested.txt
        assert excluded_files >= 2  # file.pyc, temp.tmp
        assert excluded_dirs >= 1  # __pycache__
    
    def test_compress_with_callback(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa compressão com callback de progresso"""
        compressor = TarCompressor()
        output = tmp_path / "backup.tar.gz"
        
        progress_calls = []
        
        def progress_callback(count):
            progress_calls.append(count)
        
        compressor.compress(
            source_dir,
            output,
            simple_exclusion_filter,
            progress_callback=progress_callback
        )
        
        # Callback deve ter sido chamado
        assert len(progress_calls) > 0
    
    def test_compress_different_levels(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa diferentes níveis de compressão"""
        compressor = TarCompressor()
        
        output_low = tmp_path / "backup_low.tar.gz"
        output_high = tmp_path / "backup_high.tar.gz"
        
        compressor.compress(source_dir, output_low, simple_exclusion_filter, compression_level=1)
        compressor.compress(source_dir, output_high, simple_exclusion_filter, compression_level=9)
        
        # Nível 9 deve gerar arquivo menor ou igual
        assert output_high.stat().st_size <= output_low.stat().st_size
    
    def test_decompress(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa descompressão"""
        compressor = TarCompressor()
        archive = tmp_path / "backup.tar.gz"
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        
        # Comprime
        compressor.compress(source_dir, archive, simple_exclusion_filter)
        
        # Descomprime
        compressor.decompress(archive, extract_dir)
        
        # Verifica que arquivos foram extraídos
        extracted_source = extract_dir / source_dir.name
        assert extracted_source.exists()
        assert (extracted_source / "file1.txt").exists()
        assert (extracted_source / "README.md").exists()
    
    def test_compress_preserves_structure(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa que estrutura de diretórios é preservada"""
        compressor = TarCompressor()
        archive = tmp_path / "backup.tar.gz"
        
        compressor.compress(source_dir, archive, simple_exclusion_filter)
        
        # Verifica conteúdo do arquivo
        with tarfile.open(archive, 'r:gz') as tar:
            names = tar.getnames()
            # Deve conter subdir/nested.txt
            assert any('subdir' in name and 'nested.txt' in name for name in names)


class TestZipCompressor:
    """Testes para ZipCompressor"""
    
    def test_extension(self):
        """Testa propriedade extension"""
        compressor = ZipCompressor()
        assert compressor.extension == ".zip"
    
    def test_compress_basic(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa compressão básica"""
        compressor = ZipCompressor()
        output = tmp_path / "backup.zip"
        
        total_files, excluded_files, excluded_dirs = compressor.compress(
            source_dir,
            output,
            simple_exclusion_filter
        )
        
        # Verifica que arquivo foi criado
        assert output.exists()
        assert output.stat().st_size > 0
        
        # Verifica contadores
        assert total_files >= 3
        assert excluded_files >= 2
        assert excluded_dirs >= 1
    
    def test_compress_with_callback(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa compressão com callback de progresso"""
        compressor = ZipCompressor()
        output = tmp_path / "backup.zip"
        
        progress_calls = []
        
        def progress_callback(count):
            progress_calls.append(count)
        
        compressor.compress(
            source_dir,
            output,
            simple_exclusion_filter,
            progress_callback=progress_callback
        )
        
        assert len(progress_calls) > 0
    
    def test_decompress(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa descompressão"""
        compressor = ZipCompressor()
        archive = tmp_path / "backup.zip"
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        
        # Comprime
        compressor.compress(source_dir, archive, simple_exclusion_filter)
        
        # Descomprime
        compressor.decompress(archive, extract_dir)
        
        # Verifica que arquivos foram extraídos
        extracted_source = extract_dir / source_dir.name
        assert extracted_source.exists()
        assert (extracted_source / "file1.txt").exists()
    
    def test_compress_preserves_structure(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa que estrutura de diretórios é preservada"""
        compressor = ZipCompressor()
        archive = tmp_path / "backup.zip"
        
        compressor.compress(source_dir, archive, simple_exclusion_filter)
        
        # Verifica conteúdo do arquivo
        with zipfile.ZipFile(archive, 'r') as zipf:
            names = zipf.namelist()
            # Deve conter subdir/nested.txt
            assert any('subdir' in name and 'nested.txt' in name for name in names)


class TestGetCompressor:
    """Testes para get_compressor() factory function"""
    
    def test_get_tar_compressor(self):
        """Testa obter compressor tar"""
        compressor = get_compressor('tar')
        assert isinstance(compressor, TarCompressor)
        assert compressor.extension == ".tar.gz"
    
    def test_get_zip_compressor(self):
        """Testa obter compressor zip"""
        compressor = get_compressor('zip')
        assert isinstance(compressor, ZipCompressor)
        assert compressor.extension == ".zip"
    
    def test_get_tar_case_insensitive(self):
        """Testa que formato é case-insensitive"""
        compressor1 = get_compressor('TAR')
        compressor2 = get_compressor('Tar')
        compressor3 = get_compressor('tar')
        
        assert all(isinstance(c, TarCompressor) for c in [compressor1, compressor2, compressor3])
    
    def test_get_zip_case_insensitive(self):
        """Testa que formato é case-insensitive"""
        compressor1 = get_compressor('ZIP')
        compressor2 = get_compressor('Zip')
        
        assert all(isinstance(c, ZipCompressor) for c in [compressor1, compressor2])
    
    def test_unsupported_format(self):
        """Testa formato não suportado"""
        with pytest.raises(ValueError, match="Formato não suportado"):
            get_compressor('rar')
        
        with pytest.raises(ValueError, match="Formato não suportado"):
            get_compressor('7z')


class TestCompressionComparison:
    """Testes comparativos entre compressores"""
    
    def test_both_compress_same_files(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa que ambos compressores processam mesmo número de arquivos"""
        tar_comp = TarCompressor()
        zip_comp = ZipCompressor()
        
        tar_out = tmp_path / "backup.tar.gz"
        zip_out = tmp_path / "backup.zip"
        
        tar_stats = tar_comp.compress(source_dir, tar_out, simple_exclusion_filter)
        zip_stats = zip_comp.compress(source_dir, zip_out, simple_exclusion_filter)
        
        # Devem processar mesmos arquivos
        assert tar_stats[0] == zip_stats[0]  # total_files
        assert tar_stats[1] == zip_stats[1]  # excluded_files
        assert tar_stats[2] == zip_stats[2]  # excluded_dirs
    
    def test_both_preserve_content(self, source_dir, tmp_path, simple_exclusion_filter):
        """Testa que ambos preservam conteúdo dos arquivos"""
        tar_comp = TarCompressor()
        zip_comp = ZipCompressor()
        
        tar_archive = tmp_path / "backup.tar.gz"
        zip_archive = tmp_path / "backup.zip"
        
        tar_extract = tmp_path / "tar_extracted"
        zip_extract = tmp_path / "zip_extracted"
        tar_extract.mkdir()
        zip_extract.mkdir()
        
        # Comprime e descomprime com ambos
        tar_comp.compress(source_dir, tar_archive, simple_exclusion_filter)
        zip_comp.compress(source_dir, zip_archive, simple_exclusion_filter)
        
        tar_comp.decompress(tar_archive, tar_extract)
        zip_comp.decompress(zip_archive, zip_extract)
        
        # Verifica que conteúdo é igual
        tar_file = tar_extract / source_dir.name / "file1.txt"
        zip_file = zip_extract / source_dir.name / "file1.txt"
        
        assert tar_file.read_text() == zip_file.read_text()


class TestEmptyDirectory:
    """Testes com diretório vazio"""
    
    def test_compress_empty_directory_tar(self, tmp_path, simple_exclusion_filter):
        """Testa compressão de diretório vazio com tar"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        compressor = TarCompressor()
        output = tmp_path / "backup.tar.gz"
        
        total_files, excluded_files, excluded_dirs = compressor.compress(
            empty_dir,
            output,
            simple_exclusion_filter
        )
        
        assert total_files == 0
        assert output.exists()
    
    def test_compress_empty_directory_zip(self, tmp_path, simple_exclusion_filter):
        """Testa compressão de diretório vazio com zip"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        compressor = ZipCompressor()
        output = tmp_path / "backup.zip"
        
        total_files, excluded_files, excluded_dirs = compressor.compress(
            empty_dir,
            output,
            simple_exclusion_filter
        )
        
        assert total_files == 0
        assert output.exists()
