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
