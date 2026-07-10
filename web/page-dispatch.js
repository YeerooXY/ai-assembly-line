import { escapeHtml, initializeViewerPage, renderChipRow, renderKeyValueRows, renderList } from "./viewer-layout.js";

const LOCKED_STATUSES = new Set(["claimed", "in_progress", "review"]);
const DONE_STATUSES = new Set(["done"]);
const BLOCKED_STATUSES = new Set(["blocked"]);
const FILTERS = ["all", "available", "locked", "waiting", "blocked", "done"];

initializeViewerPage({
  pageId: "dispatch",
  eyebrow: "Task Dispatch",
  title: "Available Task Graph",
  description: "Topological task board that highlights what can be picked up now and generates one-copy execution context for a fresh AI chat.",
  requiredKeys: ["taskBacklog", "collaborationState"],
  extraSourceFiles: ["prompts/07-task-executor.md", "contracts/task_run.schema.json"],
  helperNote: "Green tasks are available now. Red tasks are locked or blocked. Yellow tasks are waiting for dependencies or review.",
  renderContent(container, data) {
    const tasks = Array.isArray(data.taskBacklog) ? data.taskBacklog : [];
    const state = data.collaborationState && typeof data.collaborationState === "object" ? data.collaborationState : {};
    const model = buildDispatchModel(tasks, state);

    container.innerHTML = renderDispatchShell(model);
    bindDispatchControls(container, model);
  },
});

function buildDispatchModel(tasks, state) {
  const actors = Array.isArray(state.actors) ? state.actors : [];
  const actorMap = new Map(actors.map((actor) => [actor.actor_id, actor]));
  const assignmentMap = buildAssignmentMap(state.task_assignments);
  const taskMap = new Map(tasks.map((task) => [task.id, task]));
  const layers = computeTopologicalLayers(tasks);

  const rawRows = tasks.map((task) => {
    const assignment = assignmentMap.get(task.id);
    const actor = assignment?.assigned_to ? actorMap.get(assignment.assigned_to) : null;
    return {
      task,
      assignment,
      id: task.id ?? "unknown-task",
      title: task.title ?? task.summary ?? task.id ?? "Untitled task",
      summary: task.summary ?? "",
      ownerRole: task.owner_role ?? "unknown role",
      repoTarget: task.repo_target ?? "unknown repo",
      lane: task.lane ?? "unassigned lane",
      planningStatus: task.status ?? "not set",
      executionStatus: assignment?.status ?? "unclaimed",
      assignedTo: actor?.display_name ?? assignment?.assignee_label ?? assignment?.assigned_to ?? "Unassigned",
      assigneeType: assignment?.assignee_type ?? actor?.kind ?? "unassigned",
      dependsOn: Array.isArray(task.depends_on) ? task.depends_on : [],
      outputs: Array.isArray(task.outputs) ? task.outputs : [],
      verification: Array.isArray(task.verification) ? task.verification : [],
      acceptanceCriteria: Array.isArray(task.acceptance_criteria) ? task.acceptance_criteria : [],
      proof: Array.isArray(assignment?.proof) ? assignment.proof : [],
      notes: assignment?.notes ?? "",
      updatedAt: assignment?.updated_at ?? "",
    };
  });

  const rowsById = new Map(rawRows.map((row) => [row.id, row]));
  const rows = rawRows.map((row) => classifyRow(row, rowsById, taskMap));
  const classifiedRowsById = new Map(rows.map((row) => [row.id, row]));
  const summary = summarizeRows(rows);
  const defaultTaskId = rows.find((row) => row.dispatchStatus === "available")?.id ?? rows[0]?.id ?? "";

  return {
    actors,
    state,
    tasks,
    layers,
    rows,
    rowsById: classifiedRowsById,
    summary,
    defaultTaskId,
  };
}

function buildAssignmentMap(assignments) {
  const map = new Map();
  if (!Array.isArray(assignments)) {
    return map;
  }

  for (const assignment of assignments) {
    if (assignment?.task_id) {
      map.set(assignment.task_id, assignment);
    }
  }
  return map;
}

