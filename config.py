"""
Módulo de Configuração
Gerencia o carregamento e validação de configurações do sistema de backup.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class Config:
    """Gerenciador de configurações do sistema de backup"""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.json"
    
    def __init__(self, config_path: Path = None):
        """
        Inicializa o gerenciador de configuração
        
        Args:
            config_path: Caminho para o arquivo config.json (opcional)
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Dict[str, Any] = {}
        self.load()
        
    def load(self) -> None:
        """Carrega configurações do arquivo JSON"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.config_path}\n"
                f"Execute o script de instalação ou crie o config.json manualmente."
            )
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao parsear config.json: {e}")
    
    def save(self) -> None:
        """Salva configurações no arquivo JSON"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    # === Paths ===
    
    @property
    def default_backup_source(self) -> Path:
        """Diretório padrão de origem para backup"""
        path = self._config.get('paths', {}).get('default_backup_source', '/home/montezuma')
        return Path(path).expanduser()
    
    @property
    def backup_destination(self) -> Path:
        """Diretório onde os backups serão armazenados"""
        path = self._config.get('paths', {}).get('backup_destination', '~/.bin/data/backups/archives')
        dest = Path(path).expanduser()
        dest.mkdir(parents=True, exist_ok=True)
        return dest
    
    @property
    def temp_dir(self) -> Path:
        """Diretório temporário para operações"""
        path = self._config.get('paths', {}).get('temp_dir', '/tmp/backup-universal')
        return Path(path)
    
    @property
    def index_file(self) -> Path:
        """Arquivo de índice de backups"""
        return self.backup_destination / "indice_backups.json"
    
    # === Retention Policy ===
    
    @property
    def max_backups_per_directory(self) -> int:
        """Número máximo de backups por diretório"""
        return self._config.get('retention_policy', {}).get('max_backups_per_directory', 5)
    
    @property
    def days_to_keep(self) -> int:
        """Dias para manter backups"""
        return self._config.get('retention_policy', {}).get('days_to_keep', 30)
    
    @property
    def max_total_size_gb(self) -> int:
        """Tamanho máximo total de backups em GB"""
        return self._config.get('retention_policy', {}).get('max_total_size_gb', 50)
    
    # === Compression ===
    
    @property
    def default_format(self) -> str:
        """Formato padrão de compressão (tar ou zip)"""
        return self._config.get('compression', {}).get('default_format', 'tar')
    
    @property
    def default_compression_level(self) -> int:
        """Nível de compressão padrão (0-9)"""
        return self._config.get('compression', {}).get('default_level', 6)
    
    # === Exclusion Patterns ===
    
    @property
    def default_exclusion_patterns(self) -> List[str]:
        """Padrões de exclusão padrão"""
        return self._config.get('exclusion_patterns', {}).get('default', [])
    
    @property
    def custom_exclusion_patterns(self) -> List[str]:
        """Padrões de exclusão customizados"""
        return self._config.get('exclusion_patterns', {}).get('custom', [])
    
    @property
    def all_exclusion_patterns(self) -> List[str]:
        """Todos os padrões de exclusão (default + custom)"""
        return self.default_exclusion_patterns + self.custom_exclusion_patterns
    
    def add_custom_pattern(self, pattern: str) -> None:
        """Adiciona um padrão customizado de exclusão"""
        if pattern not in self.custom_exclusion_patterns:
            self._config.setdefault('exclusion_patterns', {}).setdefault('custom', []).append(pattern)
            self.save()
    
    def remove_custom_pattern(self, pattern: str) -> None:
        """Remove um padrão customizado de exclusão"""
        custom = self._config.get('exclusion_patterns', {}).get('custom', [])
        if pattern in custom:
            custom.remove(pattern)
            self.save()
    
    # === Notifications ===
    
    @property
    def notifications_enabled(self) -> bool:
        """Se notificações estão habilitadas"""
        return self._config.get('notifications', {}).get('enabled', False)
    
    @property
    def notification_email(self) -> str:
        """Email para notificações"""
        return self._config.get('notifications', {}).get('email', '')
    
    @property
    def notification_webhook(self) -> str:
        """Webhook para notificações"""
        return self._config.get('notifications', {}).get('webhook_url', '')
    
    # === Utilities ===
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor da configuração"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Define um valor na configuração"""
        self._config[key] = value
        self.save()
    
    def __repr__(self) -> str:
        return f"<Config: {self.config_path}>"
