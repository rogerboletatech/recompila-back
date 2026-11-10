def test_health_eh_publico(cliente):
    assert cliente.get("/health").json() == {"status": "ok"}


def test_rota_sem_token_retorna_401(cliente):
    resposta = cliente.get("/api/trilhas")
    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_invalido_retorna_401(cliente):
    resposta = cliente.get("/api/trilhas", headers={"Authorization": "Bearer nao-eh-jwt"})
    assert resposta.status_code == 401


def test_token_expirado_retorna_401(cliente, gerar_token):
    resposta = cliente.get("/api/trilhas", headers={"Authorization": f"Bearer {gerar_token(expira_em=-60)}"})
    assert resposta.status_code == 401


def test_escopo_insuficiente_retorna_403(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token('recompila:read')}"}
    resposta = cliente.post("/api/cadastro", json={"nome": "Maria", "email": "m@x.com", "trilha": "devs"}, headers=cabecalho)
    assert resposta.status_code == 403


def test_lista_trilhas(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    trilhas = cliente.get("/api/trilhas", headers=cabecalho).json()
    assert [t["id"] for t in trilhas] == ["devs", "pm", "qa", "kids"]


def test_detalha_trilha_e_404_quando_inexistente(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    assert cliente.get("/api/trilhas/pm", headers=cabecalho).json()["nome"] == "Produto"
    assert cliente.get("/api/trilhas/xyz", headers=cabecalho).status_code == 404


def test_conversa_classifica_intencao(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    corpo = cliente.post("/api/conversa", json={"mensagem": "Sou dev front"}, headers=cabecalho).json()
    assert corpo["intencao"] == "stack"
    assert corpo["sugestoes"]


def test_conversa_rejeita_mensagem_vazia(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    assert cliente.post("/api/conversa", json={"mensagem": ""}, headers=cabecalho).status_code == 422


def test_raio_x(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    corpo = cliente.post("/api/raio-x", json={"habilidades": ["Java", "Spring"]}, headers=cabecalho).json()
    assert corpo["trilha_recomendada"] == "devs"


def test_cadastro_cria_inscricao(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    resposta = cliente.post("/api/cadastro", json={"nome": "Maria", "email": "m@x.com", "trilha": "qa"}, headers=cabecalho)
    assert resposta.status_code == 201
    assert resposta.json()["trilha"] == "qa"
    assert resposta.json()["status"] == "recebido"


def test_cadastro_com_trilha_invalida_retorna_422(cliente, gerar_token):
    cabecalho = {"Authorization": f"Bearer {gerar_token()}"}
    resposta = cliente.post("/api/cadastro", json={"nome": "Maria", "email": "m@x.com", "trilha": "xyz"}, headers=cabecalho)
    assert resposta.status_code == 422
    assert "Trilha desconhecida" in resposta.json()["detail"]


def test_openapi_declara_oauth2(cliente):
    esquema = cliente.get("/openapi.json").json()["components"]["securitySchemes"]
    assert any(s["type"] == "oauth2" for s in esquema.values())
