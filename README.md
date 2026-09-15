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

> **⚠️ Nota Técnica sobre API Gratuita e Chaves Sensíveis:**
> O consumo do OpenRouter atende ao requisito de IA do projeto (oferece modelos gratuitos). Contudo, testes de estresse comprovaram latência extrema nessas opções. Para garantir o tempo de resposta do Andon e evitar exposição de credenciais, **a chave real da API e a SECRET_KEY não estão versionadas no repositório. Elas possuem saldo ativo e estarão disponíveis exclusivamente na mensagem de publicação do portal**, junto com a Collection do Postman. O avaliador não precisará realizar cadastros.
