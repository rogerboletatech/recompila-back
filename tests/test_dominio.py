import pytest

from recompila_bff.domain.cadastro import Candidato
from recompila_bff.domain.erros import ErroDeDominio
from recompila_bff.domain.raio_x import recomendar_trilha


def test_raio_x_recomenda_trilha_pelos_sinais():
    assert recomendar_trilha(["Python", "SQL", "Git"]).trilha == "devs"
    assert recomendar_trilha(["roadmap", "backlog"]).trilha == "pm"
    assert recomendar_trilha(["automação", "Selenium"]).trilha == "qa"


def test_raio_x_sem_sinal_cai_em_devs():
    recomendacao = recomendar_trilha(["culinária"])
    assert recomendacao.trilha == "devs"
    assert "Nenhum sinal claro" in recomendacao.justificativa


def test_raio_x_rejeita_lista_vazia():
    with pytest.raises(ErroDeDominio):
        recomendar_trilha(["  ", ""])


def test_candidato_valido_normaliza_campos():
    candidato = Candidato.criar("  Maria  ", "Maria@Exemplo.com ", "devs")
    assert candidato.nome == "Maria"
    assert candidato.email == "maria@exemplo.com"


@pytest.mark.parametrize(
    ("nome", "email", "trilha", "mensagem"),
    [
        ("M", "m@x.com", "devs", "Nome muito curto."),
        ("Maria", "sem-arroba", "devs", "E-mail inválido."),
        ("Maria", "m@x.com", "inexistente", "Trilha desconhecida"),
    ],
)
def test_candidato_invalido(nome, email, trilha, mensagem):
    with pytest.raises(ErroDeDominio, match=mensagem):
        Candidato.criar(nome, email, trilha)
