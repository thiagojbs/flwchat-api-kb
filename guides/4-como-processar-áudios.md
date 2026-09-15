# 4. Como processar áudios

Nessa etapa vamos ensinar como adicionar a capacidade de processar áudios à sua IA.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

![](https://files.readme.io/7cc1583c454c1a0441643149950d2cdafb2d08bef63adb07def0e4575c8bd7a6-image.png)

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_transcribe_audio.json).
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

## Separando os tipos de mensagem

Como explicado anteriormente, mensagens agregadas são divididas em mensagens de texto e mensagens que contenham áudio, imagem ou arquivo. Para separarmos as mensagens de texto das mensagens que contenham arquivos, vamos usar o node "Filter" validando se o tipo de mensagem "Text" é ou não vazio.

* Se não for vazio vamos usar um "Set" para gravar a várivel "lastMessagesAggregated.text" e, caso seja vazio, serão  enviadas apenas mensagens do tipo "File",  vamos tratar sobre mais a frente.

<br />

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/71fc809bc4c502da99eb9943f229c9850a781eb0b9c7ea44e93591ea0ab93402-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Já para mensagens "Files" devemos dividir os arquivos vindos do webhook em arquivos únicos, usando o node "Split Out" e tratar cada tipo de arquivo de uma maneira. Nessa etapa vamos tratar apenas arquivos de áudio, outros tipos de arquivos serão abordados mais a frente.

[block:image]{"images":[{"image":["https://files.readme.io/e7c75bd3c0081ce3d348d9c5298682a3b463db1d52f5da648eb28fb9e8841acc-image.png",null,""],"align":"center","border":true}]}[/block]

* Após dividirmos os arquivos vamos separá-los por tipo, áudio, imagem e documentos. Para isso usaremos o node "Switch" e comparar se o "file.mimeType" (tipo de arquivo) começa com áudio/(formato) do arquivo.

[block:image]{"images":[{"image":["https://files.readme.io/7af17401bbc21aa3d7560ece8c31595cc9099638341708ad4427a6c4aae10cf8-image.png",null,""],"align":"center","border":true}]}[/block]

***

## Tratando arquivo de áudio

* Após separar o arquivo de áudio dos demais, é preciso fazer o seu download. Para isso usaremos uma requisição HTTP, vamos dar um "GET" na URL pública que se encontra o áudio.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c479446f08f8c7de2912467eeb97adc6c1449024ae15df08aa5bb7c56f312686-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

***

## Transcrevendo o áudio

* Logo após realizar o download do áudio, crie um node OpenIA > "Transcribe Recording".

* No campo "Input Data Field Name" é necessário passar o nome do campo de entrada que contém os dados do arquivo binário a serem processados.

[block:image]{"images":[{"image":["https://files.readme.io/204196db3bcddd8f53201fd10a3890f6707cd323a80b3f59108dfb06ba9072d2-image.png",null,""],"align":"center","border":true}]}[/block]

* Grave o output da transcrição em uma variável.
* Crie um node "Merge" para agrupar os inputs.
* Grave os valores "text" e "sessionId" em um node "Set".

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/564f668d83d296a519040ff68fc620715a5ede2a0f10014fe43997892da0fcc4-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Em seguida, é necessário concatenar as mensagens em uma única mensagem para enviarmos para o seu assistente.  Para isso será utilizado um node "Code", basta copiar o código abaixo:

```javascript
var text = "";
var sessionId = $('Webhook').first().json.body.sessionId;

for (const item of $input.all()) {
  text += item.json.text + " \n";
}

return { "text": text, "sessionId": sessionId };
```

***

### Resumo do que o código faz:

1. Inicializa uma variável text como uma string vazia.
2. Recupera o valor do sessionId de uma resposta de webhook anterior.
3. Itera por todos os itens de entrada disponíveis e concatena o texto de cada item, adicionando uma nova linha entre os textos.
4. Retorna um objeto com o texto concatenado e o sessionId para ser usado em outro lugar.

* Ligue o node "Code" ao seu assistente, que por sua vez estará ligado ao node "Enviar mensagem".

Após todos esses passos sua integração irá processar áudios enviados, transcrevendo-os em texto para que seu assistente consiga interpretar e responder da forma mais adequada.
