"""Portas de saída: o que o núcleo precisa do mundo externo."""

from typing import Protocol

from recompila_bff.domain.cadastro import Inscricao
from recompila_bff.domain.conversa import RespostaAgente
from recompila_bff.domain.trilhas import Trilha


class CatalogoTrilhas(Protocol):
    def listar(self) -> list[Trilha]: ...

    def buscar(self, trilha_id: str) -> Trilha | None: ...


class AgenteConversa(Protocol):
    def responder(self, mensagem: str) -> RespostaAgente: ...


class RepositorioCadastro(Protocol):
    def salvar(self, inscricao: Inscricao) -> None: ...
