import { formatError, isFileProtocol, loadGeneratedState, loadLocalState, sourceFilesForKeys } from "./viewer-data.js";

const NAV_ITEMS = [
  { id: "overview", label: "Overview", href: "index.html" },
  { id: "repos", label: "Repos", href: "repos.html" },
  { id: "backlog", label: "Backlog", href: "backlog.html" },
  { id: "prompts", label: "Prompts", href: "prompts.html" },
  { id: "slots", label: "Slots", href: "slots.html" },
  { id: "verification", label: "Verification", href: "verification.html" },
];

export function initializeViewerPage(config) {
  const {
    pageId,
    eyebrow,
    title,
    description,
    requiredKeys,
    extraSourceFiles = [],
    helperNote = "",
    renderContent,
  } = config;

  const app = document.getElementById("app");
  if (!app) {
    throw new Error('Missing required root element: #app');
  }

  const sourceFiles = [...sourceFilesForKeys(requiredKeys), ...extraSourceFiles];
  app.innerHTML = `
    <header class="hero shell-width">
      <div class="hero-copy">
        <p class="eyebrow">${escapeHtml(eyebrow)}</p>
        <h1>${escapeHtml(title)}</h1>
        <p class="lede">${escapeHtml(description)}</p>
        <nav class="site-nav" aria-label="Viewer pages">
          ${NAV_ITEMS.map((item) => renderNavLink(item, pageId)).join("")}
        </nav>
      </div>
      <div class="hero-actions">
        <button id="reloadButton" type="button">Reload Generated State</button>
        <label class="file-button" for="filePicker">Load Local JSON Files</label>
        <input id="filePicker" type="file" accept=".json" multiple>
      </div>
    </header>

    <main class="layout shell-width">
      <section class="panel status-panel">
        <h2>Status</h2>
        <p id="statusMessage" class="status loading">Loading generated state...</p>
        <p class="source-note">
          This page renders generated state only. It does not edit or invent task, repo, prompt, slot, or contract structure.
        </p>
        <p class="source-note">
          Source of truth for this page:
          ${sourceFiles.map((path) => `<code>${escapeHtml(path)}</code>`).join(", ")}.
        </p>
        <p class="helper">
          Serve the repo root with <code>python -m http.server 8000</code> and open <code>http://localhost:8000/web/</code>.
          If the page is opened with <code>file://</code> and fetch is blocked, load the required JSON files with the button above.
        </p>
        ${helperNote ? `<p class="helper">${helperNote}</p>` : ""}
        <p class="helper">
          Required local files for this page: ${sourceFiles.map((path) => `<code>${escapeHtml(path)}</code>`).join(", ")}.
        </p>
      </section>

      <section class="panel">
        <div id="pageContent"></div>
      </section>
    </main>
  `;

  const statusMessage = document.getElementById("statusMessage");
  const pageContent = document.getElementById("pageContent");
  const reloadButton = document.getElementById("reloadButton");
  const filePicker = document.getElementById("filePicker");

  reloadButton.addEventListener("click", () => {
    void fetchAndRender();
  });

  filePicker.addEventListener("change", async (event) => {
    try {
      setStatus(statusMessage, "Loading local JSON files...", "loading");
      clearContent(pageContent);
      const data = await loadLocalState(requiredKeys, event.target.files);
      renderContent(pageContent, data);
      setStatus(statusMessage, "Loaded generated state from local files.", "success");
    } catch (error) {
      renderFailure(pageContent, statusMessage, error, requiredKeys);
    } finally {
      filePicker.value = "";
    }
  });

  void fetchAndRender();

  async function fetchAndRender() {
    try {
      setStatus(statusMessage, "Loading generated state...", "loading");
      clearContent(pageContent);
      const data = await loadGeneratedState(requiredKeys);
      renderContent(pageContent, data);
      setStatus(statusMessage, `Loaded generated state from ${sourceFiles.join(", ")}.`, "success");
    } catch (error) {
      renderFailure(pageContent, statusMessage, error, requiredKeys);
    }
  }
}

function renderFailure(pageContent, statusMessage, error, requiredKeys) {
  const fileList = sourceFilesForKeys(requiredKeys)
    .map((path) => `<code>${escapeHtml(path)}</code>`)
    .join(", ");

  const hint = isFileProtocol()
    ? 'Fetch is likely blocked under <code>file://</code>. Use <code>python -m http.server 8000</code> from the repo root or load the required files manually.'
    : 'Check that the generated JSON files exist and contain valid JSON.';

  setStatus(statusMessage, formatError(error), "error");
  pageContent.innerHTML = `
    <div class="card error-card">
      <h3>Unable to render this page</h3>
      <p>${escapeHtml(formatError(error))}</p>
      <p class="helper">This page requires ${fileList}.</p>
      <p class="helper">${hint}</p>
    </div>
  `;
}

function renderNavLink(item, pageId) {
  const className = item.id === pageId ? "nav-link active" : "nav-link";
  return `<a class="${className}" href="${item.href}">${escapeHtml(item.label)}</a>`;
}

export function renderList(items, emptyLabel = "None") {
  if (!items || items.length === 0) {
    return `<p class="muted">${escapeHtml(emptyLabel)}</p>`;
  }

  return `<ul class="list">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

export function renderChipRow(items, emptyLabel = "None") {
  if (!items || items.length === 0) {
    return `<p class="muted">${escapeHtml(emptyLabel)}</p>`;
  }

  return `<div class="chip-row">${items.map((item) => `<span class="chip">${escapeHtml(item)}</span>`).join("")}</div>`;
}

export function renderKeyValueRows(rows) {
  return `
    <dl class="meta">
      ${rows
        .map(
          (row) => `
            <div>
              <dt>${escapeHtml(row.label)}</dt>
              <dd>${row.value}</dd>
            </div>
          `,
        )
        .join("")}
    </dl>
  `;
}

export function renderCardGrid(cardsMarkup, className = "") {
  const suffix = className ? ` ${className}` : "";
  return `<div class="card-grid${suffix}">${cardsMarkup}</div>`;
}

export function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function clearContent(pageContent) {
  pageContent.innerHTML = "";
}

function setStatus(statusMessage, message, kind) {
  statusMessage.textContent = message;
  statusMessage.className = `status ${kind}`;
}
