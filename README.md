# Bot de vendas para WhatsApp!

## Sobre o projeto

Bot de atendimento automatizado para WhatsApp com IA (Inteligência Artificial), criado para automatizar e realizar todo o processo de vendas online de forma contínua, realizando de forma completamente autônoma atendimentos simples como responder perguntas frequentes a até o processo de efetivação da venda e compra do item desejado, auxiliando no processo de compra e atendimento ao cliente, possibilitando dar mais destaque para as vendas presenciais, escalabilidade e melhoria do atendimento ao cliente.

## 🧑‍💻 Funcionalidades

### Funcionalidades implementadas

- **Atendente:** Responde perguntas pegando como contexto uma base de dados existente.
- **Informações:** Conexão com uma base dados em csv para contexto das respostas.

### Funcionalidades futuras

- **Vendedor:** Realizar a venda dos produtos através de um link de pagamento.

## ❓ Como usar | Apenas para Windows
O processo descrito terá como ponto de partida:

- Seu sistema operacional é Windows.
- Possui uma IDE com Python 3.13 ou superior.

### Implantação do sistema
1. Instalação e configuração dos programas necessários:  
    Esses serviços são indispensáveis para o funcionamento do bot. O Docker é responsável por possibilitar o uso da Evolution API e o Ngrok para a captação e respostas de novas mensagens.
    - Docker: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    - Ngrok: [Ngrok](https://ngrok.com/)

2. Escolha a pasta onde que quer os arquivos fiquem localizados, abra o terminal e cole o seguinte comando:
    - Esse comando é responsável por clonar todo o meu repositório no seu computador!
    ```bash
    git clone https://github.com/DaviGMCoelho/bot-whatsapp.git
    ```

3. Abra o terminal e digite o seguinte comando:
    - Esse comando irá gerar um link público para a sua porta 5000, isso é necessário para a função de enviar e receber mensagens funcionar corretamente! Guarde esse link que iremos usar novamente depois!
    ```bash
    ngrok http 5000
    ```

4. Criando o contêiner  
    Aqui você vai criar o contêiner responsável por garantir a utilização da Evolution API.
    1. Abra o Docker Desktop para que o contêiner possa ser criado.
    2. Abra o terminal na pasta raiz do projeto -> **bot_whatsapp_flask/**
    3. Digite o seguinte comando:
        - Esse comando irá criar o contêiner responsável por fazer a Evolution API funcionar.
            ```bash
            docker compose up --build -d
            ```

5. Configurando a Evolution API  
    Durante esse processo o conteiner precisa estar funcionando corretamente e com o docker funcionando, aqui você vai configurar coisas como: Instruções de como você quer o que o bot funcione e dizer quando e como ele irá fazer para responder as mensagens.
    1. Com o Docker funcionando, abra o seu navegador e digite: **https://localhost:8080/manager**
    2. Crie uma instância para o seu bot.
        - Aqui você vai escanear o QR Code usando o número que deseja usar.
    3. Com a instância criada, entre nela e faça os seguintes ajustes:
        - **Comportamento:** Marque as opções "Ignorar grupos", "Sempre online" e "Marcar mensagens como lidas"
        - **Webhook:** No campo "URL", cole a URL que o Ngrok gerou e adicione "/webhook" no final, agora no campo "Eventos", procure e selecione o evento "MESSAGES_UPSERT" e adicione ele na lista, por último, habilite o Webhook e salve as alterações.

6. Ajustes finais  
    Se você fez todos os passos anteriores de forma correta, seu bot está funcionando perfeitamente, agora você apenas precisa colocar os seus dados nele.
    Atualmente o bot responde as perguntas com base em um arquivo previamente colocado, é um arquivo CSV e fica dentro de "data", você precisa substituir o arquivo de teste com suas informações, você pode facilmente converter uma planilha excel ou uma planilha do google sheets em um CSV e alimentar o bot com suas informações.
    

## 💻 Tecnologias

- **🐍 Python:** Desenvolvimento back-end e lógica do bot.
- **🌶 Flask:** Criação do Webhook e rota HTTP.
- **🐋 Docker:** Conteinerização da aplicação e da Evolution API.
- **🌐 Ngrok:** Criação do link público para o Webhook.
- **🧑‍🚀 Postman:** Testes de endpoints da Evolution API e Webhook.
- **📞 Evolution API:** Envio e recebimento de mensagens do WhatsApp.
- **🤖 IA Generativa:** Google Gemini 2.5 flash.
- **🚩 IA Embedding:** Text embedding 004 da Google.


## 🌐 Conceitos abordados

- **Webhooks:** Captura e processamento de requisições de mensagens.
- **Inteligência Artificial:** Generativas e vetoriais.
- **Requisições HTTP:** Requisições e tipos de requisições GET e POST.