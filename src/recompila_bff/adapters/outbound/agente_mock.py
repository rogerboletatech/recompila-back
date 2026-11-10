"""Agente de conversa simulado. Será trocado pelo serviço real (Spring AI/MCP) na integração."""

import re

from recompila_bff.domain.conversa import RespostaAgente

_GRUPOS: dict[str, frozenset[str]] = {
    "stack": frozenset({"dev", "stack", "programo", "programa", "código", "codigo", "back", "front", "java", "python"}),
    "vaga": frozenset({"vaga", "vagas", "emprego", "entrevista"}),
    "produto": frozenset({"pm", "po", "sm", "produto", "scrum", "backlog"}),
}

_RESPOSTAS: dict[str, tuple[str, tuple[str, ...]]] = {
    "stack": (
        "Vamos mapear sua stack e o nível que você quer alcançar. A trilha de engenharia de software cobre full stack, arquitetura e liderança técnica.",
        ("Qual é a sua stack atual?", "Quero evoluir para arquiteto"),
    ),
    "vaga": (
        "Podemos comparar os requisitos da vaga com o seu perfil e apontar as lacunas.",
        ("Vou enviar a descrição da vaga", "Quais tecnologias eu domino?"),
    ),
    "produto": (
        "Para produto, a trilha foca em discovery, priorização e entrega com times de tecnologia.",
        ("Sou PM, PO ou SM?", "Quero ver a trilha de produto"),
    ),
    "mudar": (
        "Conte um pouco da sua experiência para eu te direcionar melhor.",
        ("Sou dev", "Sou de produto", "Sou de QA"),
    ),
}


class AgenteMock:
    def responder(self, mensagem: str) -> RespostaAgente:
        palavras = set(re.findall(r"\w+", mensagem.lower()))
        intencao = next((chave for chave, sinais in _GRUPOS.items() if palavras & sinais), "mudar")
        texto, sugestoes = _RESPOSTAS[intencao]
        return RespostaAgente(texto=texto, intencao=intencao, sugestoes=sugestoes)
