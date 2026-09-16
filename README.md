# 🛡️ Andon System: API Gateway (Módulo Principal)

Este repositório contém a **API Principal** do ecossistema Andon, operando sob o padrão de arquitetura de microsserviços. O sistema atua como um orquestrador e camada de governança inteligente, interceptando requisições de clientes para uma API Secundária e consumindo serviços externos de Inteligência Artificial para mitigação de incidentes.

## 📊 Indicador de Aderência Arquitetural & 🏃‍♂️ Diretrizes de Gestão Ágil de Produtos e Projetos

Este projeto adota um medidor próprio de aderência aos princípios modernos de engenharia de software, cultura DevOps e sistemas distribuídos.

**Alta Aderência: Princípios Arquiteturais e Microsserviços**
* **Coesão e Baixo Acoplamento:** O Gateway opera como a única interface de contato na borda (*Single Point of Entry*), isolando o Backend que concentra as regras de persistência e orquestração de IA.
* **Cliente-Servidor e Independência de Interface:** O front-end atua apenas como *Client-Side ETL*, processando telemetria sem acoplamento topológico com o servidor.
* **Padrão REST e RFC 9110:** Implementação estrita de semântica HTTP. O Gateway atua como um escudo semântico, garantindo que erros estruturais (400, 401) cheguem intactos ao cliente sem mascaramento de exceções (*Error Masking*).

**Alta Aderência: Qualidade, Segurança e DevSecOps**
* **Integração de Testes (CI/CD):** O PyTest bloqueia a implantação caso a acurácia do modelo preditivo (SVM) caia abaixo do threshold de 80%.
* **Segurança no Pipeline:** A telemetria é anonimizada (rótulos SENS-01) para conformidade com a LGPD/GDPR. As transações são blindadas via JWT e o vazamento de chaves é prevenido no repositório via estratégia restrita de arquivos `.env.example`.

**Média Aderência: Modelagem de Domínio e Operações**
* **Gestão de Incidentes (Fix Forward):** O próprio produto materializa a cultura de operações contínuas ao prever falhas de hardware e gerar mitigações autônomas via LLM em tempo real.
* **Infraestrutura:** O encapsulamento é garantido via Docker, porém a orquestração avançada para auto-recuperação e escalabilidade horizontal (Kubernetes) segue mapeada como evolução futura no Roadmap MLOps.

**Trade-offs (Padrões Não Aplicados)**
* **GraphQL e RPC:** Omitidos intencionalmente. O protocolo REST síncrono atendeu integralmente aos requisitos de latência e integração entre os componentes deste MVP, evitando excesso de engenharia (*overengineering*).

O desenvolvimento deste microsserviço não foi guiado apenas por decisões técnicas, mas por uma forte cultura de **Gestão Ágil de Produto**, garantindo o alinhamento com as necessidades de negócio:

* **Product Discovery e Foco no MVP:** A concepção do projeto utilizou dinâmicas de *Lean Inception* para delimitar claramente o Produto Mínimo Viável (MVP). O foco foi isolar as funcionalidades de maior valor (mitigação autônoma de incidentes via IA) com o menor custo computacional possível para validação (uso de SQLite para prova de conceito).
* **Governança de Sprints e Backlog:** O escopo foi priorizado e fatiado em entregas incrementais. O backlog técnico (dívidas técnicas e infraestrutura) foi balanceado com o backlog de produto (regras de negócio da telemetria) iterativamente.
* **Definition of Done (DoD) Estrito:** Um incremento só foi considerado "Pronto" ao atender critérios de aceite rigorosos: versionamento padronizado de rotas (`/v1/`), isolamento via Docker comprovado, segurança de tráfego por JWT operante e documentação atualizada e interativa disponível.
* **Cultura DevOps (Shift-Left):** A integração das disciplinas de infraestrutura e gestão de projetos ocorreu desde o "dia zero". Problemas de configuração e *deploy* foram antecipados para o início do ciclo, reduzindo o tempo de *Go-To-Market* da prova de conceito.

