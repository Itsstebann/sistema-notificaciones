def test_registro(client):
    res = client.post("/auth/registro", json={"email": "test@test.com", "password": "password123"})
    assert res.status_code == 200
    assert res.json()["email"] == "test@test.com"

def test_login(client):
    client.post("/auth/registro", json={"email": "test@test.com", "password": "password123"})
    res = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_crear_notificacion(client):
    client.post("/auth/registro", json={"email": "test@test.com", "password": "password123"})
    login = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/notificaciones/", json={"titulo": "Test", "mensaje": "Mensaje de prueba", "usuario_id": 1}, headers=headers)
    assert res.status_code == 200
    assert res.json()["titulo"] == "Test"

def test_listar_notificaciones(client):
    client.post("/auth/registro", json={"email": "test@test.com", "password": "password123"})
    login = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/notificaciones/", json={"titulo": "Test", "mensaje": "Mensaje", "usuario_id": 1}, headers=headers)
    res = client.get("/notificaciones/", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_marcar_leida(client):
    client.post("/auth/registro", json={"email": "test@test.com", "password": "password123"})
    login = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    notif = client.post("/notificaciones/", json={"titulo": "Test", "mensaje": "Mensaje", "usuario_id": 1}, headers=headers)
    notif_id = notif.json()["id"]
    res = client.patch(f"/notificaciones/{notif_id}/leer", headers=headers)
    assert res.status_code == 200
    assert res.json()["leida"] == True

def test_sin_token(client):
    res = client.get("/notificaciones/")
    assert res.status_code == 401
