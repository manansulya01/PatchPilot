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
