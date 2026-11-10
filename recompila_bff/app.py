"""Composição da aplicação: liga adaptadores às portas. É o único lugar que conhece todas as camadas."""

from functools import partial

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from recompila_bff.adapters.inbound.web.rotas import criar_router
from recompila_bff.adapters.inbound.web.seguranca import criar_esquema_oauth2, exigir_escopo
from recompila_bff.adapters.outbound.agente_mock import AgenteMock
from recompila_bff.adapters.outbound.memoria import CatalogoEmMemoria, RepositorioCadastroEmMemoria
from recompila_bff.application.services import ServicoCadastro, ServicoConversa, ServicoRaioX, ServicoTrilhas
from recompila_bff.config import Settings
from recompila_bff.domain.erros import ErroDeDominio


async def _erro_de_dominio(_: Request, exc: ErroDeDominio) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    app = FastAPI(
        title="Recompila BFF",
        version="0.1.0",
        description=(
            "BFF do Recompila. Expõe conversa com o agente, trilhas, raio-x e cadastro "
            "ao front Angular. Autenticação via OAuth2 com Bearer JWT."
        ),
    )

    catalogo = CatalogoEmMemoria()
    esquema = criar_esquema_oauth2(settings)

    app.include_router(
        criar_router(
            servico_conversa=ServicoConversa(AgenteMock()),
            servico_trilhas=ServicoTrilhas(catalogo),
            servico_raio_x=ServicoRaioX(),
            servico_cadastro=ServicoCadastro(RepositorioCadastroEmMemoria()),
            exigir=partial(exigir_escopo, settings, esquema),
        )
    )
    app.add_exception_handler(ErroDeDominio, _erro_de_dominio)

    @app.get("/health", tags=["sistema"], summary="Verifica se o serviço está no ar")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
