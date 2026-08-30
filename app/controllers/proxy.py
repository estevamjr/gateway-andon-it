from flask import request
from flask_restful import Resource, Api
from app.services.proxy_service import ProxyService
from app.utils.httpResponses import success_200, success_201, error_400, error_404, error_500

def _format_response(result):
    # PROXY TRANSPARENTE: Repassa o JSON e o código HTTP originais do Backend
    return result["data"], result["status_code"]

class TelemetryAnalyzeResource(Resource):
    def post(self):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("POST", "/api/andon/analyze", data=payload)
        return _format_response(result)

class TicketListCreateResource(Resource):
    def get(self):
        result = ProxyService.forward_request("GET", "/api/tickets", params=request.args.to_dict())
        return _format_response(result)

    def post(self):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("POST", "/api/tickets", data=payload)
        return _format_response(result)

class TicketDetailResource(Resource):
    def put(self, ticket_id: str):
        payload = request.get_json(silent=True)
        if not payload:
            return error_400("Payload JSON ausente ou inválido.")
        result = ProxyService.forward_request("PUT", f"/api/tickets/{ticket_id}", data=payload)
        return _format_response(result)

    def delete(self, ticket_id: str):
        result = ProxyService.forward_request("DELETE", f"/api/tickets/{ticket_id}")
        return _format_response(result)

class LogsResource(Resource):
    def get(self):
        result = ProxyService.forward_request("GET", "/api/logs", params=request.args.to_dict())
        return _format_response(result)

def initializeProxyRoutes(api: Api):
    api.add_resource(TelemetryAnalyzeResource, '/api/v1/telemetry/analyze')
    api.add_resource(TicketListCreateResource, '/api/v1/tickets')
    api.add_resource(TicketDetailResource, '/api/v1/tickets/<string:ticket_id>')
    api.add_resource(LogsResource, '/api/v1/logs')