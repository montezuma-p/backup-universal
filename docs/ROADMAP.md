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
- [x] **✨ Arquitetura modular (v1.1)**
- [x] **✨ Sistema de configuração via config.json (v1.1)**
- [x] **✨ Separação de responsabilidades em módulos (v1.1)**
- [x] **✨ Suite completa de testes automatizados (v1.2)**
- [x] **✨ Cobertura de código 80%+ (v1.2)**

---

## 🚀 próximos passos

### 🔧 **v1.1 - Configuração Flexível** ✅ **CONCLUÍDO!**

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3N3NXNqeGFhbWRlZGV4d2VkdXFjMnB6M3NlaGRhbDN5N2FzYndpMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tn33aiTi1jkl6H6/giphy.gif" width="250" align="right"/>

#### 📝 Sistema de configuração via JSON

- [x] **Criar `config.json`** na raiz do projeto
- [x] Mover diretórios hardcoded para configuração:
  - `default_backup_source`
  - `backup_destination`
- [x] Padrões de exclusão personalizáveis via config
- [x] Políticas de retenção configuráveis:
  - Número de backups por diretório
  - Dias para manter backups
  - Tamanho máximo total de backups
- [x] Formato padrão de compressão (tar/zip)
- [x] Nível de compressão padrão (0-9)
- [x] **Arquitetura modular completa**
- [x] **Separação em módulos especializados**

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

### 🧪 **v1.2 - Testes Automatizados** ✅ **CONCLUÍDO!**

<img src="https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif" width="200" align="right"/>

#### 🧪 Suite completa de testes

- [x] **Testes unitários para todos os módulos**
- [x] Cobertura de 80%+ do código
- [x] Testes para BackupManager
- [x] Testes para RestoreManager
- [x] Testes para sistema de exclusão
- [x] Testes para compressão e integridade
- [x] Testes para índice e cleanup
- [x] Testes para utilitários
- [x] Configuração pytest com coverage
- [x] Integração contínua (GitHub Actions)

**Benefícios:**
- ✅ Código mais confiável
- ✅ Refatoração segura
- ✅ Documentação viva
- ✅ Menos bugs em produção

---

### ☁️ **v1.3 - Testes de Integração** (Em Desenvolvimento)

<img src="https://media.giphy.com/media/26tn33aiTi1jkl6H6/giphy.gif" width="200" align="right"/>

#### 🔗 Testes end-to-end

- [ ] Testes de fluxo completo de backup
- [ ] Testes de restauração real
- [ ] Testes de limpeza automática
- [ ] Testes de cenários complexos
- [ ] Testes de performance
- [ ] Testes com dados reais

---

### ☁️ **v1.4 - Integração com Cloud** (Planejado)

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

**Última atualização:** 12 de novembro de 2025  
**Versão atual:** 1.2 ✨ **COM TESTES AUTOMATIZADOS**  
**Próxima release:** v1.3 (Testes de Integração)

</div>
