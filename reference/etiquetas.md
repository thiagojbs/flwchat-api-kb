# Etiquetas

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/tag — Listar

**Resposta 200** [`PublicTagDTO`](#publictagdto)[]

Array de [`PublicTagDTO`](#publictagdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-tag

## `POST` /core/v1/tag — Criar

Cria uma etiqueta na conta. A cor define automaticamente a cor do texto; quando omitida, a etiqueta é criada em `GRAY_600`.

**Body** [`PublicReqCreateTagDTO`](#publicreqcreatetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a etiqueta é criada em `GRAY_600`. Use `GET /v1/tag/color` para as cores disponíveis. |

**Resposta 200** [`PublicTagDTO`](#publictagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-tag

## `GET` /core/v1/tag/color — Listar cores

Listagem das cores disponíveis para etiquetas. O valor de `color` é o que deve ser informado na criação e na atualização.

**Resposta 200** [`PublicTagColorDTO`](#publictagcolordto)[]

Array de [`PublicTagColorDTO`](#publictagcolordto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cores disponíveis para etiquetas. O nome combina a família de cor com o tom, do mais claro (100) ao mais escuro (600). |
| `bgColor` | string | - | Cor de fundo da etiqueta, em hexadecimal. |
| `textColor` | string | - | Cor do texto correspondente, em hexadecimal. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-tag-color

## `DELETE` /core/v1/tag/{id} — Excluir

Exclui uma etiqueta. Quando a etiqueta estiver vinculada a contatos, a exclusão é recusada até que seja confirmada com `removeFromContacts`, pois ela será removida de todos os contatos associados.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da etiqueta. |

**Body** [`PublicReqDeleteTagDTO`](#publicreqdeletetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `removeFromContacts` | boolean | - | Confirma a exclusão de uma etiqueta que está vinculada a contatos, removendo-a de todos eles. Sem esta confirmação, a exclusão é recusada quando existir ao menos um contato vinculado. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-tag-id

## `PUT` /core/v1/tag/{id} — Atualizar

Atualiza o nome e a cor de uma etiqueta. Quando a cor é omitida, a cor atual é mantida.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da etiqueta. |

**Body** [`PublicReqUpdateTagDTO`](#publicrequpdatetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a cor atual da etiqueta é mantida. Use `GET /v1/tag/color` para as cores disponíveis. |

**Resposta 200** [`PublicTagDTO`](#publictagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-tag-id

---

## Schemas

### PublicReqCreateTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a etiqueta é criada em `GRAY_600`. Use `GET /v1/tag/color` para as cores disponíveis. |

### PublicReqDeleteTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `removeFromContacts` | boolean | - | Confirma a exclusão de uma etiqueta que está vinculada a contatos, removendo-a de todos eles. Sem esta confirmação, a exclusão é recusada quando existir ao menos um contato vinculado. |

### PublicReqUpdateTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a cor atual da etiqueta é mantida. Use `GET /v1/tag/color` para as cores disponíveis. |

### PublicTagColorDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cores disponíveis para etiquetas. O nome combina a família de cor com o tom, do mais claro (100) ao mais escuro (600). |
| `bgColor` | string | - | Cor de fundo da etiqueta, em hexadecimal. |
| `textColor` | string | - | Cor do texto correspondente, em hexadecimal. |

### PublicTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |
