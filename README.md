# 🛡️🎫 Ecossistema Andon IT: Documentação Unificada (Gateway & Lógica Preditiva)

Este repositório centraliza a documentação da aplicação, operando sob o padrão de arquitetura de microsserviços. O ecossistema possui dois módulos principais:
* **API Gateway (Módulo Principal):** Atua como um orquestrador e camada de governança inteligente na borda, interceptando requisições (Porta 8080).
* **Ticket-Andon-IT (API Secundária):** Responsável por toda a persistência de dados (I/O), processamento de regras de negócios complexas e classificação de telemetria via algoritmos de Machine Learning (SVM) (Porta 5000).



## 💻 Instruções de Instalação e Execução

⚠️ **Pré-requisito Crítico:** Certifique-se de que o **Docker Desktop** (ou daemon do Docker) esteja em execução na sua máquina antes de iniciar os comandos.

### 1. Criando a Rede Compartilhada
Os containers precisam de uma rede compartilhada para se comunicarem. No terminal, execute:
```bash
docker network create andon-net
```

### 2. Subindo o Backend (API Secundária - Porta 5000)
O banco de dados SQLite requer um mapeamento de volume físico. No terminal, execute:
```bash
git clone https://github.com/estevamjr/ticket-andon-it.git
cd ticket-andon-it/backend
cp .env.example .env
```

*(Nota: A chave do LLM (OpenRouter) foi fornecida na mensagem de publicação do portal da disciplina. Já a Collection está em cada diretório principal do serviço de Gateway e Ticket, com o nome '[estevamjr]- Andon IT.postman_collection.json').*

Abra o arquivo `.env` recém-criado na raiz do backend e insira as credenciais (garantir que o env alterado está dentro do diretório backend):
```env
OPENROUTER_API_KEY=cole_a_chave_do_backend_aqui
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
LLM_MODEL_NAME=google/gemini-3.7-flash
```

⚠️ **Prevenção de Erro no Windows (UTF-8):** Se estiver utilizando o PowerShell no Windows, rode o comando abaixo para garantir que o arquivo `.env` não cause conflitos de codificação no Docker:
```bash
Get-Content .env | Set-Content -Encoding utf8 .env-utf8; Move-Item -Force .env-utf8 .env
```

Construa a imagem e suba o container da API Secundária:
```bash
docker build -t andon-api .
docker run -d --name backend-andon --network andon-net -p 5000:5000 --env-file .env -v "${PWD}/instance:/app/instance" andon-api
```

### 3. Subindo o Gateway (API Principal - Porta 8080)
Volte para a pasta raiz dos seus projetos e execute:
```bash
cd ../..
git clone https://github.com/estevamjr/gateway-andon-it.git
cd gateway-andon-it
cp .env.example .env
```

⚠️ **Atenção Máxima:** Como o Gateway atua apenas como roteador, o arquivo `.env` do Gateway NÃO deve conter chaves de IA. Ele precisa conter estritamente a URL de comunicação com o Backend. Insira a variável abaixo no seu arquivo `.env`:
```env
BACKEND_URL=http://backend-andon:5000
```

Prevenção de Erro no Windows (UTF-8) para o Gateway:
```bash
Get-Content .env | Set-Content -Encoding utf8 .env-utf8; Move-Item -Force .env-utf8 .env
```

Construa a imagem e suba o container do Gateway:
```bash
docker build -t andon-gateway .
docker run -d --name andon-gateway --network andon-net -p 8080:8080 --env-file .env andon-gateway
```

## 🚀 Como Testar a Aplicação (Guia End-to-End Completo)

Para testar todas as rotas da aplicação, você precisará registrar um usuário, gerar um Token de autenticação e inseri-lo no cabeçalho das requisições subsequentes. O fluxo simula o ciclo de vida real de um incidente e **as rotas são dependentes de estado**. O `ticket_id` gerado pela IA na etapa de análise será obrigatório para as etapas de atualização e deleção.

### 🔐 Configurando a Autenticação (Swagger ou Postman)

