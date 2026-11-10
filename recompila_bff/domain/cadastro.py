import re
import uuid
from dataclasses import dataclass

from recompila_bff.domain.erros import ErroDeDominio
from recompila_bff.domain.trilhas import TRILHAS_IDS

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class Candidato:
    nome: str
    email: str
    trilha: str

    @classmethod
    def criar(cls, nome: str, email: str, trilha: str) -> "Candidato":
        nome = nome.strip()
        email = email.strip().lower()
        if len(nome) < 2:
            raise ErroDeDominio("Nome muito curto.")
        if not _EMAIL.match(email):
            raise ErroDeDominio("E-mail inválido.")
        if trilha not in TRILHAS_IDS:
            raise ErroDeDominio(f"Trilha desconhecida: {trilha}.")
        return cls(nome=nome, email=email, trilha=trilha)


@dataclass(frozen=True, slots=True)
class Inscricao:
    id: str
    candidato: Candidato
    status: str

    @classmethod
    def nova(cls, candidato: Candidato) -> "Inscricao":
        return cls(id=str(uuid.uuid4()), candidato=candidato, status="recebido")
