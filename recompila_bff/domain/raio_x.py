from dataclasses import dataclass

from recompila_bff.domain.erros import ErroDeDominio

# Palavras que indicam aderência a cada trilha. Regra de negócio pura, sem I/O.
_SINAIS: dict[str, frozenset[str]] = {
    "devs": frozenset({"python", "java", "javascript", "typescript", "angular", "react", "spring", "sql", "api", "git", "front", "back", "programacao", "código", "codigo"}),
    "pm": frozenset({"produto", "backlog", "roadmap", "priorizacao", "priorização", "stakeholders", "discovery", "pm", "po", "sm", "scrum"}),
    "qa": frozenset({"teste", "testes", "qa", "automacao", "automação", "regressao", "regressão", "cypress", "selenium"}),
    "kids": frozenset({"escola", "kids", "criança", "crianca", "professor"}),
}


@dataclass(frozen=True, slots=True)
class RecomendacaoRaioX:
    trilha: str
    justificativa: str


def recomendar_trilha(habilidades: list[str]) -> RecomendacaoRaioX:
    normalizadas = {h.strip().lower() for h in habilidades if h.strip()}
    if not normalizadas:
        raise ErroDeDominio("Informe ao menos uma habilidade.")

    ordem = list(_SINAIS)
    pontuacao = {trilha: len(normalizadas & sinais) for trilha, sinais in _SINAIS.items()}
    melhor = max(ordem, key=lambda t: (pontuacao[t], -ordem.index(t)))

    if pontuacao[melhor] == 0:
        return RecomendacaoRaioX("devs", "Nenhum sinal claro. A trilha de engenharia de software é o ponto de partida.")
    return RecomendacaoRaioX(melhor, f"{pontuacao[melhor]} habilidade(s) alinhadas a esta trilha.")
