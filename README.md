# GTray

É uma aplicação que permite o uso da IA em qualquer programa, melhorando o texto selecionado no momento em que a tecla de atalho é pressionada.

## Pré-requisitos

- Python 3.x
- Sistema operacional Windows
- Chave da API do OpenAI

## Instalação

1. Clone o repositório ou baixe o código-fonte

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

## Configuração

1. Inicie a aplicação executando:
```bash
python GTray.py
```

2. Configure sua chave da API do OpenAI:
   - Clique no botão "Configurar API Key"
   - Digite sua chave da API do OpenAI
   - Clique em "Salvar" para salvar a chave

3. Configure os atalhos de teclado:
   - Clique no botão "Configurar Atalho"
   - Pressione a combinação de teclas desejada
   - O atalho será salvo automaticamente

## Uso

1. Inicie a aplicação:
   - Clique no botão "Iniciar" para ativar o serviço
   - A aplicação será minimizada para a bandeja do sistema

2. Usando os atalhos:
   - Modo genérico: Use o atalho configurado para assistência geral da IA
   - Modo Python: Use o atalho específico do Python para geração de código
   - Modo gráfico: Use o atalho gráfico para visualização de dados
   - Modo criação: Use o atalho de criação para novos projetos de código

3. Controle de visibilidade:
   - Use a checkbox "Visível" para controlar a visibilidade da interface
   - A aplicação continua rodando em segundo plano quando oculta

## Recursos

- Integração com a bandeja do sistema
- Múltiplos modos de assistência da IA
- Atalhos de teclado personalizáveis
- Geração e melhoria de código
- Geração de gráficos a partir de dados
- Assistente para criação de projetos

## Dependências

- pynput==1.8.0
- pyperclip==1.9.0
- pywin32==308
- pystray==0.19.4
- keyboard==0.13.5
- openai==1.65.4
- configparser==7.1.0
- PyQt5==5.15.11

## Nota

Certifique-se de manter sua chave da API em segurança e nunca compartilhá-la publicamente. A aplicação armazena a chave da API localmente em um formato criptografado.