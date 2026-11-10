import time

import jwt
import pytest
from fastapi.testclient import TestClient

from recompila_bff.app import create_app
from recompila_bff.config import Settings

CHAVE = "chave-de-teste-com-pelo-menos-32-bytes"
EMISSOR = "https://auth.recompila.local/"
PUBLICO = "recompila-bff"


@pytest.fixture
def settings() -> Settings:
    return Settings(jwt_key=CHAVE, jwt_issuer=EMISSOR, jwt_audience=PUBLICO)


@pytest.fixture
def cliente(settings: Settings) -> TestClient:
    return TestClient(create_app(settings))


@pytest.fixture
def gerar_token():
    def _gerar(escopo: str = "recompila:read recompila:write", expira_em: int = 300) -> str:
        agora = int(time.time())
        claims = {"sub": "teste", "iss": EMISSOR, "aud": PUBLICO, "iat": agora, "exp": agora + expira_em, "scope": escopo}
        return jwt.encode(claims, CHAVE, algorithm="HS256")

    return _gerar
