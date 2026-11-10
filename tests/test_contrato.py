from pathlib import Path

from recompila_bff.app import create_app
from recompila_bff.contrato import gerar_yaml

RAIZ = Path(__file__).resolve().parents[1]


def test_contrato_yaml_esta_em_dia_com_o_codigo(settings):
    esperado = (RAIZ / "openapi" / "recompila-bff.yaml").read_text(encoding="utf-8")
    assert gerar_yaml(create_app(settings)) == esperado, "Rode: python scripts/exportar_openapi.py"
