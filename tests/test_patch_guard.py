from patch_guard import inspect_patch


def test_flags_dynamic_execution_in_added_lines():
    result = inspect_patch("--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old = 1\n+result = eval(user_input)\n")
    assert result["status"] == "REVIEW REQUIRED"
    assert any(item["id"] == "dynamic_execution" for item in result["findings"])


def test_clean_diff_is_not_called_verified():
    result = inspect_patch("--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old = 1\n+new = 2\n")
    assert result["status"] == "NO HEURISTIC FLAGS"
    assert "does not establish correctness or safety" in result["limitations"]


def test_non_diff_output_gets_format_warning():
    result = inspect_patch("Maybe change the code to use a loop.")
    assert any(item["id"] == "diff_format" for item in result["findings"])


def test_empty_patch_is_explicit():
    result = inspect_patch("")
    assert result["status"] == "NO PATCH"
    assert result["warning_count"] == 0


def test_only_added_lines_are_scanned():
    result = inspect_patch("--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-result = eval(user_input)\n+result = safe_value\n")
    assert not any(item["id"] == "dynamic_execution" for item in result["findings"])


def test_flags_selected_risky_added_patterns():
    samples = {
        "shell_execution": "+subprocess.run(user_command, shell=True)",
        "unsafe_deserialization": "+payload = pickle.loads(blob)",
        "network_access": "+response = requests.get(url)",
        "secret_access": "+token = os.getenv('API_TOKEN')",
    }
    for expected_id, added_line in samples.items():
        patch = "--- a/file.py\n+++ b/file.py\n@@ -1 +1 @@\n-old = None\n" + added_line + "\n"
        result = inspect_patch(patch)
        assert any(item["id"] == expected_id for item in result["findings"])


def test_oversized_patch_is_flagged():
    result = inspect_patch("--- a/file.py\n+++ b/file.py\n@@ -1 +1 @@\n+" + ("x" * 20001))
    assert any(item["id"] == "large_patch" for item in result["findings"])
