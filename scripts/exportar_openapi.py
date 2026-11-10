"""Regenera openapi/recompila-bff.yaml. Rode sempre que mudar uma rota ou schema."""

from pathlib import Path

from recompila_bff.app import create_app
from recompila_bff.config import Settings
from recompila_bff.contrato import gerar_yaml

RAIZ = Path(__file__).resolve().parents[1]


def main() -> None:
    # A chave não é usada na geração do contrato; só precisa existir para montar a aplicação.
    app = create_app(Settings(jwt_key="contrato-gerado-sem-validacao-de-token"))
    destino = RAIZ / "openapi" / "recompila-bff.yaml"
    destino.write_text(gerar_yaml(app), encoding="utf-8")
    print(f"Contrato gerado em {destino}")


if __name__ == "__main__":
    main()
