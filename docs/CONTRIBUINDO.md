# 🤝 Contribuindo

## 🛠️ Configuração do Ambiente

### 1. Clone o Repositório
```bash
git clone https://github.com/montezuma-p/backup-universal.git
cd backup-universal
```

### 2. Crie uma Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as Dependências

**Dependências principais:**
```bash
pip install -r requirements.txt
```

**Dependências de desenvolvimento (testes, linting, formatação):**
```bash
pip install -r requirements-dev.txt
```

## 🧪 Executando os Testes

### Todos os testes
```bash
pytest
```

### Por tipo
```bash
pytest -m unit           # Testes unitários
pytest -m integration    # Testes de integração
pytest -m e2e           # Testes end-to-end
```

### Com cobertura
```bash
pytest --cov=backup --cov-report=html
```

## 🎨 Qualidade de Código

### Formatação
```bash
black .
isort .
```

### Linting
```bash
pylint backup/
flake8 backup/
mypy backup/
```

## 📝 Estrutura de Testes

```
tests/
├── unit/           # Testes de módulos isolados
├── integration/    # Testes de múltiplos módulos
└── e2e/           # Testes CLI completos
```

## 🚀 Workflow Sugerido

1. Crie uma branch: `git checkout -b minha-feature`
2. Faça suas alterações
3. Execute os testes: `pytest`
4. Formate o código: `black . && isort .`
5. Commit: `git commit -m "feat: minha feature"`
6. Push: `git push origin minha-feature`
7. Abra um Pull Request

## 💡 Dicas

- Use `pytest -v` para output detalhado
- Use `pytest -k nome_teste` para rodar teste específico
- Use `pytest --lf` para rodar apenas testes que falharam
- Mantenha cobertura acima de 80%

---

**Dúvidas?** Abra uma issue! 🎯
