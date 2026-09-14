import requests
from flask import request, Response
from flask_restful import Resource, Api
from app.services.proxy_service import ProxyService
from app.utils.httpResponses import success_200, success_201, error_400, error_404, error_500

BACKEND_URL = "http://backend-andon:5000"

def _format_response(result):
    # PROXY TRANSPARENTE: Repassa o JSON e o código HTTP originais do Backend
    return result["data"], result["status_code"]

# ==========================================
# ROTAS DO SWAGGER
# ==========================================
class SwaggerUIResource(Resource):
    def get(self):
        resp = requests.get(f"{BACKEND_URL}/apidocs/")
        headers = {k: v for k, v in resp.headers.items() if k.lower() not in ['transfer-encoding', 'content-encoding']}
        return Response(resp.content, resp.status_code, headers)

class SwaggerJSONResource(Resource):
    def get(self):
        resp = requests.get(f"{BACKEND_URL}/apispec_1.json")
        headers = {k: v for k, v in resp.headers.items() if k.lower() not in ['transfer-encoding', 'content-encoding']}
        return Response(resp.content, resp.status_code, headers)

class SwaggerStaticResource(Resource):
    def get(self, filename):
        resp = requests.get(f"{BACKEND_URL}/flasgger_static/{filename}")
        headers = {k: v for k, v in resp.headers.items() if k.lower() not in ['transfer-encoding', 'content-encoding']}
        return Response(resp.content, resp.status_code, headers)

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================
class AuthRegisterResource(Resource):
    def post(self):
        payload = request.get_json(silent=True) or {}
        result = ProxyService.forward_request("POST", "/api/v1/auth/register", data=payload)
        return _format_response(result)

class AuthLoginResource(Resource):
    def post(self):
        payload = request.get_json(silent=True) or {}
        result = ProxyService.forward_request("POST", "/api/v1/auth/login", data=payload)
        return _format_response(result)

# ==========================================
# ROTAS DA APLICAÇÃO (ORIGINAIS)
# ==========================================
class TelemetryAnalyzeResource(Resource):
    def post(self):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("POST", "/api/v1/andon/analyze", data=payload)
        return _format_response(result)

class TicketListCreateResource(Resource):
    def get(self):
        result = ProxyService.forward_request("GET", "/api/v1/tickets", params=request.args.to_dict())
        return _format_response(result)

    def post(self):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("POST", "/api/v1/tickets", data=payload)
        return _format_response(result)

class TicketDetailResource(Resource):
    def put(self, ticket_id: str):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("PUT", f"/api/v1/tickets/{ticket_id}", data=payload)
        return _format_response(result)

    def delete(self, ticket_id: str):
        result = ProxyService.forward_request("DELETE", f"/api/v1/tickets/{ticket_id}")
        return _format_response(result)

class LogsResource(Resource):
    def get(self):
        result = ProxyService.forward_request("GET", "/api/v1/logs", params=request.args.to_dict())
        return _format_response(result)

# ==========================================
# INICIALIZAÇÃO
# ==========================================
def initializeProxyRoutes(api: Api):
    # Auth
    api.add_resource(AuthRegisterResource, '/api/v1/auth/register')
    api.add_resource(AuthLoginResource, '/api/v1/auth/login')
    
    # App (Rotas exatas espelhando o Swagger do Backend)
    api.add_resource(TelemetryAnalyzeResource, '/api/v1/andon/analyze')
    api.add_resource(TicketListCreateResource, '/api/v1/tickets')
    api.add_resource(TicketDetailResource, '/api/v1/tickets/<string:ticket_id>')
    api.add_resource(LogsResource, '/api/v1/logs')
    
    # Swagger
    api.add_resource(SwaggerUIResource, '/apidocs/')
    api.add_resource(SwaggerJSONResource, '/apispec_1.json')
    api.add_resource(SwaggerStaticResource, '/flasgger_static/<path:filename>')