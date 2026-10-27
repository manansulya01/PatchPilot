const $ = (id) => document.getElementById(id);
const sampleCode = `def calculate_total(prices, discount):
    total = 0
    for price in prices:
        total += round(price * (1 - discount), 2)
    return total`;
let lastReport = null;
let toastTimer = null;

function toast(message, isError = false) {
  const node = $("toast");
  node.textContent = message;
  node.classList.remove("hidden", "error");
  if (isError) node.classList.add("error");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => node.classList.add("hidden"), 3200);
}
function setStatus(label, type = "neutral") {
  const node = $("result-state");
  node.className = `state-pill ${type}`;
  node.innerHTML = '<span class="state-dot"></span>' + escapeHtml(label);
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
}
function updateEditorMeta() {
  const code = $("source-code").value;
  $("char-count").textContent = `${code.length.toLocaleString()} chars`;
  $("line-numbers").innerHTML = Array.from({length: Math.max(1, code.split("\n").length)}, (_, i) => i + 1).join("<br>");
}
function showView(view) {
  $("empty-state").classList.toggle("hidden", view !== "empty");
  $("loading-state").classList.toggle("hidden", view !== "loading");
  $("report").classList.toggle("hidden", view !== "report");
}
function loadExample() {
  $("bug-description").value = "The checkout total is wrong when a discount is applied to a cart with multiple items. The total should apply the discount to the subtotal and round only the final amount.";
  $("language").value = "python";
  $("source-code").value = sampleCode;
  $("mode").value = "demo";
  $("mode-note").textContent = "Demo output is illustrative. It does not call an AI model or execute tests.";
  updateEditorMeta();
  showView("empty");
  setStatus("AWAITING INPUT");
}
function openSettings() {
  $("settings-message").textContent = "";
  $("settings-message").classList.remove("error");
  $("settings-modal").classList.remove("hidden");
  $("api-key").focus();
}
function closeSettings() { $("settings-modal").classList.add("hidden"); }
async function refreshConfig() {
  try {
    const response = await fetch("/api/config");
    const data = await response.json();
    $("connection-title").textContent = data.configured ? "Nebius connected" : "Demo mode";
    $("connection-subtitle").textContent = data.configured ? data.model : "No API key needed";
    $("connection-dot").classList.toggle("connected", Boolean(data.configured));
    if (data.base_url) $("base-url").value = data.base_url;
    if (data.model) $("model-id").value = data.model;
    if (data.configured && $("mode").value === "demo") {
      $("mode-note").textContent = "A model connection is configured. Select Live Nemotron to use it.";
    }
  } catch (_) {
    $("connection-title").textContent = "Server unavailable";
    $("connection-subtitle").textContent = "Check the local backend";
  }
}
async function saveSettings(event) {
  event.preventDefault();
  const button = $("save-settings");
  button.disabled = true;
  button.textContent = "Saving…";
  const message = $("settings-message");
  message.classList.remove("error");
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        api_key: $("api-key").value || null,
        base_url: $("base-url").value.trim(),
        model: $("model-id").value.trim()
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not save settings.");
    message.textContent = "Connection settings saved in server memory. Run a small live test to verify access.";
    $("api-key").value = "";
    await refreshConfig();
    toast("Connection settings saved.");
  } catch (error) {
    message.textContent = error.message;
    message.classList.add("error");
  } finally {
    button.disabled = false;
    button.innerHTML = 'Save connection <span>→</span>';
  }
}
async function clearSettings() {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({clear: true})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not clear settings.");
    $("api-key").value = "";
    $("model-id").value = "";
    $("settings-message").textContent = "Connection cleared from server memory.";
    await refreshConfig();
    toast("Connection cleared.");
  } catch (error) {
    $("settings-message").textContent = error.message;
    $("settings-message").classList.add("error");
  }
}
async function runAnalysis() {
  const description = $("bug-description").value.trim();
  const code = $("source-code").value;
  const mode = $("mode").value;
  if (description.length < 5) { toast("Add a more detailed bug report first.", true); $("bug-description").focus(); return; }
  if (!code.trim()) { toast("Add the relevant source code first.", true); $("source-code").focus(); return; }
  $("analyze").disabled = true;
  $("analyze").innerHTML = '<span class="loader-small"></span> Analyzing…';
  setStatus("ANALYZING");
  showView("loading");
  $("loading-caption").textContent = mode === "live" ? "Requesting analysis from your configured Nebius model" : "Preparing clearly labeled illustrative output";
  const started = performance.now();
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({description, code, language: $("language").value, mode})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis failed.");
    data.elapsed_ms = data.elapsed_ms || Math.round(performance.now() - started);
    lastReport = {input: {description, code, language: $("language").value}, ...data};
    renderReport(data);
    showView("report");
    setStatus("REPORT READY", "ready");
  } catch (error) {
    showView("empty");
    setStatus("REQUEST FAILED", "error");
    toast(error.message, true);
  } finally {
    $("analyze").disabled = false;
    $("analyze").innerHTML = '<span class="button-icon">✳</span> Analyze bug <span class="button-arrow">↗</span>';
  }
}
function renderReport(data) {
  $("model-badge").textContent = data.mode === "live" ? "LIVE · " + (data.model || "NVIDIA MODEL") : "DEMO · SIMULATED";
  $("elapsed").textContent = `${data.elapsed_ms || 0} ms`;
  $("analysis-text").textContent = data.analysis || "No root-cause explanation returned.";
  $("patch-text").textContent = data.patch || "# No patch proposed. More source context may be needed.";
  $("test-text").textContent = data.regression_test || "# No regression test proposed.";
  const review = data.patch_review || {status: "UNAVAILABLE", warning_count: 0, added_lines_checked: 0, findings: [], limitations: "Preflight data was not returned."};
  const reviewStatus = $("patch-review-status");
  reviewStatus.textContent = review.status || "UNAVAILABLE";
  reviewStatus.className = "guard-status " + (review.warning_count ? "warning" : (review.status === "NO HEURISTIC FLAGS" ? "clear" : "neutral"));
  $("patch-review-summary").textContent = `${review.added_lines_checked || 0} added diff lines inspected · ${review.warning_count || 0} warning(s). ${review.limitations || ""}`;
  const findings = Array.isArray(review.findings) ? review.findings : [];
  $("patch-review-findings").innerHTML = findings.length
    ? findings.map(item => '<li><strong>' + escapeHtml(item.severity || "info").toUpperCase() + ' · ' + escapeHtml(item.id || "finding") + '</strong>: ' + escapeHtml(item.message || "Review this item.") + '</li>').join("")
    : '<li>No heuristic flags were triggered. This does not mean the patch is correct or safe.</li>';
  const risks = [
    ...(Array.isArray(data.assumptions) ? data.assumptions.map(x => "Assumption: " + x) : []),
    ...(Array.isArray(data.risks) ? data.risks : []),
    ...(Array.isArray(data.next_steps) ? data.next_steps.map(x => "Next: " + x) : [])
  ];
  if (!risks.length) risks.push("Model output can be incorrect; review the diff and test independently.");
  $("risks-list").innerHTML = risks.map(item => '<li>' + escapeHtml(item) + '</li>').join("");
  $("verification-heading");
}
async function copyText(text, label) {
  try {
    await navigator.clipboard.writeText(text);
    toast(label + " copied.");
  } catch (_) {
    const area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
    toast(label + " copied.");
  }
}
function exportReport() {
  if (!lastReport) return;
  const blob = new Blob([JSON.stringify(lastReport, null, 2)], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "patchpilot-evidence-report.json";
  a.click();
  URL.revokeObjectURL(url);
  toast("Evidence report exported.");
}
$("source-code").addEventListener("input", updateEditorMeta);
$("new-analysis").addEventListener("click", () => { loadExample(); $("bug-description").focus(); });
$("load-example").addEventListener("click", loadExample);
$("try-example").addEventListener("click", () => { loadExample(); runAnalysis(); });
$("reset-code").addEventListener("click", () => { $("source-code").value = sampleCode; updateEditorMeta(); });
$("analyze").addEventListener("click", runAnalysis);
$("mode").addEventListener("change", () => {
  const live = $("mode").value === "live";
  $("mode-note").textContent = live
    ? "Live mode calls your configured model. It requires working Nebius credentials and an available model ID."
    : "Demo output is illustrative. It does not call an AI model or execute tests.";
  $("mode-note").style.color = live ? "#a8c7ff" : "";
  $("mode-select");
});
$("open-settings").addEventListener("click", openSettings);
$("top-settings").addEventListener("click", openSettings);
$("close-settings").addEventListener("click", closeSettings);
$("settings-modal").addEventListener("click", (event) => { if (event.target === $("settings-modal")) closeSettings(); });
$("settings-form").addEventListener("submit", saveSettings);
$("clear-settings").addEventListener("click", clearSettings);
$("copy-patch").addEventListener("click", () => copyText($("patch-text").textContent, "Patch"));
$("copy-test").addEventListener("click", () => copyText($("test-text").textContent, "Test"));
$("export-report").addEventListener("click", exportReport);
$("new-run").addEventListener("click", () => { showView("empty"); $("bug-description").focus(); });
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault(); loadExample(); $("bug-description").focus();
  }
  if (event.key === "Escape") closeSettings();
});
updateEditorMeta();
refreshConfig();
