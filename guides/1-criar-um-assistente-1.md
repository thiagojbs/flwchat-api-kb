# 1. Criar um assistente

Neste primeiro passo vamos criar juntos um agente IA e configurar as primeiras etapas da integração com o assistente no N8N.

Antes de tudo vamos criar nosso assistente IA, configurar o modelo e criar uma chave de API.

## Como criar uma conta na OpenAI

* Acesse o site da OpenAI (<https://platform.openai.com>) no seu navegador.
* Inicie o cadastro: clique no botão "Sign Up" ou "Registrar-se" no canto superior direito da página.
* Preencha suas informações: insira seu endereço de e-mail ou, se preferir, faça login diretamente com uma conta Google ou Microsoft. Em seguida crie uma senha.
* Verificação de e-mail: após fornecer suas informações e criar uma conta, você receberá um e-mail de verificação. Acesse sua caixa de entrada e clique no link de verificação enviado pela OpenAI.
* Preencha seus dados pessoais: pode ser solicitado o fornecimento de informações como seu nome e telefone para verificação.
* Escolha um plano: a OpenAI oferece tanto uma versão gratuita quanto planos pagos com mais recursos. Escolha o que melhor se adequa às suas necessidades.

***

## Como criar um projeto dentro da OpenAI

* Após criar sua conta na OpenAI, será possível acessar o painel onde você poderá criar o seu assistente.
* No painel, clique em "Dashboard".
* Depois, clique em "Assistants".

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1884fc9cfbadab6cbe9b395cce670fc856b0a0cb618daf59c8470345b496481a-WTS.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Clique em "Create".
* Ao clicar em "Create", será aberta a tela acima onde você poderá dar um nome ao seu assistente no campo "Name".
* No campo "System instruction", você deverá definir como o assistente deve se comportar. Exemplo:

> **Você deve se comportar como um corretor de imóveis. Pergunte ao cliente sobre o tipo de imóvel, localização desejada, número de quartos, banheiros, vagas de garagem e faixa de preço. Responda perguntas frequentes de forma rápida e objetiva. Transfira para o atendimento humano se a informação disponível não for suficiente.**

* Defina o modelo no campo "Model" — recomendamos o gpt-4o-mini por ser um modelo completo e mais rápido que outros.
* Em seguida, é possível definir configurações adicionais como "File search" que permite que o assistente tenha conhecimento dos arquivos que você ou seus usuários carregam. Depois que um arquivo é carregado, o assistente decide automaticamente quando recuperar o conteúdo com base nas solicitações do usuário e, também, o "Code Interpreter" que permite que o assistente escreva e execute códigos.
* Configure o "Response Format" para "Text".
* Deixe os campos "Temperature" e "Top P" default, no futuro ajuste para que a resposta seja mais adequada ao tom que você deseja que o assistente responda.

***

## Como criar uma chave de API

* No menu lateral, clique em "API Keys".
* Na página de "API Keys", clique no botão "Create new secret key", como demonstra a imagem abaixo:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/43e2c8e270320cec6ab59a1a01942b68fcdcc679b147031f5542879e44a572a1-WTS_3.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Um pop-up aparecerá mostrando sua nova chave de API. **Copie a chave imediatamente**, pois você não poderá visualizá-la novamente.
* Essa chave será usada para autenticar suas solicitações ao utilizar a API da OpenAI.
* Se precisar, você pode revogar ou criar novas chaves a partir dessa mesma tela a qualquer momento.

<br />

**Lembre-se de que a chave de API é privada e você não deve compartilhá-la publicamente, pois ela dá acesso à sua conta e aos seus créditos da OpenAI.**
