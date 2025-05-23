pip install diagrams
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Flask
from diagrams.onprem.id import Keycloak

with Diagram("IAM Architecture - Keycloak + Flask OAuth2", show=True, direction="LR"):

    user = User("User")
    client = Nginx("Client (Frontend App)")
    keycloak = Keycloak("Keycloak IdP\n(OAuth2 / OIDC)")
    flask_api = Flask("Flask API\n(Resource Server)")
    jwks = Server("JWKS Endpoint\n(Keycloak)")

    user >> Edge(label="Login / Auth Code Flow") >> client
    client >> Edge(label="OAuth2 Tokens\n(Access Token)") >> user

    client >> Edge(label="Bearer Token\nAPI Calls") >> flask_api
    flask_api >> Edge(label="Token Validation\n(Fetch JWKS)") >> jwks
    jwks >> keycloak  # JWKS keys served by Keycloak

    client >> Edge(style="dotted", label="OAuth2 Auth Code Flow\nRedirects to IdP") >> keycloak
    keycloak >> Edge(style="dotted", label="Auth Tokens") >> client
