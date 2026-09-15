# 3. Como ler e responder textos

Vamos adicionar a capacidade de ler e responder textos usando o ChatGPT.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

![](https://files.readme.io/cfefb1c37cf1a3dfbb0565c56dc4962574eda264966f4ad202eac5961ce13215-image.png)

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_response_with_text.json) .
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

***

# Como fazer

## Montando o escopo da integração

* Crie uma conta no [N8N](https://n8n.io/).
* Clique em "Add workflow".
* Em seguida, clique em "Add first step".
* Selecione o node "On webhook call".
* Altere o método "HTTP" para **"Post"**.

***

## Armazenando variáveis

* Crie um node "Edit Fields".
* Crie uma variável chamada text e armazene nessa variável o valor "lastMessagesAggregated". Veja imagem abaixo

  ![](https://files.readme.io/facbcd30f03b11a64240d77c4287b5960eef156874099cfd664fd92db60b382c-image.png)

***

## Configurando o node do assistente

* Logo após criar o webhook, é preciso criar o node do assistente IA.
* Para isso, clique em "+" digite **"OpenIA"** e selecione **"Message an assistant"**.
* Adicione a credencial que foi criada dentro da plataforma da OpenIA, essa credencial será a chave da API que você criou no passo 3 da etapa [Criar um assistente](https://flwchat.readme.io/reference/1-criar-um-assistente-1).
* Nas opções "Resource" e "Operation" deixe ambos default.
* Em "Assistant" selecione o assistente que você criou na etapa [Criar um assistente](https://flwchat.readme.io/reference/1-criar-um-assistente-1).
* Em "Prompt" selecione a opção "Define below", no campo "text" passe a variável "text" que gravamos no node anterior "Edit Fields".

  ![](https://files.readme.io/ae767047c740f4d42a51d78e0c20c5976fda75c90c94fbaf99089f7d85fd935a-image.png)

<br />

* Em "Memory" defina para "Use memory connector". Será criado um nó abaixo do nome "Window Buffer Memory", nele é preciso passar o ID da sessão (presente no webhook).

> ### Atenção
>
> Definir a memória é muito importante, ela que fará com que o assistente consiga entender o contexto da conversa.
>
> ![](https://files.readme.io/5df3223a5bdecaf177473b259690b565fe6dc883ef21de2574e6a168eab20746-image.png)
>
> <br />

***

## Ferramentas do assistente IA

O assistente assistente possui ferramentas (Tools), que permite interações com outros sistemas através de requisições HTTP, isso torna-se útil e abre um leque de opções, você pode fazer requisições para buscar um boleto em um banco de dados e retorna-lo para o contato por exemplo, nesse documento vamos abordar três funcionalidades, mas o céu é o limite tratando-se dessa funcionalidade.

1. Nessa primeira etapa vamos realizar uma requisição na API para buscar as equipes de uma conta, essa lista de equipes dará uma base ao seu agente para transferir o contato de acordo com o contexto da conversa.

* Clique em tools e crie uma requisição HTTP
* Em "Description" você deve dar instruções para o agente da função, segue uma sugestão: "Nesta função você consegue listar as equipes disponíveis para transferência".
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/get_v2-department).
* Ao configurar o header defina o "Value Provided" como "Using Field Below". Veja imagem abaixo

  ![](https://files.readme.io/358fe8a6d87ef75b4e5762813d0508afdc2507743637092ef2839bfef9ba105c-image.png)

2. Nessa etapa vamos configurar a função de transferência de equipe, também vamos criar uma requisição HTTP, para o endpoint de transferir conversas.

* Assim como na etapa anterior vamos dar algumas instruções para nosso assistente IA sobre como usar essa função, segue uma sugestão:\
  **Setores para transferência.**\
  **Algumas diretrizes:**\
  **-Seja rápido e objetivo ao responder perguntas frequentes, buscando entender detalhadamente o problema do contato.**\
  **-Explique de maneira simples qualquer processo técnico de baixa complexidade.**\
  **-Demonstre paciência ao lidar com questões delicadas ou frustrações dos clientes.**\
  **-Utilize um tom positivo e otimista, mesmo ao comunicar informações difíceis ou negativas**.\
  **-Não solicite dados do contato como (e-mail, Id, números de protocolo, documentos).**
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/put_v1-session-id-transfer).
* Marque a opção "Send Body" e cole o JSON abaixo no body da requisição.

```json
{
  "type": "DEPARTMENT",
  "newDepartmentId": "{departmentId}"
}
```

* Você deve usar um placeholder para quaisquer dados a serem preenchidos pelo modelo. Veja imagem abaixo

  ![](https://files.readme.io/9c47ae4c1fa9260cab44ea338517f64f7233a6916b49c2e8742882392c1c6fc9-image.png)

3. Por fim, a função de concluir atendimento, nessa etapa vamos configurar uma outra requisição para finalizar o atendimento quando solicitado pelo contato. Siga os passos abaixo

* No campo "Description" passe as instruções para seu assistente IA.
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/put_v1-session-id-complete).
* Marque a opção "Send Body" e cole o JSON abaixo no body da requisição
* ```json
  {
    "reactivateOnNewMessage": true
  }
  ```

  ![](https://files.readme.io/e395c0cd565d4c4ffa909f2c9c435968e37b079209006e47990240b1b7554735-image.png)

  ***

  ## Configuração do node de enviar mensagem ao contato
* O primeiro passo é instalar o módulo do WTS em seu N8N. É possível encontrar essa informação para a instalação em "Ajustes" > "Integrações" > "Automações via N8N".
* Após instalar o módulo WTS, crie uma chave de API dentro da plataforma em "Ajustes" > "Integrações" > "Integrações Via API" > "Novo" > "Nomeie a chave" > "Salve" > "Copie".
* Clique para adicionar um novo nó e digite "WTS", procure por "Session Actions" > "Send Message Text".
* Em "Credential to connection with", caso você já tenha uma chave de API criada, bastar selecioná-la. Caso não, basta criar uma nova "Create new credential" e colar a chave API criada na plataforma.
* O output em questão é a resposta do seu agente, você deve passá-lo dentro da requisição para disparar essa resposta para o contato.
* No campo "Text" coloque o output retornado por seu agente IA, no campo "Session ID" informe o id da sessão (essa informação você encontra no output do webhook, procure por "sessionId").

  ![](https://files.readme.io/32bd80ce5b147a49d540fee71eb35c23da1f13b56c6bec8a36ad78882e24f370-image.png)

Seguindo esse tutorial, será possível ler e responder textos usando o ChatGPT, além disso será possível executar funções de transferência e conclusão de atendimentos. Você também pode adicionar outras funções ao seu assistente, como buscar boletos em uma API externa por exemplo, existem diversas possibilidades que você pode explorar utilizando as ferramentas do seu assistente.