function classifyRow(row, rowsById, taskMap) {
  const missingDependencies = row.dependsOn.filter((dependencyId) => !taskMap.has(dependencyId));
  const dependencyRows = row.dependsOn.map((dependencyId) => rowsById.get(dependencyId)).filter(Boolean);
  const blockedDependencies = dependencyRows.filter((dependency) => BLOCKED_STATUSES.has(dependency.executionStatus));
  const unfinishedDependencies = dependencyRows.filter((dependency) => !isDone(dependency));

  let dispatchStatus = "available";
  let visualStatus = "complete";
  let dispatchReason = "All dependencies are done or absent, and the task is free to take.";

  if (isDone(row)) {
    dispatchStatus = "done";
    visualStatus = "done";
    dispatchReason = "Task is already marked done.";
  } else if (BLOCKED_STATUSES.has(row.executionStatus) || missingDependencies.length || blockedDependencies.length) {
    dispatchStatus = "blocked";
    visualStatus = "blocked";
    dispatchReason = missingDependencies.length
      ? `Missing dependency reference(s): ${missingDependencies.join(", ")}.`
      : blockedDependencies.length
        ? `Blocked by dependency task(s): ${blockedDependencies.map((dependency) => dependency.id).join(", ")}.`
        : "Task is explicitly blocked.";
  } else if (LOCKED_STATUSES.has(row.executionStatus)) {
    dispatchStatus = "locked";
    visualStatus = "blocked";
    dispatchReason = `Task is currently ${row.executionStatus} by ${row.assignedTo}.`;
  } else if (unfinishedDependencies.length) {
    dispatchStatus = "waiting";
    visualStatus = "review";
    dispatchReason = `Waiting for dependency task(s): ${unfinishedDependencies.map((dependency) => dependency.id).join(", ")}.`;
  }

  return {
    ...row,
    dependencyRows,
    missingDependencies,
    blockedDependencies,
    unfinishedDependencies,
    dispatchStatus,
    visualStatus,
    dispatchReason,
  };
}

function isDone(row) {
  return DONE_STATUSES.has(row.executionStatus) || row.planningStatus === "done";
}

function computeTopologicalLayers(tasks) {
  const taskMap = new Map(tasks.map((task) => [task.id, task]));
  const indegree = new Map(tasks.map((task) => [task.id, 0]));
  const dependents = new Map(tasks.map((task) => [task.id, []]));

  for (const task of tasks) {
    const dependencies = Array.isArray(task.depends_on) ? task.depends_on : [];
    for (const dependencyId of dependencies) {
      if (!taskMap.has(dependencyId)) {
        continue;
      }
      indegree.set(task.id, (indegree.get(task.id) ?? 0) + 1);
      dependents.get(dependencyId).push(task.id);
    }
  }

  const remaining = new Set(tasks.map((task) => task.id));
  let ready = tasks.filter((task) => (indegree.get(task.id) ?? 0) === 0).map((task) => task.id);
  const layers = [];

  while (ready.length) {
    const layerIds = ready.filter((taskId) => remaining.has(taskId));
    if (!layerIds.length) {
      break;
    }

    layers.push({ label: `Wave ${layers.length + 1}`, taskIds: layerIds, cyclic: false });
    const next = [];

    for (const taskId of layerIds) {
      remaining.delete(taskId);
      for (const dependentId of dependents.get(taskId) ?? []) {
        indegree.set(dependentId, (indegree.get(dependentId) ?? 0) - 1);
        if ((indegree.get(dependentId) ?? 0) === 0) {
          next.push(dependentId);
        }
      }
    }

    ready = next;
  }

  if (remaining.size) {
    layers.push({ label: "Unsorted / cyclic", taskIds: Array.from(remaining), cyclic: true });
  }

  return layers;
}

function summarizeRows(rows) {
  return rows.reduce(
    (summary, row) => {
      summary.total += 1;
      summary[row.dispatchStatus] = (summary[row.dispatchStatus] ?? 0) + 1;
      return summary;
    },
    {
      total: 0,
      available: 0,
      locked: 0,
      waiting: 0,
      blocked: 0,
      done: 0,
    },
  );
}

