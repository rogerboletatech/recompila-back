"""Adaptadores de saída em memória. Mock até existirem os serviços reais."""

from recompila_bff.domain.cadastro import Inscricao
from recompila_bff.domain.trilhas import Trilha

_TRILHAS: tuple[Trilha, ...] = (
    Trilha("devs", "Engenheiro de software", "Engenheiro de software: full stack, com arquitetura e liderança técnica", "Para quem já programa e quer desenhar soluções sem depender de ninguém."),
    Trilha("pm", "Produto", "Produto: PM, PO e SM", "Discovery, priorização, backlog e entrega com times de tecnologia."),
    Trilha("qa", "Qualidade", "Qualidade e automação", "Estratégia de testes, automação e qualidade contínua."),
    Trilha("kids", "Kids", "Recompila Kids para escolas", "Lógica e programação para alunos da escola básica."),
)


class CatalogoEmMemoria:
    def __init__(self) -> None:
        self._por_id = {t.id: t for t in _TRILHAS}

    def listar(self) -> list[Trilha]:
        return list(_TRILHAS)

    def buscar(self, trilha_id: str) -> Trilha | None:
        return self._por_id.get(trilha_id)


class RepositorioCadastroEmMemoria:
    def __init__(self) -> None:
        self._inscricoes: dict[str, Inscricao] = {}

    def salvar(self, inscricao: Inscricao) -> None:
        # O e-mail fica só no registro; nunca vai para logs.
        self._inscricoes[inscricao.id] = inscricao
