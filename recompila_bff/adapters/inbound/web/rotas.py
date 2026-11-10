"""Adaptador de entrada HTTP. Traduz requisições em chamadas aos casos de uso."""

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from recompila_bff.adapters.inbound.web.schemas import (
    CadastroIn,
    CadastroOut,
    ConversaIn,
    ConversaOut,
    RaioXIn,
    RaioXOut,
    TrilhaOut,
)
from recompila_bff.application.ports.inbound.casos_de_uso import Cadastrar, Conversar, ConsultarTrilhas, RecomendarTrilha
from recompila_bff.domain.trilhas import Trilha

ESCOPO_LEITURA = "recompila:read"
ESCOPO_ESCRITA = "recompila:write"

_RESPOSTAS_AUTH = {
    401: {"description": "Token ausente ou inválido"},
    403: {"description": "Escopo insuficiente"},
}


def _trilha_out(trilha: Trilha) -> TrilhaOut:
    return TrilhaOut(id=trilha.id, nome=trilha.nome, titulo=trilha.titulo, resumo=trilha.resumo)


def criar_router(
    servico_conversa: Conversar,
    servico_trilhas: ConsultarTrilhas,
    servico_raio_x: RecomendarTrilha,
    servico_cadastro: Cadastrar,
    exigir: Callable[[str], Any],
) -> APIRouter:
    router = APIRouter(prefix="/api")
    leitura = Depends(exigir(ESCOPO_LEITURA))
    escrita = Depends(exigir(ESCOPO_ESCRITA))

    @router.post(
        "/conversa",
        response_model=ConversaOut,
        tags=["conversa"],
        summary="Envia uma mensagem ao agente",
        responses=_RESPOSTAS_AUTH,
    )
    def post_conversa(corpo: ConversaIn, _: dict = leitura) -> ConversaOut:
        resposta = servico_conversa.conversar(corpo.mensagem)
        return ConversaOut(texto=resposta.texto, intencao=resposta.intencao, sugestoes=list(resposta.sugestoes))

    @router.get(
        "/trilhas",
        response_model=list[TrilhaOut],
        tags=["trilhas"],
        summary="Lista as trilhas do Recompila",
        responses=_RESPOSTAS_AUTH,
    )
    def get_trilhas(_: dict = leitura) -> list[TrilhaOut]:
        return [_trilha_out(t) for t in servico_trilhas.listar()]

    @router.get(
        "/trilhas/{trilha_id}",
        response_model=TrilhaOut,
        tags=["trilhas"],
        summary="Detalha uma trilha",
        responses={**_RESPOSTAS_AUTH, 404: {"description": "Trilha não encontrada"}},
    )
    def get_trilha(trilha_id: str, _: dict = leitura) -> TrilhaOut:
        trilha = servico_trilhas.buscar(trilha_id)
        if trilha is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trilha não encontrada.")
        return _trilha_out(trilha)

    @router.post(
        "/raio-x",
        response_model=RaioXOut,
        tags=["raio-x"],
        summary="Recomenda uma trilha a partir das habilidades informadas",
        responses=_RESPOSTAS_AUTH,
    )
    def post_raio_x(corpo: RaioXIn, _: dict = leitura) -> RaioXOut:
        recomendacao = servico_raio_x.recomendar(corpo.habilidades)
        return RaioXOut(trilha_recomendada=recomendacao.trilha, justificativa=recomendacao.justificativa)

    @router.post(
        "/cadastro",
        response_model=CadastroOut,
        status_code=status.HTTP_201_CREATED,
        tags=["cadastro"],
        summary="Inscreve a pessoa em uma trilha",
        responses=_RESPOSTAS_AUTH,
    )
    def post_cadastro(corpo: CadastroIn, _: dict = escrita) -> CadastroOut:
        inscricao = servico_cadastro.cadastrar(corpo.nome, corpo.email, corpo.trilha)
        return CadastroOut(id=inscricao.id, trilha=inscricao.candidato.trilha, status=inscricao.status)

    return router
