import os
import subprocess
import sys
from pathlib import Path


def test_preflight_rejects_untrusted_endpoint_before_network_call():
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env.update({
        "NEBIUS_API_KEY": "test-key-never-real",
        "NEBIUS_BASE_URL": "https://nebius.com.attacker.example/v1",
        "NEBIUS_MODEL": "nvidia/Nemotron-3_5-Lightning",
    })
    result = subprocess.run(
        [sys.executable, "scripts/check_nebius.py"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 2
    assert "official *.nebius.com host" in result.stdout
    assert "test-key-never-real" not in result.stdout
    assert "test-key-never-real" not in result.stderr
