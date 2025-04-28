# Sistema de Ingestão de Dados de Criptomoedas

## Visão Geral
Este projeto é um sistema de ingestão de dados de criptomoedas que coleta, processa e armazena dados do mercado de criptomoedas utilizando a API CoinCap. Foi projetado para fornecer uma solução confiável e escalável para acompanhar preços e informações do mercado de criptomoedas.

## Estrutura do Projeto
```
.
├── src/                    # Diretório do código fonte
│   ├── client/            # Implementações dos clientes de API
│   ├── model/             # Modelos e esquemas de dados
│   ├── repository/        # Camada de acesso ao banco de dados
│   ├── service/           # Camada de lógica de negócios
│   ├── util/              # Funções e utilitários auxiliares
│   └── main.py            # Ponto de entrada da aplicação
├── tests/                 # Suíte de testes
├── terraform/             # Infraestrutura Terraform GCP
├── .github/              # Configuração do GitHub Actions
├── pyproject.toml        # Dependências e configuração do projeto
└── poetry.lock          # Dependências travadas
```

## Principais Funcionalidades
- **Coleta de Dados**: Busca dados de criptomoedas da API CoinCap
- **Dados Históricos**: Coleta histórico diário de preços para criptomoedas específicas
- **Dados de Mercado**: Coleta informações de mercado incluindo dados de exchanges e volumes de negociação
- **Atualizações Incrementais**: Ingestão inteligente que busca apenas dados novos
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e logging
- **Integração com Banco de Dados**: Persistência de dados baseada em ORM com SQLAlchemy
- **Operações Assíncronas**: Chamadas de API assíncronas para melhor performance

## Stack Tecnológico
- **Python 3.12.2**
- **SQLAlchemy**: ORM e toolkit de banco de dados
- **Poetry**: Gerenciamento de dependências
- **Pydantic**: Validação de dados
- **Structlog**: Logging estruturado
- **Terraform**: Gerenciamento de infraestrutura (GCP)

## Estratégia de Implementação
O projeto segue uma abordagem de arquitetura limpa com clara separação de responsabilidades:

1. **Camada de Cliente**: Gerencia a comunicação com a API CoinCap
2. **Camada de Serviço**: Implementa a lógica de negócios e processamento de dados
3. **Camada de Repositório**: Gerencia operações de banco de dados
4. **Camada de Modelo**: Define estruturas e esquemas de dados

## Uso
O sistema pode ser configurado para:
- Buscar dados históricos de preços para criptomoedas específicas
- Coletar dados de mercado de várias exchanges
- Controlar parâmetros de ingestão de dados (intervalos de datas, limites, etc.)

Exemplo de uso:
```python
# Ingerir dados históricos e de mercado
assets = ["bitcoin", "ethereum", "cardano"]
start_date = datetime(2024, 1, 1)
asyncio.run(main(assets, start_date))

# Ingerir apenas dados de mercado com paginação
assets = ["bitcoin"]
asyncio.run(main(assets, ingest_history=False, market_limit=50, market_offset=0))
```

## Pontos de Melhoria e Evolução
- Implementar API e endpoints para executar o sistema em produção com FastAPI
- Implementar Cloud Run para executar o sistema em produção
- Implementar CD com Cloud Build para construir a imagem do Cloud Run
- Implementar Cloud Storage para armazenar dados brutos antes de envio para o banco de dados
- Implementar orquestração com Airflow ou Workflows
- Implementar testes de qualidade de dados
- Ampliar cobertura de testes

## Configuração de Execução
1. Instalar Python 3.12.2
2. Instalar Poetry
3. Executar `make install` para instalar as dependências python e poetry
4. Executar `make infra` e `make infra_apply` para criar o banco de dados no GCP
5. Configurar variáveis de ambiente no arquivo `.env` ( chave `COINCAP_API_KEY` e `DATABASE_URL`)
6. Executar a aplicação usando `make run`
