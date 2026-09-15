# Arquivos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v2/file — Obter url para upload

Envie os metadados do arquivo e você receberá uma URL e deverá fazer upload para ela usando o método PUT Após enviar o conteúdo do arquivo, faça uma chamada para o endpont POST /core/v2/file

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Type` | query | sim | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | Tipo do arquivo Se informado o tipo UNDEFINED o sistema tentará identificar o tipo do arquivo Arquivos do tipo DOCUMENT não passam por transformação ou compressão, mas arquivos do tipo IMAGE e VIDEO são transformados para que sejam compatíveis com todas as plataformas. |
| `Name` | query | sim | string | Nome do arquivo, com extensão (ex.: paisagem.jpg) |
| `MimeType` | query | - | string | Mimetype do arquivo. Se não informado ele será definido pelo tipo ou extensão do arquivo |

**Resposta 200** [`PublicUrlUploadFileV2DTO`](#publicurluploadfilev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | - | Código do arquivo temporário, só será válido após confirmar o salvamento; |
| `urlUpload` | string | - | Url para upload do arquivo (utilize o metodo PUT para upload) |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-file

## `POST` /core/v2/file — Salvar arquivo

Após o upload do arquivo na URL fornecida na rota GET /core/v2/file execute este metodo para obter o ID do arquivo O Id do arquivo pode ser fornecido no envio de mensagens. O FileId pode ser reaproveitado, não sendo necessário novos uploads para o mesmo arquivo.

**Body** [`PublicReqFileSaveV2DTO`](#publicreqfilesavev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | sim | Código do arquivo |

**Resposta 200** [`PublicFileV2DTO`](#publicfilev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | - |  |
| `key` | string | - |  |
| `size` | integer(int64) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-file

---

## Schemas

### PublicFileV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | - |  |
| `key` | string | - |  |
| `size` | integer(int64) | - |  |

### PublicReqFileSaveV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | sim | Código do arquivo |

### PublicUrlUploadFileV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | - | Código do arquivo temporário, só será válido após confirmar o salvamento; |
| `urlUpload` | string | - | Url para upload do arquivo (utilize o metodo PUT para upload) |