## 🎯 RTM: Matriz de Rastreabilidade de Requisitos (MVP)
Este projeto atende integralmente ao **Cenário 2.1** das diretrizes de Arquitetura de Software.

| Requisito do MVP | Implementação e Compliance no Projeto | Status |
| :--- | :--- | :--- |
| **API Principal (5.0 pts)** | Desenvolvida em Python (Flask) rodando na porta 8080. Implementa os 4 métodos exigidos (`GET`, `POST`, `PUT`, `DELETE`) mapeados no controller de roteamento. | ✅ Atingido |
| **API Externa (1.0 pt)** | Integração via `POST` com a API não paga do **OpenRouter** para LLM. Os dados são processados nativamente, sem redirecionar o usuário. | ✅ Atingido |
| **Containerização (1.0 pt)**| `Dockerfile` isolado e disponibilizado na raiz deste repositório com orquestração manual em rede. | ✅ Atingido |
| **Documentação (1.0 pt)** | Instruções de instalação, fluxograma de arquitetura e declaração de uso da API externa presentes neste README. | ✅ Atingido |
| **Organização (1.0 pt)** | Código organizado no padrão MVC (Controllers/Services). Repositório público e independente do Backend. | ✅ Atingido |

## 🏗️ Arquitetura e Padrões de Projeto

O sistema rompe com a arquitetura monolítica legado para adotar a componentização de serviços:
* **Gateway de Borda & Segurança:** O Gateway centraliza a entrada (porta 8080) e intercepta os cabeçalhos de autorização, atuando como controlador de acesso.
* **Tratamento RFC 9110:** Implementa blindagem semântica. Erros estruturais ou falhas de autenticação são barrados na borda (ex: `401 Unauthorized`, `400 Bad Request`), impedindo o mascaramento de exceções (Erro 500) comuns em arquiteturas distribuídas.
* **Desacoplamento Cognitivo:** A responsabilidade de gerar os planos de ação (playbooks) foi transferida para um modelo LLM externo, aliviando o processamento interno.
* **Roteamento de Alta Fidelidade e Versionamento Estrito:** Para evitar ambiguidades de roteamento (*mismatch* de rotas 404), o Gateway atua com orquestração fiel. Em vez de suprimir (*strip*) o prefixo da URL internamente, a camada de roteamento foi refatorada para preservar e orquestrar a rota exata diretamente ao Backend, garantindo padronização universal do `/v1/`.

![Arquitetura Andon IT](./Andon%20IT%20-%20Autonomous%20Action.png)

## ⚙️ Dívidas Técnicas (Tech Debts) e Governança
* **Roteamento (Low Risk):** A constante de host `BACKEND_URL` presente na configuração principal funciona como *fallback*, sendo redundante em relação à inicialização dinâmica via variável de ambiente. A centralização dessa chamada está mapeada para a próxima iteração.
* **Governança Git:** Para manter o histórico linear e evitar commits de mesclagem não intencionais em um ambiente distribuído, o padrão estabelecido para sincronização de repositório neste projeto é o uso estrito do `git pull --rebase`.

## 🌐 Consumo da API Externa

A mitigação automática de incidentes depende do consumo de uma API pública.
* **Serviço Consumido:** OpenRouter (LLMService).
* **Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`
* **Licença de Uso:** Serviço gratuito (modelos *free tier*).

## 💻 Instruções de Instalação e Execução

⚠️ **Pré-requisito Crítico:** Certifique-se de que o **Docker Desktop** (ou daemon do Docker) esteja em execução na sua máquina antes de iniciar os comandos abaixo.

### 1. Clonar e Configurar

    git clone https://github.com/estevamjr/gateway-andon-it.git
    cd gateway-andon-it

Renomeie o arquivo de molde `app/.env.example` para `app/.env`. 
**Atenção:** A chave real da API do OpenRouter, a SECRET_KEY e a **Collection do Postman** para testes serão fornecidas diretamente na mensagem de publicação do portal da disciplina. Insira as chaves no seu arquivo `.env`:

    SECONDARY_API_URL=http://backend-andon:5000
    OPENROUTER_API_KEY=sua_chave_real_aqui

### 2. Subindo a Arquitetura (Docker Manual)
A arquitetura depende de uma rede virtual Docker para a comunicação entre o Gateway e o Backend. Abra o terminal e execute os passos abaixo na ordem:

**A. Crie a rede interna (caso ainda não exista):**

    docker network create andon-net

**B. Construa a imagem e suba o container do Gateway:**

    docker build -t andon-gateway .
    docker run -d --name andon-gateway --network andon-net -p 8080:8080 --env-file app/.env andon-gateway

A API Principal estará orquestrando as requisições na porta **8080**.

### 3. Fluxo de Testes (Postman / Swagger)

> 💡 **Dica:** Utilize a **Collection do Postman** anexada na estrura deste projeto (arquivo: [estevamjr]- Andon IT.postman_collection.json).

**Passo 1: Criar um Usuário**
* **Endpoint:** `POST http://localhost:8080/api/v1/auth/register`
* **Payload (JSON):** `{"username": "admin", "password": "123"}`

