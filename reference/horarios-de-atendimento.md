# Horários de Atendimento

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/company/officehours — Obter

**Resposta 200** [`PublicCompanyOfficeHoursDTO`](#publiccompanyofficehoursdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `limitHours` | boolean | - | Indica se há limite de horário de atendimento |
| `offlineResponse` | string | - | Mensagem exibida quando a empresa está fora do horário de atendimento |
| `timezoneDiff` | number(double) | - | Diferença de fuso horário em relação ao UTC (em horas) |
| `days` | [`PublicCompanyOfficeHoursDayDTO`](#publiccompanyofficehoursdaydto)[] | - | Configurações de horário por dia da semana |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-company-officehours

---

## Schemas

### PublicCompanyOfficeHoursDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `limitHours` | boolean | - | Indica se há limite de horário de atendimento |
| `offlineResponse` | string | - | Mensagem exibida quando a empresa está fora do horário de atendimento |
| `timezoneDiff` | number(double) | - | Diferença de fuso horário em relação ao UTC (em horas) |
| `days` | [`PublicCompanyOfficeHoursDayDTO`](#publiccompanyofficehoursdaydto)[] | - | Configurações de horário por dia da semana |

### PublicCompanyOfficeHoursDayDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do registro |
| `dayWeek` | string | - | Dia da semana em inglês (MAIÚSCULO) |
| `active` | boolean | - | Indica se o atendimento está ativo neste dia |
| `periods` | [`PublicCompanyOfficeHoursPeriodDTO`](#publiccompanyofficehoursperioddto)[] | - | Lista de períodos de atendimento (entrada e saída) |

### PublicCompanyOfficeHoursPeriodDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `startTime` | string | - | Horário de início do período (formato HH:mm) |
| `endTime` | string | - | Horário de término do período (formato HH:mm) |
