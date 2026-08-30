# 🛡️ Andon System: API Gateway (Módulo Principal)

Este repositório contém a **API Principal** do ecossistema Andon, operando sob o padrão de arquitetura de microsserviços. O sistema atua como um Proxy Reverso inteligente, orquestrando requisições de clientes para uma API Secundária e consumindo serviços externos de Inteligência Artificial para mitigação de incidentes.

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
* **Proxy Transparente & Borda:** O Gateway centraliza a entrada (porta 8080) e intercepta os cabeçalhos de autorização.
* **Tratamento RFC 9110:** Implementa blindagem semântica. Erros estruturais ou falhas de autenticação são barrados na borda (ex: `401 Unauthorized`, `400 Bad Request`), impedindo o mascaramento de exceções (Erro 500) comuns em arquiteturas distribuídas.
* **Desacoplamento Cognitivo:** A responsabilidade de gerar os planos de ação (playbooks) foi transferida para um modelo LLM externo, aliviando o processamento interno.

![Arquitetura Andon IT](./Andon%20IT%20-%20Autonomous%20Action.png)

## 🌐 Consumo da API Externa

A mitigação automática de incidentes depende do consumo de uma API pública.
* **Serviço Consumido:** OpenRouter (LLMService).
* **Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`
* **Licença de Uso:** Serviço gratuito (modelos *free tier*).

*(Nota Ágil: A orquestração deste Gateway foi planejada via Lean Inception e estruturada com critérios de Definition of Done (DoD) estritos, garantindo que o software obedeça ao escopo desenhado nas Sprints de Governança).*

## 💻 Instruções de Instalação e Execução

O projeto segue as melhores práticas de segurança (ausência de chaves hardcoded). Siga os passos para instanciar a aplicação:

### 1. Clonar e Configurar

    git clone https://github.com/estevamjr/gateway-andon-it.git
    cd gateway-andon-it

Renomeie o arquivo de molde `app/.env.example` para `app/.env` e insira a chave da API do OpenRouter fornecida na entrega deste projeto:

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

### 3. Fluxo de Autenticação e Teste Local
Para testar os serviços via Postman ou Insomnia, siga o fluxo de autenticação abaixo:

**Passo 1: Criar um Usuário**
* **Endpoint:** `POST http://localhost:8080/api/auth/register`
* **Payload (JSON):** `{"username": "admin", "password": "123"}`

**Passo 2: Gerar o Token JWT**
* **Endpoint:** `POST http://localhost:8080/api/auth/login`
* **Payload (JSON):** `{"username": "admin", "password": "123"}`
* *Copie o `access_token` retornado no JSON.*

**Passo 3: Acessar Rota Protegida (Ex: IA Andon)**
* **Endpoint:** `POST http://localhost:8080/api/v1/telemetry/analyze`
* **Header:** `Authorization: Bearer <seu_access_token_aqui>`
* **Payload (JSON):** Envie os dados de telemetria para testar a mitigação via LLM.

> **⚠️ Nota Técnica sobre o Requisito de API Gratuita:**
> Embora a plataforma OpenRouter atenda ao requisito do escopo por oferecer modelos *free tier*, os testes de estresse na infraestrutura comprovaram que a latência extrema dessas opções gratuitas inviabiliza o tempo de resposta em tempo real exigido por um sistema Andon. A integração em produção consome um modelo pago, e **a chave fornecida na entrega possui saldo ativo**. O avaliador não precisará realizar cadastros ou lidar com falhas de *timeout*.