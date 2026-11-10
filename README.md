# recompila-back (BFF)

Backend-for-frontend do Recompila em FastAPI. Expõe conversa com o agente, trilhas, raio-x e cadastro para o front Angular. Autenticação OAuth2 (Bearer JWT). Arquitetura hexagonal.

## Estrutura

```
src/recompila_bff/
├── domain/                  regras de negócio puras (sem FastAPI)
├── application/
│   ├── ports/inbound/       casos de uso expostos ao mundo externo
│   ├── ports/outbound/      o que o núcleo precisa de fora (catálogo, agente, repositório)
│   └── services.py          orquestração dos casos de uso
├── adapters/
│   ├── inbound/web/         rotas HTTP, schemas, segurança OAuth2
│   └── outbound/            implementações (hoje em memória e mock do agente)
├── app.py                   composição: liga adaptadores às portas
└── main.py                  ponto de entrada do uvicorn
openapi/recompila-bff.yaml   contrato gerado a partir do código
```

## Rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env            # ajuste RECOMPILA_JWT_KEY
uvicorn recompila_bff.main:app --reload
```

Swagger UI em `http://localhost:8000/docs`. O botão Authorize usa o fluxo OAuth2 configurado em `RECOMPILA_OAUTH_*`.

## Testes e contrato

```bash
pytest
python scripts/exportar_openapi.py   # regenere após mudar rotas ou schemas
```

O teste `test_contrato` falha se o YAML versionado estiver diferente do código.

## Autenticação

O BFF valida o JWT (assinatura, `iss`, `aud`, `exp`) e exige o escopo da rota: `recompila:read` para leitura e conversa, `recompila:write` para cadastro. O servidor de autorização que emite os tokens ainda não foi escolhido.
