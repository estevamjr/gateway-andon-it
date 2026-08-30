import os
import requests
from flask import request

class ProxyService:
    BASE_URL = os.getenv("SECONDARY_API_URL", "http://backend-andon:5000").rstrip("/")

    @classmethod
    def _get_headers(cls):
        headers = {"Content-Type": "application/json"}
        auth_header = request.headers.get("Authorization")
        if auth_header:
            headers["Authorization"] = auth_header
        return headers

    @classmethod
    def _build_url(cls, endpoint: str) -> str:
        return f"{cls.BASE_URL}{endpoint}"

    @classmethod
    def forward_request(cls, method: str, endpoint: str, data=None, params=None):
        url = cls._build_url(endpoint)
        headers = cls._get_headers()

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=100
            )

            try:
                response_data = response.json()
            except ValueError:
                response_data = response.text

            return {
                "status_code": response.status_code,
                "data": response_data
            }

        except requests.exceptions.RequestException as e:
            # Correção: Retorna 502 e o "data" estruturado como dicionário JSON
            return {
                "status_code": 502,
                "data": {
                    "status": "error",
                    "code": 502,
                    "message": f"Erro de comunicação com a API Secundária: {str(e)}"
                }
            }