O Gateway expõe a documentação OpenAPI gerada pelo Backend de forma centralizada. Acesse pelo navegador:
👉 **Swagger UI Interativo:** `http://localhost:8080/apidocs/`

**Via Swagger UI:**
1. Acesse o link acima.
2. Execute o Registro e o Login (Passos 1 e 2 abaixo).
3. Copie o valor do `"token"` retornado no Login.
4. Suba até o topo da página, clique no botão **Authorize**, digite `Bearer ` (com um espaço) e cole o token. Clique em *Authorize* e feche. 

**Via Postman:**
1. Importe o arquivo da nossa Collection (`Andon_IT_Postman_Collection.json`).
2. Execute o Registro e o Login (Passos 1 e 2 abaixo).
3. Copie o `"token"` retornado no Login.
4. Na aba **Authorization** de todas as outras rotas, certifique-se de que o tipo **Bearer Token** está selecionado e cole o valor.

### 🗺️ Fluxo de Execução Passo a Passo e Payloads

#### Passo 1: Registro de Usuário (Register)
Cria as credenciais para acesso ao sistema.
* **Rota:** `POST http://localhost:8080/api/v1/auth/register`
* **Body (JSON):**
```json
{
  "username": "admin",
  "password": "123"
}
```

#### Passo 2: Autenticação (Login)
* **Rota:** `POST http://localhost:8080/api/v1/auth/login`
* **Body (JSON):** *(Mesmas credenciais criadas no Passo 1)*
* **Ação Obrigatória:** Na resposta, copie o valor do `"token"` e configure a autorização (Bearer). Sem isso, as próximas rotas retornarão erro de não autorizado (401).

#### Passo 3: Análise de Telemetria (Ação Autônoma da IA)
A IA analisa a telemetria, detecta a anomalia e aciona o LLM para gerar o plano de ação, abrindo o incidente.
* **Rota:** `POST http://localhost:8080/api/v1/andon/analyze`
* **Body (JSON):**
```json
{
  "device_id": "SRV-TEST-01",
  "cpu_usage_pct": 98.2,
  "mem_available_gb": 0.4,
  "active_threats": 2,
  "untrusted_processes": ["xmrig", "nc_backdoor"],
  "andon_status": 2
}
```
* **Ação Obrigatória (CRÍTICO):** A resposta trará o plano de ação gerado. Localize no JSON de resposta o atributo **`ticket_id`**. **Copie este ID exato** para utilizá-lo nos Passos 6, 7 e 8.

#### Passo 4: Consultar Histórico da IA (Logs)
Valida a persistência das decisões do LLM.
* **Rota:** `GET http://localhost:8080/api/v1/logs`

#### Passo 5: Listar Todos os Incidentes (Tickets)
Valida a persistência dos tickets criados.
* **Rota:** `GET http://localhost:8080/api/v1/tickets`

#### Passo 6: Atualizar o Incidente (Update)
Simula a intervenção humana atualizando o status do ticket.
* **Rota:** `PUT http://localhost:8080/api/v1/tickets/{ticket_id}`
* **Body (JSON):** *(Substitua `{ticket_id}` na URL)*
```json
{
  "assignee_id": "estevamjr",
  "status": "valid"
}
```

#### Passo 7: Encerrar o Incidente (Delete)
Finaliza o ciclo removendo fisicamente o ticket.
* **Rota:** `DELETE http://localhost:8080/api/v1/tickets/{ticket_id}`

#### Passo 8: Prova Real de Deleção (Verify)
Garante que o registro não existe mais no banco de dados.
* **Rota:** `GET http://localhost:8080/api/v1/tickets/{ticket_id}`
* **Resultado Esperado:** A aplicação deve retornar **Status 404 (Not Found)** e a mensagem `"Ticket não encontrado"`.

> **⚠️ Nota Técnica sobre API Gratuita e Chaves Sensíveis:**
> O consumo do OpenRouter atende ao requisito de IA do projeto. Contudo, testes de estresse comprovaram latência extrema nas opções de *free tier*. Para garantir o tempo de resposta do Andon e a estabilidade da avaliação, **a chave real da API não está versionada no repositório, mas possui saldo pré-pago ativo**. Ela estará disponível exclusivamente na mensagem de publicação do portal.

