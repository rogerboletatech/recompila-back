"""Casos de uso: orquestram domínio e portas de saída. Não conhecem HTTP."""

from recompila_bff.application.ports.outbound.dependencias import AgenteConversa, CatalogoTrilhas, RepositorioCadastro
from recompila_bff.domain.cadastro import Candidato, Inscricao
from recompila_bff.domain.conversa import RespostaAgente
from recompila_bff.domain.erros import ErroDeDominio
from recompila_bff.domain.raio_x import RecomendacaoRaioX, recomendar_trilha
from recompila_bff.domain.trilhas import Trilha


class ServicoConversa:
    def __init__(self, agente: AgenteConversa) -> None:
        self._agente = agente

    def conversar(self, mensagem: str) -> RespostaAgente:
        texto = mensagem.strip()
        if not texto:
            raise ErroDeDominio("Mensagem vazia.")
        return self._agente.responder(texto)


class ServicoTrilhas:
    def __init__(self, catalogo: CatalogoTrilhas) -> None:
        self._catalogo = catalogo

    def listar(self) -> list[Trilha]:
        return self._catalogo.listar()

    def buscar(self, trilha_id: str) -> Trilha | None:
        return self._catalogo.buscar(trilha_id)


class ServicoRaioX:
    def recomendar(self, habilidades: list[str]) -> RecomendacaoRaioX:
        return recomendar_trilha(habilidades)


class ServicoCadastro:
    def __init__(self, repositorio: RepositorioCadastro) -> None:
        self._repositorio = repositorio

    def cadastrar(self, nome: str, email: str, trilha: str) -> Inscricao:
        candidato = Candidato.criar(nome, email, trilha)
        inscricao = Inscricao.nova(candidato)
        self._repositorio.salvar(inscricao)
        return inscricao
