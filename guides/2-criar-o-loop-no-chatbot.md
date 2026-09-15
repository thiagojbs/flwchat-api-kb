# 2. Criar o loop no chatbot

Entenda como criar o modelo de chatbot e configurar o loop de modo que as mensagens enviadas não se percam e sejam sempre processadas por seu assistente.

## Como criar o modelo do chatbot

* Dentro da plataforma faça login com o usuário administrador e siga os passos abaixo para criar o modelo do chatbot que será integrado à IA.

* No menu de opções clique em **Apps** > **Chatbot** > **Novo**.

* Dê um nome ao seu chatbot e o associe a um tipo de canal (Z-API ou WhatsApp oficial). Defina a equipe padrão desse chatbot.

* Crie um nó de mensagem receptiva. Exemplo: *Olá, boas-vindas! Como posso ajudar?*

* Em seguida, configure uma ação que aguarde resposta do contato com as opções: **"Limite de espera: Sem limite"** e **"Tolerância: 5 segundos"**.

* Acima do nó de "Aguardar resposta do contato" é necessário criar um ponto de retorno. Atenção: sem este ponto de retorno o loop não irá funcionar.

* Em seguida, é preciso configurar o disparo webhook que enviará as informações do atendimento.

* No campo **URL** copie a URL do webhook que deverá ser criado no N8N e cole no campo "URL". Clique em **"Atualizar"** para salvar as configurações.

[block:image]{"images":[{"image":["https://files.readme.io/2a68c3db185774771513e3170f7bd6d9f9b88f50a23c066ababadae59bf9f9be-image.png",null,null],"align":"center","border":true}]}[/block]

<br />

***

## Como criar os loops

* Dentro do subfluxo de **"Sucesso"** crie uma ação que redireciona para o ponto de retorno **"GPT"**, como mostra a imagem acima.
* Assim, o loop estará configurado de modo que sempre que o contato enviar uma mensagem a mesma voltará ao ponto de retorno configurado e será disparada via webhook criando o loop.

  ![](https://files.readme.io/1cea14fb4be34843910e0885f9dfb82d2376afb50718f3e6d2f53f1fca4baec3-image.png)

<br />

* No subfluxo de **"Falha no envio"** adicione uma mensagem de modo que o contato seja informado que a mensagem dele falhou ou não foi compreendida, logo após adicione outro ponto de retorno **"GPT"**, assim como no fluxo de "Sucesso no envio"

  ![](https://files.readme.io/cda5cd9b183db87645645cf2aaf482e281d973361e593fe392f47b757f0c4dba-image.png)

<br />

Após seguir os passos acima, salve seu chatbot, publique e o associe ao canal em que os clientes entrarão em contato e serão respondidos por seu assistente.