function renderDispatchShell(model) {
  const summaryRows = [
    { label: "Total", value: escapeHtml(String(model.summary.total)) },
    { label: "Available now", value: `<strong>${escapeHtml(String(model.summary.available))}</strong>` },
    { label: "Locked", value: escapeHtml(String(model.summary.locked)) },
    { label: "Waiting", value: escapeHtml(String(model.summary.waiting)) },
    { label: "Blocked", value: escapeHtml(String(model.summary.blocked)) },
    { label: "Done", value: escapeHtml(String(model.summary.done)) },
  ];

  return `
    <div class="stack">
      <section class="card">
        <div class="section-heading">
          <div>
            <h2>Dispatch Board</h2>
            <p class="muted">Pick a green task, copy its full execution context, and paste it into a fresh AI chat.</p>
          </div>
          <span class="chip status-complete">${escapeHtml(String(model.summary.available))} available</span>
        </div>
        ${renderKeyValueRows(summaryRows)}
      </section>

      <section class="card">
        <div class="section-heading">
          <div>
            <h3>Topological graph</h3>
            <p class="muted">Tasks are grouped by dependency wave. Availability is derived from dependency completion and collaboration state.</p>
          </div>
          <div class="chip-row" id="dispatchFilters">
            ${FILTERS.map((filter) => `<button type="button" data-filter="${escapeHtml(filter)}">${escapeHtml(filter)}</button>`).join("")}
          </div>
        </div>
        <div id="dispatchGraph" class="dependency-graph"></div>
      </section>

      <section id="dispatchDetail" class="card"></section>
    </div>
  `;
}

function bindDispatchControls(container, model) {
  let selectedTaskId = model.defaultTaskId;
  let activeFilter = "available";
  const graph = container.querySelector("#dispatchGraph");
  const detail = container.querySelector("#dispatchDetail");
  const filterContainer = container.querySelector("#dispatchFilters");

  container.addEventListener("click", async (event) => {
    const filterButton = event.target.closest("[data-filter]");
    if (filterButton) {
      activeFilter = filterButton.dataset.filter;
      render();
      return;
    }

    const node = event.target.closest("[data-task-id]");
    if (node) {
      selectedTaskId = node.dataset.taskId;
      render();
      return;
    }

    const copyButton = event.target.closest("[data-copy-kind]");
    if (copyButton) {
      const selectedRow = model.rowsById.get(selectedTaskId);
      if (!selectedRow) {
        return;
      }
      const text = copyButton.dataset.copyKind === "task" ? JSON.stringify(selectedRow.task, null, 2) : buildExecutionContext(selectedRow, model);
      await copyText(text, copyButton);
    }
  });

  function render() {
    graph.innerHTML = renderGraph(model, activeFilter, selectedTaskId);
    detail.innerHTML = renderTaskDetail(model.rowsById.get(selectedTaskId), model);
    for (const button of filterContainer.querySelectorAll("[data-filter]")) {
      button.classList.toggle("active", button.dataset.filter === activeFilter);
    }
  }

  render();
}

function renderGraph(model, activeFilter, selectedTaskId) {
  if (!model.rows.length) {
    return '<p class="muted">No tasks exist in generated/task_backlog.json yet.</p>';
  }

  const columns = model.layers.map((layer) => {
    const rows = layer.taskIds
      .map((taskId) => model.rowsById.get(taskId))
      .filter(Boolean)
      .filter((row) => activeFilter === "all" || row.dispatchStatus === activeFilter);

    return `
      <section class="graph-column ${layer.cyclic ? "error-card" : ""}">
        <div class="graph-column-heading">
          <h4>${escapeHtml(layer.label)}</h4>
          <span class="chip">${escapeHtml(String(rows.length))}</span>
        </div>
        <div class="graph-node-stack">
          ${rows.length ? rows.map((row) => renderGraphNode(row, selectedTaskId)).join("") : '<p class="muted">No tasks for this filter.</p>'}
        </div>
      </section>
    `;
  });

  return `<div class="graph-columns">${columns.join("")}</div>`;
}

function renderGraphNode(row, selectedTaskId) {
  const selectedLabel = row.id === selectedTaskId ? ' <span class="chip status-active">selected</span>' : "";
  return `
    <article class="graph-node status-${escapeHtml(row.visualStatus)}" data-task-id="${escapeHtml(row.id)}" tabindex="0">
      <div class="graph-node-title">
        <strong>${escapeHtml(row.id)}</strong>
        <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
      </div>
      <p>${escapeHtml(row.title)}</p>
      <div class="graph-node-meta">
        <span>${escapeHtml(row.ownerRole)} · ${escapeHtml(row.repoTarget)}</span>
        <span>${escapeHtml(row.dispatchReason)}</span>
        ${selectedLabel}
      </div>
    </article>
  `;
}

