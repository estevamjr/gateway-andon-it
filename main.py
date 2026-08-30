import os
from flask import Flask
from flask_restful import Api
from app.controllers.proxy import initializeProxyRoutes

def create_app():
    app = Flask(__name__)
    api = Api(app)

    initializeProxyRoutes(api)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
