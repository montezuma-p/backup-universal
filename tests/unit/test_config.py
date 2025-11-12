"""
Testes Unitários - Módulo de Configuração
Testa gerenciamento de configurações
"""

import pytest
import json
import importlib.util
from pathlib import Path

# Importa módulo diretamente do arquivo
spec = importlib.util.spec_from_file_location(
    "config",
    Path(__file__).parent.parent.parent / "config.py"
)
config_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_mod)

Config = config_mod.Config


@pytest.fixture
def sample_config_data():
    """Dados de configuração de exemplo"""
    return {
        "paths": {
            "default_backup_source": "/home/user/projects",
            "backup_destination": "/tmp/test_backups",
            "temp_dir": "/tmp/backup-temp"
        },
        "retention_policy": {
            "max_backups_per_directory": 10,
            "days_to_keep": 60,
            "max_total_size_gb": 100
        },
        "compression": {
            "default_format": "tar",
            "default_level": 9
        },
        "exclusion_patterns": {
            "default": ["*.pyc", "*.tmp", "__pycache__"],
            "custom": ["*.log"]
        },
        "notifications": {
            "enabled": True,
            "email": "user@example.com",
            "webhook_url": "https://hooks.example.com/webhook"
        }
    }


@pytest.fixture
def config_file(tmp_path, sample_config_data):
    """Cria arquivo de configuração temporário"""
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as f:
        json.dump(sample_config_data, f, indent=2)
    return config_path


class TestConfigInit:
    """Testes de inicialização do Config"""
    
    def test_init_with_valid_config(self, config_file):
        """Testa inicialização com arquivo válido"""
        config = Config(config_file)
        assert config.config_path == config_file
    
    def test_init_missing_file(self, tmp_path):
        """Testa inicialização com arquivo inexistente"""
        nonexistent = tmp_path / "nonexistent.json"
        
        with pytest.raises(FileNotFoundError, match="Arquivo de configuração não encontrado"):
            Config(nonexistent)
    
    def test_init_corrupted_json(self, tmp_path):
        """Testa inicialização com JSON corrompido"""
        bad_config = tmp_path / "bad_config.json"
        bad_config.write_text("{ invalid json }")
        
        with pytest.raises(ValueError, match="Erro ao parsear config.json"):
            Config(bad_config)


class TestPathProperties:
    """Testes para propriedades de paths"""
    
    def test_default_backup_source(self, config_file):
        """Testa default_backup_source"""
        config = Config(config_file)
        assert config.default_backup_source == Path("/home/user/projects")
    
    def test_backup_destination(self, config_file):
        """Testa backup_destination"""
        config = Config(config_file)
        dest = config.backup_destination
        
        assert dest == Path("/tmp/test_backups")
        # Deve criar diretório automaticamente
        assert dest.exists()
    
    def test_temp_dir(self, config_file):
        """Testa temp_dir"""
        config = Config(config_file)
        assert config.temp_dir == Path("/tmp/backup-temp")
    
    def test_index_file(self, config_file):
        """Testa index_file (derivado de backup_destination)"""
        config = Config(config_file)
        expected = Path("/tmp/test_backups") / "indice_backups.json"
        assert config.index_file == expected


class TestRetentionPolicyProperties:
    """Testes para propriedades de retention_policy"""
    
    def test_max_backups_per_directory(self, config_file):
        """Testa max_backups_per_directory"""
        config = Config(config_file)
        assert config.max_backups_per_directory == 10
    
    def test_days_to_keep(self, config_file):
        """Testa days_to_keep"""
        config = Config(config_file)
        assert config.days_to_keep == 60
    
    def test_max_total_size_gb(self, config_file):
        """Testa max_total_size_gb"""
        config = Config(config_file)
        assert config.max_total_size_gb == 100
    
    def test_default_values(self, tmp_path):
        """Testa valores padrão quando não especificados"""
        minimal_config = tmp_path / "minimal.json"
        minimal_config.write_text('{"paths": {}}')
        
        config = Config(minimal_config)
        assert config.max_backups_per_directory == 5
        assert config.days_to_keep == 30
        assert config.max_total_size_gb == 50


class TestCompressionProperties:
    """Testes para propriedades de compression"""
    
    def test_default_format(self, config_file):
        """Testa default_format"""
        config = Config(config_file)
        assert config.default_format == "tar"
    
    def test_default_compression_level(self, config_file):
        """Testa default_compression_level"""
        config = Config(config_file)
        assert config.default_compression_level == 9
    
    def test_default_compression_values(self, tmp_path):
        """Testa valores padrão de compressão"""
        minimal_config = tmp_path / "minimal.json"
        minimal_config.write_text('{}')
        
        config = Config(minimal_config)
        assert config.default_format == "tar"
        assert config.default_compression_level == 6


