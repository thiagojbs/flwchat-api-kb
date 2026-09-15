# MAKE

O **Make.com** é uma plataforma de automação que permite criar fluxos de trabalho personalizados para integrar diferentes aplicativos e serviços, eliminando tarefas manuais e repetitivas. Com uma interface visual intuitiva, os usuários podem conectar ferramentas e configurar gatilhos e ações para automatizar processos.

### Como funciona a contagem:

* **Operação**: Cada vez que um módulo em um cenário é executado, ele conta como uma operação. Por exemplo:
  * Buscar dados em uma planilha: 1 operação.
  * Enviar uma mensagem via e-mail ou Slack: 1 operação.
  * Processar dados de várias linhas: cada linha pode contar como uma operação separada.
* **Cobrança**:
  * **Plano contratado**: Cada plano (Gratuito, Core, Pro, etc.) tem um limite de operações mensais.
    * **Exemplo**: Um plano Core pode oferecer 10.000 operações por mês.
  * **Excedente**: Se o limite for atingido, os cenários param de executar até que:
    * O limite seja renovado no próximo ciclo.
    * Você faça um upgrade para um plano superior.

### Autenticação - Make.com

Um token permanente permite que você autentique e autorize seu aplicativo sem ter que implementar fluxos de autenticação OAuth 2.0. Basta criar um novo token e usá-lo para autenticação onde quiser.

Tutorial de instalação do aplicativo wtschat no Make.com

Passos para instalação

1. ### Acesse o Link do Aplicativo Make

   Abra o navegador e acesse o [link ](https://www.make.com/en/hq/app-invitation/0e94c36cbd3949661d56ad6aa33a80df)específico do aplicativo Make. Clique no botão “Instalar” para iniciar o processo.

   ![](https://files.readme.io/dab813e8d75ffeaec47b23d825d9d2b37b833d63a144a6f471ee33e5f04f7e83-image.png)
2. ### Complete a Instalação do Aplicativo

Você será redirecionado para uma página onde deverá selecionar a organização na qual deseja instalar o aplicativo. Selecione a organização desejada e clique no botão “Instalar” localizado no canto inferior direito da tela.\
Observação: A instalação só pode ser feita em uma organização na qual você possui a função de “administrador” ou “desenvolvedor de aplicativos”.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ef661dee5d39df4742fde9a3c0c359d2a85f53ee3456126d3a8619ce3190f063-INSTALAO_1.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]

3. ### Confirmação de Instalação
   Uma notificação aparecerá na tela indicando que a instalação foi concluída com sucesso. Clique em "Finish Wizard"

<br />

4. ### Acesse o Make
   Abra o Make e acesse a organização onde você instalou o aplicativo. Navegue até “Aplicativos Instalados” para visualizar o ícone e o nome do aplicativo "wts.chat".

![](https://files.readme.io/76c4ae2777e38063a22bb3cf1ada4ee603fbc98602785c16ba4a7c7ca59a36f2-image.png)

*Visualize o ícone do aplicativo wts.chat em Aplicativos Instalados*

<br />

5. ### Crie um Novo Cenário
   Vá para a seção “Cenários”. Clique no botão “Crie um novo cenário” no canto superior direito da tela.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f6ead864644441c5328cf2630f30d8962742d533f63ea778af58321aa8a69bae-create_scenario.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]

6. ### Adicione o módulo wtsChat ao Cenário
   Após criar o cenário, um pop-up será exibido permitindo que você pesquise os aplicativos. Digite "wts chat" na barra de pesquisa. Você poderá ver todos os módulos do wts chat, organizados em grupos como “Contatos”, “Mensagens”, “Painéis”, etc.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c653eb4d846c64beefb01adf8166fa3a66824241f2e741d367cab70cce6c5cd1-INSTALAO_2.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]
