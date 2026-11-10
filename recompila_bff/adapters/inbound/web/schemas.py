"""Modelos de entrada e saída HTTP. Refletem o contrato em openapi/recompila-bff.yaml."""

from typing import Annotated

from pydantic import BaseModel, Field

Texto = Annotated[str, Field(min_length=1, max_length=60)]


class ConversaIn(BaseModel):
    mensagem: str = Field(min_length=1, max_length=2000, examples=["Sou dev front, quero virar arquiteto"])


class ConversaOut(BaseModel):
    texto: str
    intencao: str = Field(examples=["stack"])
    sugestoes: list[str]


class TrilhaOut(BaseModel):
    id: str = Field(examples=["devs"])
    nome: str
    titulo: str
    resumo: str


class RaioXIn(BaseModel):
    habilidades: list[Texto] = Field(min_length=1, max_length=30, examples=[["Python", "SQL", "Git"]])


class RaioXOut(BaseModel):
    trilha_recomendada: str = Field(examples=["devs"])
    justificativa: str


class CadastroIn(BaseModel):
    nome: str = Field(min_length=2, max_length=120, examples=["Maria Souza"])
    email: str = Field(max_length=254, examples=["maria@exemplo.com"])
    trilha: str = Field(examples=["devs"])


class CadastroOut(BaseModel):
    id: str
    trilha: str
    status: str = Field(examples=["recebido"])
