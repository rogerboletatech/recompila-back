"""Gera o contrato OpenAPI em YAML a partir da aplicação. O arquivo versionado deve refletir o código."""

from fastapi import FastAPI
import yaml


def gerar_yaml(app: FastAPI) -> str:
    return yaml.safe_dump(app.openapi(), sort_keys=False, allow_unicode=True)
