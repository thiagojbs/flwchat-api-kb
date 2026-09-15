# N8N

O **n8n** é uma plataforma **LowCode** que permite criar automações de maneira intuitiva, sem a necessidade de conhecimento profundo em programação. Com o n8n, é possível integrar nossa plataforma com diversos serviços externos, aumentando significativamente as possibilidades ao utilizar nossa API.

# Modalidades de uso

### n8n.cloud

Você pode optar por contratar o n8n como **serviço na nuvem**, pagando por execução dos fluxos. Existem diferentes pacotes com limites de execuções mensais, atendendo às necessidades da maioria dos usuários. Este modelo é ideal para aqueles que buscam simplicidade e não querem se preocupar com manutenção de infraestrutura.\
Veja mais [aqui](https://n8n.io).

### Auto-hospedado (Self-hosted)

Para cenários em que há grande volume de integrações e automações, o custo do n8n na nuvem pode ser um fator limitante. Nesse caso, é possível instalar o n8n em um servidor próprio, permitindo execuções ilimitadas e reduzindo os custos relacionados.

Com a opção de **auto-hospedagem**, você paga apenas pelo servidor, o que é vantajoso para quem deseja flexibilidade e escalabilidade sem restrição de execuções.\
Veja mais [aqui](https://docs.n8n.io/hosting/).

***

# Módulo nativo para uso Self-hosted

Desenvolvemos um módulo nativo para facilitar a integração;

> 📘 Atenção - Community Nodes
>
> Para construção do módulo utilizamos a funcionalidade **Community Nodes** do N8N, esta funcionalidade está disponível apenas para contas **auto-hospedadas (self-hosted)**.
>
> Os usuários com n8n.cloud ainda não têm acesso a essa funcionalidade.

### Passos para instalação

**1 - Acesse as configurações na página inicial do n8n. Para isso, clique no menu de configurações no canto inferior esquerdo, em seguida clique em “Settings”/ “Configurações”.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/71de7612ae22b4af7730ebc6dec92b7ffa7d5bd0db6ba32f4b97dfe72df00491-chrome-capture-2024-11-19_2.gif",
        "",
        "Configurações da plataforma"
      ],
      "align": "center",
      "caption": "Configurações da plataforma"
    }
  ]
}
[/block]

**2 - Em seguida, no menu de opções clique em “Community nodes”/ “Nós da comunidade”.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0ecb7ffaaa79d7602cd7272e58fa61da6ff43b6600e4a3b961f9cbf64cf0a34a-community.png",
        "",
        "Opção \"Community nodes\""
      ],
      "align": "center",
      "caption": "Opção \"Community nodes\""
    }
  ]
}
[/block]

**3 - Clique em “Install comunnity nodes”.**

Adicione o nome do pacote npm e aceite os termos de instalação e clique em install.\
**Nome do pacote**: n8n-nodes-wts.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a0f9d80c267de39a3188e62fc2a5c59bcd504b8cd2bfe691d001824a655b4f00-Nome_NPM.png",
        "",
        "Defina o nome do pacote: **n8n-nodes-wts**"
      ],
      "align": "center",
      "caption": "Defina o nome do pacote: **n8n-nodes-wts**"
    }
  ]
}
[/block]

### 🎉 Pronto, agora é só usar...

***

### Uso do módulo

* Clique no painel de nós, no canto superior direito e busque por “wts chat” para listar as ações disponíveis.

[block:image]{"images":[{"image":["https://files.readme.io/deb34f3d8488b542c6936a683d2025997f8268ed5d76c8b67f7c962711e5523a-zoom.gif","",""],"align":"center"}]}[/block]

Para utilizar o módulo, é necessário ter um token permanente, saiba mais [aqui](https://flwchat.readme.io/reference/criar-token-para-integra%C3%A7%C3%A3o) .

Após adicionar um dos nós, clique em **Credential to connect with** e **Create new credential**. Escolha um nome que identifique a sua conta na plataforma. Para finalizar, clique em **salvar**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/bdeaf66ba592ecbe7ad27a56df035e7f89ba9ce940921788a4e361e8416fc52b-chrome-capture-2024-11-19_5.gif",
        "",
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

Preencha as outras opções do nó e execute.

### 🎉 Pronto você deu o primeiro passo para realizar as integrações.
