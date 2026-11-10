"""Configuração carregada de variáveis de ambiente com prefixo RECOMPILA_."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECOMPILA_", env_file=".env", extra="ignore")

    # Chave de validação dos tokens (HS256 usa segredo; RS256 usa a chave pública em PEM).
    jwt_key: str
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "https://auth.recompila.local/"
    jwt_audience: str = "recompila-bff"

    # Endpoints do servidor de autorização, exibidos no Swagger UI para o fluxo OAuth2.
    oauth_authorization_url: str = "https://auth.recompila.local/oauth2/authorize"
    oauth_token_url: str = "https://auth.recompila.local/oauth2/token"
