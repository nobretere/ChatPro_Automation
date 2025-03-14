# ChatPro App

Esta pasta contém o código da aplicação ChatPro, que auxilia no atendimento ao cliente via WhatsApp.

## Estrutura de Arquivos

- `database.py`: Módulo para conexão e consultas ao banco de dados SQLite `messages.db`.
- `interface.py`: Interface gráfica desenvolvida com `tkinter` para interação com o usuário.
- `openai_api.py`: Integração com a API da OpenAI para geração de respostas automáticas.

## Configuração

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências listadas no `requirements.txt`.
3. Configure a variável de ambiente `OPENAI_API_KEY` com sua chave de API da OpenAI.

## Executando a Aplicação

Execute o arquivo `interface.py` para iniciar a aplicação e interagir com as funcionalidades de atendimento ao cliente.