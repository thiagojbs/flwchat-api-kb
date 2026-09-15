# 5. Como processar imagens

Nessa etapa vamos ensinar como adicionar a capacidade de processar imagens à sua IA.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/369776debe631f1056604367ea9f710eab5f720f7ebd09ee18394d33c8e89ec7-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_transcribe_image.json).
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

## Processando imagens

* Na etapa anterior no processamento de áudio foi criado o node "Switch" para processar diferentes tipos de arquivo, vamos criar uma rota dentro desse switch para processar as **imagens.**

* Para isso, é necessário comparar se o "file.mimeType" (tipo de arquivo) começa com image/ + (formato) do arquivo, assim como foi feito para o áudio. Confira a imagem abaixo:

[block:image]{"images":[{"image":["https://files.readme.io/6291b8bb5c1840b9ee157b48677d63afdf81b190962700520d60f28f33defc68-image.png",null,""],"align":"center","border":true}]}[/block]

* Grave o "Content" (resultado da transcrição da imagem) em uma variável

  ![](https://files.readme.io/580a4203a135f4df22c16ef8e685b2a13ca6f231a89652a3dbdd68a05cd74861-image.png)
* Após esses passos basta ligar o node "Set" (que contém a variável da transcrição da imagem) ao "Merge". Como mostra a imagem inicial desse documento
* Salve seu workflow.

<br />

Seguindo esse rápido tutorial será possível processar imagens com IA.
