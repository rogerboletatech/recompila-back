"""OAuth2 (Authorization Code com Bearer JWT). O BFF valida tokens; quem emite é o servidor de autorização."""

from collections.abc import Callable

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from recompila_bff.config import Settings

ESCOPOS = {
    "recompila:read": "Ler trilhas, conversar com o agente e fazer o raio-x",
    "recompila:write": "Enviar cadastro para uma trilha",
}


def criar_esquema_oauth2(settings: Settings) -> OAuth2AuthorizationCodeBearer:
    return OAuth2AuthorizationCodeBearer(
        authorizationUrl=settings.oauth_authorization_url,
        tokenUrl=settings.oauth_token_url,
        scopes=ESCOPOS,
        auto_error=False,
    )


def exigir_escopo(settings: Settings, esquema: OAuth2AuthorizationCodeBearer, escopo: str) -> Callable[..., dict]:
    def dependencia(token: str | None = Security(esquema, scopes=[escopo])) -> dict:
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token ausente.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            claims = jwt.decode(
                token,
                settings.jwt_key,
                algorithms=[settings.jwt_algorithm],
                audience=settings.jwt_audience,
                issuer=settings.jwt_issuer,
                options={"require": ["exp", "iss", "aud"]},
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        if escopo not in str(claims.get("scope", "")).split():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Escopo insuficiente.")
        return claims

    return dependencia