**Passo 2: Gerar o Token JWT**
* **Endpoint:** `POST http://localhost:8080/api/v1/auth/login`
* **Payload (JSON):** `{"username": "admin", "password": "123"}`
* *Copie o `access_token` retornado no JSON.*

**Passo 3: Acessar Rotas Protegidas do CRUD (Requer Bearer Token)**
Configure o Header com `Authorization: Bearer <seu_access_token>` e teste as rotas abaixo (conforme disponíveis na Collection):
* **IA Andon (Criar Incidente):** `POST http://localhost:8080/api/v1/telemetry/analyze`
* **Listar Tickets:** `GET http://localhost:8080/api/v1/tickets`
* **Atualizar Ticket:** `PUT http://localhost:8080/api/v1/tickets/<ticket_id>`
* **Deletar Ticket:** `DELETE http://localhost:8080/api/v1/tickets/<ticket_id>`
* **Consultar Logs:** `GET http://localhost:8080/api/v1/logs`

**Passo 4: Acesso ao Swagger UI (Interface Interativa)**
O Gateway expõe a documentação OpenAPI gerada pelo Backend de forma centralizada. Acesse pelo navegador:
👉 `http://localhost:8080/apidocs/`

## 🚀 Como Testar a Aplicação (Guia End-to-End Completo)

Para testar todas as rotas da aplicação, você precisará registrar um usuário, gerar um Token de autenticação e inseri-lo no cabeçalho das requisições subsequentes. O fluxo simula o ciclo de vida real de um incidente e **as rotas são dependentes de estado**. O `ticket_id` gerado pela IA na etapa de análise será obrigatório para as etapas de atualização e deleção.

### 🔐 Configurando a Autenticação (Swagger ou Postman)

**Via Swagger UI:**
1. Acesse `http://localhost:5000/apidocs/` no seu navegador.
2. Execute o Registro e o Login (Passos 1 e 2 abaixo).
3. Copie o valor do `"token"` retornado no Login.
4. Suba até o topo da página, clique no botão **Authorize**, digite `Bearer ` (com um espaço) e cole o token. Clique em *Authorize* e feche. 

**Via Postman:**
1. Importe o arquivo da nossa Collection (`Andon_IT_Postman_Collection.json`).
2. Execute o Registro e o Login (Passos 1 e 2 abaixo).
3. Copie o `"token"` retornado no Login.
4. Na aba **Authorization** de todas as outras rotas, certifique-se de que o tipo **Bearer Token** está selecionado e cole o valor.

---

### 🗺️ Fluxo de Execução Passo a Passo e Payloads

#### Passo 1: Registro de Usuário (Register)
Cria as credenciais para acesso ao sistema.
* **Rota:** `POST /api/v1/auth/register`
* **Body (JSON):**
```json
{
  "username": "admin4",
  "password": "password123"
}
```
* **Resultado Esperado:** Status `201 Created` confirmando a criação do usuário.

