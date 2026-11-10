"""Portas de entrada: o que o mundo externo pode pedir ao núcleo."""

from typing import Protocol

from recompila_bff.domain.cadastro import Inscricao
from recompila_bff.domain.conversa import RespostaAgente
from recompila_bff.domain.raio_x import RecomendacaoRaioX
from recompila_bff.domain.trilhas import Trilha


class ConsultarTrilhas(Protocol):
    def listar(self) -> list[Trilha]: ...

    def buscar(self, trilha_id: str) -> Trilha | None: ...


class Conversar(Protocol):
    def conversar(self, mensagem: str) -> RespostaAgente: ...


class RecomendarTrilha(Protocol):
    def recomendar(self, habilidades: list[str]) -> RecomendacaoRaioX: ...


class Cadastrar(Protocol):
    def cadastrar(self, nome: str, email: str, trilha: str) -> Inscricao: ...