![Arquitetura Andon IT](./Andon%20IT%20-%20Autonomous%20Action.png)

## 🏗️ Arquitetura e Padrões de Projeto

O sistema rompe com a arquitetura monolítica legado para adotar a componentização de serviços:
* **Gateway de Borda & Segurança:** O Gateway centraliza a entrada (porta 8080) e intercepta os cabeçalhos de autorização, atuando como controlador de acesso.
* **Tratamento RFC 9110:** Implementa blindagem semântica. Erros estruturais ou falhas de autenticação são barrados na borda (ex: `401 Unauthorized`, `400 Bad Request`), impedindo o mascaramento de exceções (Erro 500) comuns em arquiteturas distribuídas.
* **Desacoplamento Cognitivo:** A responsabilidade de gerar os planos de ação (playbooks) foi transferida para um modelo LLM externo, aliviando o processamento interno da borda.
* **Roteamento de Alta Fidelidade e Versionamento Estrito:** Para evitar ambiguidades de roteamento (*mismatch* de rotas 404), o Gateway atua com orquestração fiel. Em vez de suprimir (*strip*) o prefixo da URL internamente, a camada de roteamento foi refatorada para preservar e orquestrar a rota exata diretamente ao Backend, garantindo padronização universal do `/v1/`.

## 🏗️ Decisões Arquiteturais e Tech Debts

A separação deste módulo permitiu escalar a persistência e a lógica pesada de forma independente do Gateway:
* **Persistência Orientada a ORM:** Utiliza SQLAlchemy para abstrair transações SQL no **SQLite**. O uso do SQLite simplifica o *setup* do avaliador para o MVP. Contudo, a arquitetura garante **Independência de Banco de Dados**: migrar para um PostgreSQL requer apenas a alteração da variável `DATABASE_URL` no `.env`, sem impacto nas regras de negócio.
* **Componentização Preditiva:** O modelo de Machine Learning (Support Vector Machine) foi encapsulado em um Pipeline estrito do `Scikit-Learn`, mantendo a precisão acima de 80%.
* **Interface de Contrato (Swagger):** Todas as interações e contratos REST foram padronizados via OpenAPI 3 (Flasgger).
* **Versionamento Universal (API e Contratos):** Todos os *controllers* (`auth.py`, `ticket.py`, `andon.py`, `log.py`) foram refatorados para espelhar a exigência do prefixo `/api/v1/`. Isso garante que o Swagger e os endpoints orquestrados pelo Gateway falem exatamente o mesmo idioma, mitigando falhas de comunicação entre os microsserviços.
* **Dívida Técnica (Frontend):** O diretório `/frontend` presente no ecossistema é um módulo legado mantido intencionalmente via estratégia de Arquitetura Evolutiva. Está fora do escopo deste MVP e sua remoção ocorrerá no próximo ciclo.
* **Dívida Técnica (DevOps):** A atual assimetria na orquestração (Gateway via Compose vs. Backend via CLI) foi adotada para facilitar testes isolados. O plano futuro prevê um repositório guarda-chuva com um `docker-compose.yml` global.
* **Roteamento (Low Risk):** A constante de host `BACKEND_URL` presente na configuração principal funciona como *fallback*, sendo redundante em relação à inicialização dinâmica via variável de ambiente. A centralização dessa chamada está mapeada para a próxima iteração.
* **Governança Git:** Para manter o histórico linear e evitar commits de mesclagem não intencionais em um ambiente distribuído, o padrão estabelecido para sincronização de repositório neste projeto é o uso estrito do `git pull --rebase`.

### 🏗️ Decisões Arquiteturais dos Microsserviços

Este projeto adota uma abordagem de arquitetura distribuída, onde cada microsserviço possui uma estrutura de diretórios otimizada para o seu domínio e responsabilidade única:

