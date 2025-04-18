# Protocolo de Devolução/Reentrega

Aplicativo Streamlit para registro e consulta de protocolos de devolução e reentrega.

## Funcionalidades

- Registro de protocolos de devolução/reentrega
- Consulta de protocolos por ID
- Visualização de todos os registros
- Exportação para Excel (individual ou todos os registros)
- Administração (exclusão de registros com autenticação)

## Configuração

### Secrets do Streamlit

Este aplicativo utiliza o sistema de secrets do Streamlit para gerenciar credenciais sensíveis.

1. Para desenvolvimento local, crie um arquivo `.streamlit/secrets.toml` com o seguinte conteúdo:

```toml
# Database credentials
[db_credentials]
host = "your_host"
database = "your_database"
user = "your_username"
password = "your_password"
port = "5432"

# Admin credentials
[admin]
delete_password = "your_secure_password"

# Excel template configuration (optional)
[excel]
template_path = "/path/to/modelo_devolucao.xlsx"
```

2. Para implantação no Streamlit Cloud:
   - Acesse as configurações do seu aplicativo no Streamlit Cloud
   - Vá para a seção "Secrets"
   - Adicione as mesmas variáveis que estão no arquivo `secrets.toml`

## Requisitos

- Python 3.7+
- Streamlit
- psycopg2
- openpyxl

## Execução

Para executar o aplicativo localmente:

```bash
streamlit run main.py
```

## Estrutura do Projeto

- `main.py`: Arquivo principal com interface do usuário
- `database.py`: Operações de banco de dados
- `form_handler.py`: Gerenciamento de formulários
- `excel_handler.py`: Exportação para Excel
- `.streamlit/secrets.toml`: Arquivo de configuração de secrets (local)