#### Passo 2: Autenticação (Login)
* **Rota:** `POST /api/v1/auth/login`
* **Body (JSON):** *(Mesmas credenciais criadas no Passo 1)*
```json
{
  "username": "admin4",
  "password": "password123"
}
```
* **Ação Obrigatória:** Na resposta, copie o valor do `"token"` e configure a autorização (Bearer) conforme explicado no início desta seção. Sem isso, as próximas rotas retornarão erro de não autorizado (401).

#### Passo 3: Análise de Telemetria (Ação Autônoma da IA)
A IA analisa a telemetria, detecta a anomalia e aciona o LLM para gerar o plano de ação, abrindo o incidente.
* **Rota:** `POST /api/v1/andon/analyze`
* **Body (JSON):**
```json
{
  "action_threats": 0,
  "cpu_usage": 85.5,
  "device_id": "servidor_borda_01",
  "mac_address": "00:1B:44:11:3A:B7",
  "ram_usage": 92.0,
  "timestamp": "2026-09-15T22:00:00.000Z",
  "untrusted_processes": 1
}
```
* **Ação Obrigatória (CRÍTICO):** A resposta trará o plano de ação gerado. Localize no JSON de resposta o atributo **`ticket_id`** (Ex: `"ticket_id": "10a40dd8-be61-4c95-8bc6-00e0e80809cf"`). **Copie este ID exato** para utilizá-lo nos Passos 6, 7 e 8.

#### Passo 4: Consultar Histórico da IA (Logs)
Valida o histórico de processos e análises realizadas pela IA.
* **Rota:** `GET /api/v1/logs`
* **Como testar:** Nenhuma alteração na URL ou Body é necessária. Apenas execute.
* **Resultado Esperado:** Retorna a lista completa com o histórico de logs processados pelo sistema.

#### Passo 5: Listar Todos os Incidentes (Tickets)
Valida a persistência dos tickets criados.
* **Rota:** `GET /api/v1/tickets`
* **Como testar:** Nenhuma alteração na URL ou Body é necessária.
* **Resultado Esperado:** Retorna a lista de todos os incidentes (Kanban tickets) abertos no banco de dados.

#### Passo 6: Atualizar o Incidente (Update)
Simula a intervenção humana atualizando o status do ticket.
* **Rota:** `PUT /api/v1/tickets/{ticket_id}`
* **Como testar:** Substitua `{ticket_id}` na URL pelo ID copiado no Passo 3.
* **Body (JSON):**
```json
{
  "assignee_id": "estevamjr",
  "status": "valid"
}
```
* **Resultado Esperado:** Status `200 OK` confirmando a atualização do estado no banco.

#### Passo 7: Encerrar o Incidente (Delete)
Finaliza o ciclo removendo fisicamente o ticket.
* **Rota:** `DELETE /api/v1/tickets/{ticket_id}`
* **Como testar:** Insira o mesmo `{ticket_id}` na URL. Nenhum Body é necessário.
* **Resultado Esperado:** Status `200 OK` e a mensagem de que o ticket foi deletado com sucesso.

#### Passo 8: Prova Real de Deleção (Verify)
Garante que o registro não existe mais no banco de dados.
* **Rota:** `GET /api/v1/tickets/{ticket_id}` *(No Postman, utilize a mesma rota da listagem, mas adicione o ID na URL)*.
* **Como testar:** Insira o `{ticket_id}` deletado na URL.
* **Resultado Esperado:** A aplicação deve retornar **Status 404 (Not Found)** e a mensagem `"Ticket não encontrado"`, provando que a deleção do Passo 7 foi efetivada com sucesso.
* 
> **⚠️ Nota Técnica sobre API Gratuita e Chaves Sensíveis:**
> O consumo do OpenRouter atende ao requisito de IA do projeto (oferece modelos gratuitos). Contudo, testes de estresse comprovaram latência extrema nessas opções. Para garantir o tempo de resposta do Andon e evitar exposição de credenciais, **a chave real da API e a SECRET_KEY não estão versionadas no repositório. Elas possuem saldo ativo e estarão disponíveis exclusivamente na mensagem de publicação do portal**, junto com a Collection do Postman. O avaliador não precisará realizar cadastros.
