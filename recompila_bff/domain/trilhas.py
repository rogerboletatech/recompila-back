from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trilha:
    id: str
    nome: str
    titulo: str
    resumo: str


TRILHAS_IDS: tuple[str, ...] = ("devs", "pm", "qa", "kids")