function renderTaskDetail(row, model) {
  if (!row) {
    return '<p class="muted">Select a task to see dispatch context.</p>';
  }

  const dependencyRows = row.dependsOn.map((dependencyId) => model.rowsById.get(dependencyId)).filter(Boolean);
  const missingDependencyText = row.missingDependencies.length ? `Missing: ${row.missingDependencies.join(", ")}` : "";

  return `
    <div class="section-heading">
      <div>
        <h3>${escapeHtml(row.id)}</h3>
        <p class="muted">${escapeHtml(row.title)}</p>
      </div>
      <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
    </div>

    <div class="chip-row">
      <button type="button" data-copy-kind="context">Copy Full Execution Context</button>
      <button type="button" data-copy-kind="task">Copy Task JSON</button>
    </div>

    ${renderKeyValueRows([
      { label: "Availability", value: escapeHtml(row.dispatchReason) },
      { label: "Assigned To", value: escapeHtml(row.assignedTo) },
      { label: "Execution Status", value: `<code>${escapeHtml(row.executionStatus)}</code>` },
      { label: "Owner Role", value: escapeHtml(row.ownerRole) },
      { label: "Repo Target", value: escapeHtml(row.repoTarget) },
      { label: "Expected Task Run", value: `<code>generated/task_runs/${escapeHtml(row.id)}.json</code>` },
    ])}

    <h4>Dependencies</h4>
    ${dependencyRows.length ? renderDependencyCards(dependencyRows) : '<p class="muted">No known dependencies.</p>'}
    ${missingDependencyText ? `<p class="helper">${escapeHtml(missingDependencyText)}</p>` : ""}

    <h4>Acceptance Criteria</h4>
    ${renderList(row.acceptanceCriteria, "No acceptance criteria listed")}

    <h4>Expected Outputs</h4>
    ${renderList(row.outputs, "No outputs listed")}

    <h4>Verification</h4>
    ${renderList(row.verification, "No verification listed")}

    <h4>Task JSON Preview</h4>
    <pre class="code-block">${escapeHtml(JSON.stringify(row.task, null, 2))}</pre>
  `;
}

function renderDependencyCards(rows) {
  return `
    <div class="card-grid two-up">
      ${rows.map((row) => `
        <article class="card inset-card">
          <div class="section-heading">
            <strong>${escapeHtml(row.id)}</strong>
            <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
          </div>
          <p class="muted">${escapeHtml(row.title)}</p>
          ${row.proof.length ? renderProofSummary(row.proof) : '<p class="muted">No proof reference recorded.</p>'}
        </article>
      `).join("")}
    </div>
  `;
}

function renderProofSummary(proofItems) {
  return `
    <ul class="list">
      ${proofItems.map((item) => `<li>${escapeHtml(item.summary ?? item.path ?? item.kind ?? "proof")}</li>`).join("")}
    </ul>
  `;
}

function buildExecutionContext(row, model) {
  const dependencyRows = row.dependsOn.map((dependencyId) => model.rowsById.get(dependencyId)).filter(Boolean);
  const dependencySummary = dependencyRows.length
    ? dependencyRows.map((dependency) => `- ${dependency.id}: ${dependency.dispatchStatus}; proof: ${summarizeProof(dependency.proof)}`).join("\n")
    : "- No dependencies.";

  return `# AI Assembly Line - One Task Execution Context

You are executing exactly one task from the AI Assembly Line backlog. Stay inside this task boundary and return a task run JSON report matching contracts/task_run.schema.json.

Expected output path for your report:
generated/task_runs/${row.id}.json

Dispatch status: ${row.dispatchStatus}
Reason: ${row.dispatchReason}
Assigned to: ${row.assignedTo} (${row.assigneeType})

## Task JSON

${JSON.stringify(row.task, null, 2)}

## Current Assignment

${JSON.stringify(row.assignment ?? { task_id: row.id, status: "unclaimed" }, null, 2)}

## Dependency Summary

${dependencySummary}

## Required Output Shape

Return exactly one JSON object with:
- schema_version
- task_id
- run_id
- actor_id
- status
- implementation_summary
- files_changed
- verification
- proof
- blockers
- notes
- updated_at

Use status "review" when implementation appears complete but still needs human review. Use "blocked" if required context or dependencies are missing. Do not mark "done" without accepted proof.
`;
}

function summarizeProof(proofItems) {
  if (!proofItems.length) {
    return "no proof recorded";
  }
  return proofItems.map((item) => item.path ?? item.summary ?? item.kind ?? "proof").join("; ");
}

async function copyText(text, button) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      fallbackCopy(text);
    }
    flashButton(button, "Copied");
  } catch (error) {
    fallbackCopy(text);
    flashButton(button, "Copied");
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

function flashButton(button, label) {
  const original = button.textContent;
  button.textContent = label;
  window.setTimeout(() => {
    button.textContent = original;
  }, 1200);
}
