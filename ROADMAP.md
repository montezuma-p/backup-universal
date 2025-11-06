# 🗺️ roadmap - backup universal

<div align="center">

<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXcydTZldm1rYWdvdDMyNmRhZjkzZ3hhNDA5aGszaXk1NDAxdG1qdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mWzDQcluZVlpm/giphy.gif" width="450"/>

### planejamento e próximos passos

_roadmap for continuous improvement_

</div>

---

## 🎯 visão geral

Este roadmap descreve as melhorias planejadas e futuras funcionalidades do **Backup Universal**.  
O objetivo é tornar o sistema cada vez mais robusto, flexível e integrado com soluções modernas.

---

## 📋 status do projeto

### ✅ **Implementado**

- [x] Backup completo de diretórios
- [x] Suporte para .tar.gz e .zip
- [x] Exclusões inteligentes com padrões
- [x] Índice JSON de backups
- [x] Detecção automática de tipo de projeto
- [x] Sistema de limpeza de backups antigos
- [x] Interface de restauração interativa
- [x] Hash MD5 para integridade
- [x] Estatísticas detalhadas de compressão
- [x] Modo silencioso para automação
- [x] Relatórios de progresso em tempo real

---

## 🚀 próximos passos

### 🔧 **v1.1 - Configuração Flexível** (Prioridade Alta)

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3N3NXNqeGFhbWRlZGV4d2VkdXFjMnB6M3NlaGRhbDN5N2FzYndpMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tn33aiTi1jkl6H6/giphy.gif" width="250" align="right"/>

#### 📝 Implementar sistema de configuração via JSON

- [ ] **Criar `config.json`** na raiz do projeto
- [ ] Mover diretórios hardcoded para configuração:
  - `area_trabalho` (atualmente `/home/montezuma`)
  - `dir_backups` (atualmente `~/.bin/data/backups/archives`)
- [ ] Padrões de exclusão personalizáveis via config
- [ ] Políticas de retenção configuráveis:
  - Número de backups por diretório
  - Dias para manter backups
  - Tamanho máximo total de backups
- [ ] Formato padrão de compressão (tar/zip)
- [ ] Nível de compressão padrão (0-9)

**Exemplo de `config.json`:**
```json
{
  "paths": {
    "default_backup_source": "/home/montezuma",
    "backup_destination": "~/.bin/data/backups/archives",
    "temp_dir": "/tmp/backup-universal"
  },
  "retention_policy": {
    "max_backups_per_directory": 5,
    "days_to_keep": 30,
    "max_total_size_gb": 50
  },
  "compression": {
    "default_format": "tar",
    "default_level": 6
  },
  "exclusion_patterns": {
    "custom": [
      "*.mp4",
      "*.mkv",
      "downloads",
      "temp"
    ]
  },
  "notifications": {
    "enabled": false,
    "email": "",
    "webhook_url": ""
  }
}
```

**Benefícios:**
- ✅ Configuração sem editar código
- ✅ Fácil personalização por usuário
- ✅ Portabilidade entre sistemas
- ✅ Versionamento de configurações

---

### ☁️ **v1.2 - Integração com Cloud** (Prioridade Alta)

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjhyN2N5Z3NrY21sZGN4ZHVhbm13ZGxlcHd0Y2lwZDc5OGY3OGZzayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LmNwrBhejkK9EFP504/giphy.gif" width="200" align="right"/>

#### ☁️ Sincronização automática com provedores de nuvem

- [ ] **Suporte para múltiplos provedores:**
  - AWS S3
  - Google Drive
  - Dropbox
  - OneDrive
  - Nextcloud/ownCloud (self-hosted)
  - Backblaze B2
- [ ] Upload automático após backup
- [ ] Sincronização incremental
- [ ] Verificação de integridade remota
- [ ] Download e restauração da nuvem
- [ ] Criptografia antes do upload
- [ ] Gerenciamento de credenciais seguro
- [ ] Status de sincronização no índice


---

## 🎯 metas de longo prazo

### 🌟 Visão: Tornar-se a ferramenta de backup definitiva para Linux

- **Simplicidade:** Uso trivial para iniciantes
- **Poder:** Recursos avançados para power users
- **Confiabilidade:** Backups que você pode confiar
- **Flexibilidade:** Configurável para qualquer cenário
- **Integração:** Funciona bem com outras ferramentas

---

## 🤝 contribuições

Quer ajudar a implementar alguma dessas features?

1. Escolha um item do roadmap
2. Abra uma issue discutindo a implementação
3. Faça um PR seguindo os padrões do projeto
4. Comemore! 🎉

<div align="center">

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTJ4dGxqM3Z4eWxmM3NqZGJ4eHZ5bjN0aGJ6YWplYWh1aDFxdHBoNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif" width="250"/>

### 🚀 **vamos construir o futuro dos backups juntos!**

_let's build the future of backups together!_

---

**Última atualização:** 05 de novembro de 2024  
**Versão atual:** 1.0  
**Próxima release:** v1.1 (config.json)

</div>
