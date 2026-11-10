from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RespostaAgente:
    texto: str
    intencao: str
    sugestoes: tuple[str, ...]