* **API Gateway (Padrão Proxy/Routing):** Apresenta uma arquitetura enxuta focada em roteamento. Não possui camadas de `models` ou `schemas`, pois não tem responsabilidade de persistência ou regras de negócio complexas. Seu fluxo baseia-se em `controllers` (recepção) e `services` (encaminhamento seguro para o backend).
* **Backend de IA (Arquitetura em Camadas/MVC):** Apresenta uma estrutura mais densa orientada a domínio (Domain-Driven). Inclui pastas como `models` (entidades de banco de dados), `schemas` (validação Pydantic) e `ml_logic` (encapsulamento do modelo SVM). Esta assimetria estrutural garante que cada serviço carregue apenas a complexidade necessária para a sua função, seguindo as melhores práticas de segregação de microsserviços (abordagem que foi fundamental para a refatoração e uso nesta entrega).

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
| **API Secundária (3.0 pts)**| Refatoração em Python (Flask) na porta 5000. Expõe os 4 métodos acessados exclusivamente via Gateway. | ✅ Atingido |
| **API Externa (1.0 pt)** | Integração via `POST` com a API do **OpenRouter** para LLM. Os dados são processados nativamente. | ✅ Atingido |
| **Persistência de Dados** | Mapeamento de dados relacional via SQLAlchemy integrado ao banco **SQLite** local. | ✅ Atingido |
| **Containerização (1.5 pt)**| `Dockerfile` isolado nos repositórios para execução e orquestração manual em rede. | ✅ Atingido |
| **Criatividade (1.0 pt)** | Funcionalidades avançadas além do CRUD básico: autenticação JWT, exceções globais e reutilização de classificação matemática (SVM), documentação robusta, integração entre todas disciplinas do curso. | ✅ Atingido |
| **Documentação (1.0 pt)** | Código organizado no padrão MVC. Repositório com endpoints interativos documentados via Swagger UI. | ✅ Atingido |

## 🌐 Consumo da API Externa

A mitigação automática de incidentes depende do consumo de uma API de inteligência artificial.
* **Serviço Consumido:** OpenRouter (LLMService) utilizando o modelo `google/gemini-3.7-flash`.
* **Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`
* **Licença de Uso:** Token com **saldo pré-pago ativo (Paid Tier)**. A chave fornecida ao avaliador possui créditos para garantir baixa latência e total estabilidade durante a execução dos testes end-to-end.

### 🧠 Validação da Execução do Modelo SVM (Machine Learning)

Para fins de avaliação, a confirmação de que o modelo Support Vector Machine (SVM) está processando os dados em tempo real — e não retornando respostas fixas (*mockadas*) — baseia-se em duas evidências técnicas de Teste de Caixa Preta:

1. **Prova Dinâmica (Entrada vs. Saída):** O sistema reage matematicamente aos dados de entrada. Ao submeter um *payload* com métricas saudáveis (ex: `cpu_usage_pct: 20.0`), a API retorna o status de integridade (`"andon_status": 0`). Injetando dados que simulam um ataque (ex: `cpu_usage_pct: 98.2` e processos maliciosos como `xmrig`), a classificação muda dinamicamente para `"andon_status": 2`. A capacidade de distinguir os dois cenários atesta o funcionamento real do motor de inferência.
```
{
  "device_id": "SRV-TEST-01",
  "cpu_usage_pct": 20.0,
  "mem_available_gb": 16.0,
  "active_threats": 0,
  "untrusted_processes": [],
  "andon_status": 0
}
```
2. **Assinatura de Execução do Scikit-Learn:** O monitoramento dos logs do contêiner (`docker logs backend-andon`) durante uma requisição revela um aviso nativo da biblioteca (`UserWarning: X does not have valid feature names...`). Este log é gerado direta e exclusivamente pelo motor do `scikit-learn` no momento em que o método `.predict()` é invocado, servindo como a "prova térmica" de que a biblioteca de Inteligência Artificial foi instanciada e acionada em tempo real.
```
{
  "cpu_usage_pct": 20.0, 
  "active_threats": 0, 
  "untrusted_processes": []
}
```

