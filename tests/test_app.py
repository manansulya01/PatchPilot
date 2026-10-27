from fastapi.testclient import TestClient

from app import app, _config, _config_lock

client = TestClient(app)


def setup_function():
    with _config_lock:
        _config["api_key"] = ""
        _config["model"] = ""
        _config["base_url"] = "https://api.tokenfactory.nebius.com/v1"


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_homepage_serves_product_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "PatchPilot" in response.text
    assert "Don't trust the patch" in response.text


def test_demo_analysis_is_explicitly_unverified():
    response = client.post("/api/analyze", json={
        "description": "The checkout discount total is wrong for multiple items.",
        "code": "def calculate_total(prices, discount):\n    return sum(prices)",
        "language": "python",
        "mode": "demo",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "demo"
    assert data["verification"]["executed"] is False
    assert data["verification"]["label"] == "NOT RUN"
    assert "patch_review" in data
    assert len(data["provenance"]["input_sha256"]) == 64
    assert len(data["provenance"]["patch_sha256"]) == 64
    assert data["challenge_review"]["status"] == "NOT RUN IN DEMO"
    assert data["patch_review"]["status"] in {"REVIEW REQUIRED", "NO HEURISTIC FLAGS", "NO PATCH"}
    assert "not" in data["risks"][1].lower() or "no code" in data["risks"][1].lower()


def test_connection_test_requires_configuration():
    response = client.post("/api/config/test")
    assert response.status_code == 503


def test_live_mode_requires_configuration():
    response = client.post("/api/analyze", json={
        "description": "A sufficiently detailed bug report.",
        "code": "print('hello')",
        "language": "python",
        "mode": "live",
    })
    assert response.status_code == 503


def test_config_never_returns_api_key():
    response = client.post("/api/config", json={
        "api_key": "secret-example",
        "base_url": "https://api.tokenfactory.nebius.com/v1",
        "model": "example/model",
    })
    assert response.status_code == 200
    assert "api_key" not in response.json()
    assert "secret-example" not in response.text
    assert client.get("/api/config").json()["configured"] is True


def test_rejects_insecure_remote_base_url():
    response = client.post("/api/config", json={
        "api_key": "secret-example",
        "base_url": "http://example.com/v1",
        "model": "example/model",
    })
    assert response.status_code == 400


def test_connection_test_reports_success_without_key_leak(monkeypatch):
    from types import SimpleNamespace

    with _config_lock:
        _config["api_key"] = "test-secret"
        _config["model"] = "nvidia/Nemotron-3_5-Lightning"
        _config["base_url"] = "https://api.tokenfactory.nebius.com/v1"

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **request: SimpleNamespace(
                        model=request["model"],
                        choices=[SimpleNamespace(message=SimpleNamespace(content="PATCHPILOT_CONNECTION_OK"))],
                    )
                )
            )

    monkeypatch.setattr("app.OpenAI", FakeOpenAI)
    response = client.post("/api/config/test")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["model"] == "nvidia/Nemotron-3_5-Lightning"
    assert data["response_preview"] == "PATCHPILOT_CONNECTION_OK"
    assert "test-secret" not in response.text


def test_connection_test_disabled_on_public_deployment(monkeypatch):
    monkeypatch.setenv("PATCHPILOT_ALLOW_RUNTIME_CONFIG", "false")
    response = client.post("/api/config/test")
    assert response.status_code == 403


def test_config_reports_runtime_configuration_policy(monkeypatch):
    monkeypatch.setenv("PATCHPILOT_ALLOW_RUNTIME_CONFIG", "false")
    response = client.get("/api/config")
    assert response.status_code == 200
    assert response.json()["runtime_config_allowed"] is False
    assert "api_key" not in response.json()