class TestExclusionPatternsProperties:
    """Testes para propriedades de exclusion_patterns"""
    
    def test_default_exclusion_patterns(self, config_file):
        """Testa default_exclusion_patterns"""
        config = Config(config_file)
        patterns = config.default_exclusion_patterns
        
        assert "*.pyc" in patterns
        assert "*.tmp" in patterns
        assert "__pycache__" in patterns
    
    def test_custom_exclusion_patterns(self, config_file):
        """Testa custom_exclusion_patterns"""
        config = Config(config_file)
        patterns = config.custom_exclusion_patterns
        
        assert "*.log" in patterns
    
    def test_all_exclusion_patterns(self, config_file):
        """Testa all_exclusion_patterns (combina default + custom)"""
        config = Config(config_file)
        patterns = config.all_exclusion_patterns
        
        # Deve conter ambos
        assert "*.pyc" in patterns  # default
        assert "*.log" in patterns  # custom
        assert len(patterns) == 4
    
    def test_add_custom_pattern(self, config_file):
        """Testa add_custom_pattern()"""
        config = Config(config_file)
        
        config.add_custom_pattern("*.bak")
        
        assert "*.bak" in config.custom_exclusion_patterns
        
        # Recarrega do arquivo para verificar persistência
        config2 = Config(config_file)
        assert "*.bak" in config2.custom_exclusion_patterns
    
    def test_add_duplicate_pattern(self, config_file):
        """Testa adicionar padrão duplicado (não deve adicionar)"""
        config = Config(config_file)
        
        initial_count = len(config.custom_exclusion_patterns)
        config.add_custom_pattern("*.log")  # Já existe
        
        assert len(config.custom_exclusion_patterns) == initial_count
    
    def test_remove_custom_pattern(self, config_file):
        """Testa remove_custom_pattern()"""
        config = Config(config_file)
        
        config.remove_custom_pattern("*.log")
        
        assert "*.log" not in config.custom_exclusion_patterns
        
        # Verifica persistência
        config2 = Config(config_file)
        assert "*.log" not in config2.custom_exclusion_patterns
    
    def test_remove_nonexistent_pattern(self, config_file):
        """Testa remover padrão inexistente (não deve dar erro)"""
        config = Config(config_file)
        
        initial_count = len(config.custom_exclusion_patterns)
        config.remove_custom_pattern("*.nonexistent")
        
        assert len(config.custom_exclusion_patterns) == initial_count


class TestNotificationsProperties:
    """Testes para propriedades de notifications"""
    
    def test_notifications_enabled(self, config_file):
        """Testa notifications_enabled"""
        config = Config(config_file)
        assert config.notifications_enabled is True
    
    def test_notification_email(self, config_file):
        """Testa notification_email"""
        config = Config(config_file)
        assert config.notification_email == "user@example.com"
    
    def test_notification_webhook(self, config_file):
        """Testa notification_webhook"""
        config = Config(config_file)
        assert config.notification_webhook == "https://hooks.example.com/webhook"
    
    def test_default_notifications(self, tmp_path):
        """Testa valores padrão de notificações"""
        minimal_config = tmp_path / "minimal.json"
        minimal_config.write_text('{}')
        
        config = Config(minimal_config)
        assert config.notifications_enabled is False
        assert config.notification_email == ''
        assert config.notification_webhook == ''


class TestUtilityMethods:
    """Testes para métodos utilitários"""
    
    def test_get_existing_key(self, config_file):
        """Testa get() com chave existente"""
        config = Config(config_file)
        
        value = config.get('compression')
        assert value is not None
        assert 'default_format' in value
    
    def test_get_nonexistent_key(self, config_file):
        """Testa get() com chave inexistente"""
        config = Config(config_file)
        
        value = config.get('nonexistent')
        assert value is None
    
    def test_get_with_default(self, config_file):
        """Testa get() com valor padrão"""
        config = Config(config_file)
        
        value = config.get('nonexistent', 'default_value')
        assert value == 'default_value'
    
    def test_set_and_get(self, config_file):
        """Testa set() e get()"""
        config = Config(config_file)
        
        config.set('custom_key', 'custom_value')
        assert config.get('custom_key') == 'custom_value'
        
        # Verifica persistência
        config2 = Config(config_file)
        assert config2.get('custom_key') == 'custom_value'


class TestSaveAndLoad:
    """Testes para save() e load()"""
    
    def test_save_and_reload(self, config_file, sample_config_data):
        """Testa salvar e recarregar configuração"""
        config = Config(config_file)
        
        # Modifica
        config._config['new_key'] = 'new_value'
        config.save()
        
        # Recarrega
        config2 = Config(config_file)
        assert config2.get('new_key') == 'new_value'
    
    def test_load_preserves_structure(self, config_file):
        """Testa que load() preserva estrutura"""
        config = Config(config_file)
        
        # Recarrega
        config.load()
        
        assert 'paths' in config._config
        assert 'retention_policy' in config._config
        assert 'compression' in config._config


class TestRepr:
    """Testes para __repr__()"""
    
    def test_repr(self, config_file):
        """Testa representação string"""
        config = Config(config_file)
        repr_str = repr(config)
        
        assert "Config" in repr_str
        assert str(config_file) in repr_str


class TestEdgeCases:
    """Testes de casos extremos"""
    
    def test_empty_config(self, tmp_path):
        """Testa com configuração vazia"""
        empty_config = tmp_path / "empty.json"
        empty_config.write_text('{}')
        
        config = Config(empty_config)
        
        # Deve usar valores padrão
        assert config.max_backups_per_directory == 5
        assert config.default_format == "tar"
    
    def test_path_expansion(self, tmp_path):
        """Testa expansão de ~ em paths"""
        config_data = {
            "paths": {
                "backup_destination": "~/test_backups"
            }
        }
        
        config_path = tmp_path / "config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f)
        
        config = Config(config_path)
        dest = config.default_backup_source
        
        # ~ deve ser expandido
        assert "~" not in str(dest)
