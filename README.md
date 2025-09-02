# SCRAP_SAM

Sistema de scraping e análise de dados do SAM (Sistema de Administração de Manutenção) da Itaipu Binacional.

## 📋 Descrição

Este projeto automatiza a coleta e análise de dados de SSAs (Solicitações de Serviço de Atividades) do sistema SAM da Itaipu, fornecendo dashboards interativos para visualização e análise dos dados.

## 🏗️ Estrutura do Projeto

```
SCRAP_SAM/
├── src/                    # Código fonte
│   ├── scrapers/          # Scripts de scraping
│   ├── dashboard/         # Interface web e visualizações
│   └── utils/             # Utilitários e helpers
├── config/                # Configurações
├── tests/                 # Testes
├── docs/                  # Documentação
├── downloads/             # Arquivos baixados
├── drivers/               # Web drivers
└── logs/                  # Arquivos de log
```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd SCRAP_SAM
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Instale os navegadores do Playwright:
```bash
playwright install
```

## 📖 Uso

### Scraping
```bash
python src/scrapers/scrap_SAM.py
```

### Dashboard
```bash
python src/dashboard/Dashboard_SM.py
```

## 🔧 Configuração

As configurações principais estão em `config/settings.py`. Você pode ajustar:
- Timeouts de scraping
- Caminhos de drivers
- Configurações do dashboard
- URLs de destino

## 📋 Dependências

- pandas: Manipulação de dados
- selenium: Automação web
- dash: Framework web
- playwright: Automação web moderna
- beautifulsoup4: Parsing HTML

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## ⚠️ Avisos

- Este projeto é destinado apenas para uso interno da Itaipu Binacional
- Respeite os termos de serviço do sistema SAM
- Use com responsabilidade para evitar sobrecarga do sistema
